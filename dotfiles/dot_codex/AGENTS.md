# Global preferences

## Main rules
- Favour code clarity over documentation or comments - write code that is easy to interpret by AI and humans later without needing supplementary documentation.
- Things that should live in docs: architectural decisions and what alternatives were considered, domain language to understand concepts in the code (captured as a glossary), a general layout document explaining what lives where in the codebase to speed up spelunking and onboarding.
- Prefer clarity over terseness - no cute functions that can't be reasoned about later - where that isn't possible use succint comments.
- Preferred stack is Go and Typescript with Python to supplement simple little things.
- React for the UI.
- Favour hexagonal or ports and adapters architecture - write code like a top level senior developer would.
- Use TDD to prove code on the backend and frontend.
- Keep Readme documents simple to understand - supplementary files can be linked to it where needed.
- Use Task instead of tools like makefiles - build/test/local dev commands live here.
- Keep code formatted and cleanly organised so that it can be parsed easily later.

## Tools
- Prefer `rg` (ripgrep) over `grep`.
- `wt` is [worktrunk](https://github.com/max-sixty/worktrunk), aliased for managing git worktrees — use it when juggling parallel branches or isolating work.
- Browser automation: use [brw](https://brw.donworks.co.uk/) via the `brw` MCP tools (`mcp__brw__*`, see the `brw` skill). Never claude-in-chrome — it's uninstalled.

## Response style
- No preamble ("Great question!", "Sure thing!"). End-of-turn recaps are fine and wanted.
- Keep responses clear but succint, don't waste tokens over explaining, I will ask for more detail where required.
- No hedging ("I think", "it seems", "perhaps") unless genuinely uncertain.
- Bullets over paragraphs for anything list-shaped.
- Code over prose when a snippet answers the question.
- One-line tool narration, not a paragraph.
- Don't volunteer next steps unless asked — ask instead.
- Answer the question asked, not adjacent ones.
- Feel free to constructively criticise my suggestions, do not assume I'm right.
