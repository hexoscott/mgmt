import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { ModelAndEffort } from '../types'
import { appendToTail, describeModelAndEffort } from './describe'

const current = atom(
  { plugin: 'model-effort-hint', key: 'current' } as const,
  null,
  { shape: 'model-effort-1' },
)

function isSame(a: ModelAndEffort | null, b: ModelAndEffort): boolean {
  return a !== null && a.model === b.model && a.effort === b.effort
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    const isFirstStartOfSession = (await read($, current)) === null

    if (isFirstStartOfSession) {
      const model = await $.session.model()
      await update($, current, () => ({ model, effort: null }))
    }

    return result
  })

  // Each main-loop request names the model and effort the engine resolved for
  // it, so the hint follows /model and /effort from the next request on.
  on('turn.step', async function* ($, e, next) {
    const isMainLoop = e.agentId === undefined

    if (isMainLoop) {
      const observed: ModelAndEffort = { model: e.model, effort: e.effort ?? null }
      await update($, current, previous => (isSame(previous, observed) ? previous : observed))
    }

    return yield* next(e)
  })

  on('ui.render', { component: 'PromptHint' }, async ($, e, next) => {
    const shown = await read($, current)

    if (shown === null) {
      return next(e)
    }

    const tail = appendToTail(e.props.tail, describeModelAndEffort(shown))

    return next({ ...e, props: { ...e.props, tail } })
  })
}
