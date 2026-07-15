# Global preferences

## Tools
- Prefer `rg` (ripgrep) over `grep`.
- `wt` is [worktrunk](https://github.com/max-sixty/worktrunk), aliased for managing git worktrees — use it when juggling parallel branches or isolating work.

## Languages
- **Go** is the first-class language — default to it for services, CLIs, and anything non-trivial.
- **Python** is secondary: small scripts, or projects where the ecosystem wins (ML, data, scientific libs).
- **TypeScript + React** for UI work — lean on the ecosystem rather than reinventing.

## UI
- Use [shadcn/ui](https://ui.shadcn.com/) components for anything that you can as a preference.

## Architecture
- Favour hexagonal / clean architecture with a ports-and-adapters style. Keep domain logic independent of frameworks, DBs, and transports; adapters plug in at the edges.
- TDD is to be used to improve code maintenance and find edge cases/bugs early.

## Code Approach
- You should use TDD style approach to coding in all cases unless there is a worth exception at which point it should be flagged to me.

## Bugs
- When a bug is identified a test should be written showing the failure state first before the fix is in place.  Feel free to use a stash and re-apply to show cleanly that the code fix does indeed rectify the issue.

## Data
- SQLite is the default datastore for small apps. Reach for something else only when there's a real reason.
- PostGres is the larger database of choice by default unless another technology makes more sense, then flag it.

## Testing
- Write tests alongside new code. Even when not doing strict TDD, design code to be testable (dependency injection, pure functions at the core, adapters at the edges).
- Try as best as possible to create integration tests that talk to real databases both locally and in CI.

## Documentation
- Code architecture and patterns etc. should be documented in the Readme.md of any codebase, especially when changes are made that need to be documented there.
- Pertinent information for AI agents that is too detailed for a human to reasonably read should be in an ai.md file linked to from the Readme.md.
- If there is an ai.md in a repo then it should be read into context to better understand the codebase being worked on.

## Response style
- No preamble ("Great question!", "Sure thing!"). End-of-turn recaps are fine and wanted.
- No hedging ("I think", "it seems", "perhaps") unless genuinely uncertain.
- Bullets over paragraphs for anything list-shaped.
- Code over prose when a snippet answers the question.
- One-line tool narration, not a paragraph.
- Don't volunteer next steps unless asked — ask instead.
- Answer the question asked, not adjacent ones.
- Feel free to constructively criticise my suggestions, do not assume I'm right.
