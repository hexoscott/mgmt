import { expect, test } from 'claude-code/testing'

import { describeModelAndEffort, formatModelName } from './describe'

test('model ids read as family and version', () => {
  expect(formatModelName('claude-opus-5-5')).toBe('Opus 5.5')
  expect(formatModelName('claude-opus-4-5-20251101')).toBe('Opus 4.5')
  expect(formatModelName('claude-sonnet-4-20250514')).toBe('Sonnet 4')
  expect(formatModelName('us.anthropic.claude-haiku-5-5-v1:0')).toBe('Haiku 5.5')
  expect(formatModelName('claude-opus-5-5[1m]')).toBe('Opus 5.5 (1M)')
})

test('gateway ids that write the version with a dot keep their minor version', () => {
  expect(formatModelName('anthropic/claude-sonnet-4.5')).toBe('Sonnet 4.5')
  expect(formatModelName('claude-opus-4.1')).toBe('Opus 4.1')
})

test('aliases are capitalised and unknown names kept as given', () => {
  expect(formatModelName('opus')).toBe('Opus')
  expect(formatModelName('some-gateway/model-x')).toBe('some-gateway/model-x')
})

test('effort is added when known', () => {
  expect(describeModelAndEffort({ model: 'claude-opus-5-5', effort: 'xhigh' })).toBe(
    'Opus 5.5 · xhigh effort',
  )
  expect(describeModelAndEffort({ model: 'claude-opus-5-5', effort: 8000 })).toBe(
    'Opus 5.5 · 8000 thinking tokens',
  )
  expect(describeModelAndEffort({ model: 'claude-opus-5-5', effort: null })).toBe('Opus 5.5')
})
