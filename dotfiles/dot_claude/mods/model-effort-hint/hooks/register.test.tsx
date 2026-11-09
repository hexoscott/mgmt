import type { On } from 'claude-code'
import { expect, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'

const PROMPT_HINT = {
  plugin: 'model-effort-hint',
  component: 'PromptHint',
  props: { isDraft: false, isWorking: false, hint: '? for shortcuts' },
} as const

const MAIN_LOOP_STEP = {
  turnId: 't1',
  index: 0,
  model: 'claude-opus-5-5',
  effort: 'xhigh',
  messageCount: 1,
} as const

const STEP_RESULT = {
  turnId: 't1',
  index: 0,
  answer: '',
  toolUses: [],
  stopReason: null,
  usage: null,
} as const

function standInEngine(on: On) {
  on('session.model', () => ({ value: 'claude-opus-5-5' }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('turn.step', async function* () {
    return STEP_RESULT
  })
  on('ui.render', ($, e) => {
    const { Text } = $.ui.resolve(e)
    const tail = (e.props as { tail?: string }).tail

    return <Text>{`tail=${tail ?? ''}`}</Text>
  })
}

async function drawnTail($: Engine, surface: 'terminal' | 'desktop') {
  const ui = await $.ui.mount({ ...PROMPT_HINT, surface })
  const text = (await ui.find({ type: 'Text' }))?.text
  await ui.unmount()

  return text
}

async function runStep($: Engine, input: object) {
  const stream = $.turn.step({ ...MAIN_LOOP_STEP, ...input })
  for await (const _chunk of stream) {
    // drain
  }
}

test('before the first request it shows the session model alone', async ($, on) => {
  standInEngine(on)
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })

  for (const surface of ['terminal', 'desktop'] as const) {
    expect(await drawnTail($, surface)).toBe('tail=· Opus 5.5')
  }
})

test('a main-loop request sets the model and effort shown', async ($, on) => {
  standInEngine(on)
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
  await runStep($, { model: 'claude-sonnet-5-5', effort: 'high' })

  for (const surface of ['terminal', 'desktop'] as const) {
    expect(await drawnTail($, surface)).toBe('tail=· Sonnet 5.5 · high effort')
  }
})

test("a subagent's request leaves the main model and effort alone", async ($, on) => {
  standInEngine(on)
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
  await runStep($, {})
  await runStep($, { model: 'claude-haiku-5-5', effort: 'low', agentId: 'a1' })

  expect(await drawnTail($, 'terminal')).toBe('tail=· Opus 5.5 · xhigh effort')
})

test('a hot reload keeps the effort the last request showed', async ($, on) => {
  standInEngine(on)
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
  await runStep($, { effort: 'max' })
  // A hot reload of the mod raises session.start again with state kept.
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })

  expect(await drawnTail($, 'terminal')).toBe('tail=· Opus 5.5 · max effort')
})

test("another plugin's tail is kept", async ($, on) => {
  standInEngine(on)
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
  const ui = await $.ui.mount({
    ...PROMPT_HINT,
    props: { ...PROMPT_HINT.props, tail: 'other' },
    surface: 'terminal',
  })

  expect((await ui.find({ type: 'Text' }))?.text).toBe('tail=other · Opus 5.5')
  await ui.unmount()
})
