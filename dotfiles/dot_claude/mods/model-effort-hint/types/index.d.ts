export type Effort = string | number

export type ModelAndEffort = { model: string; effort: Effort | null }

declare module 'claude-code' {
  interface PluginState {
    'model-effort-hint': { current: Shaped<ModelAndEffort | null> }
  }
}
