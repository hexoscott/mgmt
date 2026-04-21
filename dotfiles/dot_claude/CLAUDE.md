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
