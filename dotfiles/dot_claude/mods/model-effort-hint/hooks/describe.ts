import type { ModelAndEffort } from '../types'

const SEPARATOR = ' · '

// Matches the family and version inside ids such as `claude-opus-4-5-20251101`,
// `us.anthropic.claude-haiku-5-5-v1:0` or a gateway's `claude-sonnet-4.5`;
// a trailing date is not a minor version.
const MODEL_ID = /claude-([a-z]+)-(\d+)(?:[-.](\d{1,2})(?!\d))?/

const ONE_MILLION_CONTEXT = '[1m]'

function capitalise(word: string): string {
  return word.charAt(0).toUpperCase() + word.slice(1)
}

export function formatModelName(model: string): string {
  const contextSuffix = model.endsWith(ONE_MILLION_CONTEXT) ? ' (1M)' : ''
  const [, family, major, minor] = MODEL_ID.exec(model) ?? []

  if (family !== undefined && major !== undefined) {
    const version = minor === undefined ? major : `${major}.${minor}`

    return `${capitalise(family)} ${version}${contextSuffix}`
  }

  const isAlias = /^[a-z]+$/.test(model)

  return isAlias ? capitalise(model) : model
}

function formatEffort(effort: ModelAndEffort['effort']): string | null {
  if (effort === null) {
    return null
  }

  return typeof effort === 'number' ? `${effort} thinking tokens` : `${effort} effort`
}

export function describeModelAndEffort(current: ModelAndEffort): string {
  const parts = [formatModelName(current.model), formatEffort(current.effort)]

  return parts.filter(part => part !== null).join(SEPARATOR)
}

// The terminal already puts a space between the hint and its tail.
const LEADING_MARK = '· '

export function appendToTail(existingTail: string | undefined, text: string): string {
  const hasExistingTail = existingTail !== undefined && existingTail !== ''

  return hasExistingTail ? `${existingTail}${SEPARATOR}${text}` : `${LEADING_MARK}${text}`
}
