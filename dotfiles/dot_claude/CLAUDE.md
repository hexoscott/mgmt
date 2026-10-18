# Global preferences

Be extremely concise.  Sacrifice grammar for the sake of concision.

Construvtively criticise and challenge my ideas, do not assume I am correct.

## Main rules
- Favour code clarity over documentation or comments - write code that is easy to interpret by AI and humans later without needing supplementary documentation.
- Things that should live in docs: architectural decisions and what alternatives were considered, domain language to understand concepts in the code (captured as a glossary), a general layout document explaining what lives where in the codebase to speed up spelunking and onboarding.
- Prefer clarity over terseness - don't use clever or cute code. 
- Favour hexagonal or ports and adapters architecture - write code like a top level senior developer would.
- Use TDD in the frontend and backend.
- Run the `pre-commit-review` skill and fix what it finds before considering work done; a trivial change with no behaviour change skips it.
- Keep code formatted and cleanly organised so that it can be parsed easily later.

## Tools
- Taskfile and task instead of makefile.
- Prefer `rg` (ripgrep) over `grep`.
- `wt` is [worktrunk](https://github.com/max-sixty/worktrunk), aliased for managing git worktrees — use it when juggling parallel branches or isolating work.
- Browser automation: use [brw](https://brw.donworks.co.uk/) via the `brw` MCP tools (`mcp__brw__*`, see the `brw` skill). Never claude-in-chrome — it's uninstalled.
