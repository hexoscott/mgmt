# Global preferences

## Tools
- Prefer `rg` (ripgrep) over `grep`.
- `wt` is [worktrunk](https://github.com/max-sixty/worktrunk), aliased for managing git worktrees — use it when juggling parallel branches or isolating work.

## Languages
- **Go** is the first-class language — default to it for services, CLIs, and anything non-trivial.
- **Python** is secondary: small scripts, or projects where the ecosystem wins (ML, data, scientific libs).
- **TypeScript + React** for UI work — lean on the ecosystem rather than reinventing.

## UI
- For non-flashy UI (tables, forms, data display, admin-style surfaces), use [shadcn/ui](https://ui.shadcn.com/) components.

## Architecture
- Favour hexagonal / clean architecture with a ports-and-adapters style. Keep domain logic independent of frameworks, DBs, and transports; adapters plug in at the edges.

## Data
- SQLite is the default datastore for small apps. Reach for something else only when there's a real reason.

## Testing
- Write tests alongside new code. Even when not doing strict TDD, design code to be testable (dependency injection, pure functions at the core, adapters at the edges).

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
