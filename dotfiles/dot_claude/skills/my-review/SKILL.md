---
name: my-review
description: Review a diff, commit, branch, PR, or uncommitted changes in one bounded pass. Prioritize verified bugs and security failures, then check documented standards and the originating spec. Use for ordinary code review or explicitly as the first pass of review-rounds.
---

# My review

Review once, report actionable findings, stop. Read-only unless the user also
asked for fixes. Do not invoke review-rounds, create commits, post PR comments,
or start a confirmation loop. No mandatory agents or coverage matrices.

## 1. Pin the scope

Use the caller's explicit scope; when invoked by review-rounds, inherit its
exact scope and invariants rather than selecting a new baseline.

- No argument: `git status --short`, `git diff`, `git diff --cached`, plus
  relevant untracked source files. Do not open secrets or generated artifacts.
- Commit: resolve it, then `git show <commit>`; review that commit only.
- Branch, tag, or base ref: resolve it, then `git diff <base>...HEAD` and
  `git log <base>..HEAD --oneline`. A supplied explicit range stays that range.
- PR URL/number: `gh pr view <pr>` and `gh pr diff <pr>`, including its body
  and linked requirements. Read files at the PR head, not an unrelated checkout.

Record the resolved revision(s), diff command, and changed files. Invalid refs
stop the review with an explanation; an empty scope needs no review. Treat
user-supplied refs as quoted arguments, never executable shell text. If the
tree moves while reviewing, state which snapshot was reviewed.

## 2. Gather context

Read changed files in full, then relevant callers, shared helpers, tests, and
trust boundaries. Existing code is context: report a pre-existing defect only
when this change makes it reachable or worse, explaining the connection.

Read applicable AGENTS.md/CLAUDE.md, CONVENTIONS.md, CODING_STANDARDS.md,
CONTRIBUTING.md, and local configuration. Repo rules override generic advice.
Find requirements in the user's request, PR/issue, supplied spec, or matching
docs. If none exists or it cannot be fetched, say so and continue; do not
require tracker setup or invent requirements.

## 3. Review through three lenses

**Correctness and security first.** Check guards, null/empty inputs, error
propagation, state transitions, races, API compatibility, and data integrity.
Trace hostile input through validation, authorization, storage, networking,
rendering, and logging. Check tenant isolation and fail-closed behavior.
Flag performance only with a credible workload: unbounded quadratic work,
N+1 queries, or blocking I/O on a hot path.

**Standards.** Cite actual repo rules and skip checks tooling already enforces.
Use these Fowler smells as judgement calls, not automatic refactor orders:
unclear names, duplication, feature envy, data clumps, primitive obsession,
repeated switches, shotgun surgery, divergent change, speculative generality,
message chains, middle men, and refused bequest. Report only when a concrete
maintenance burden outweighs the added abstraction; prefer the smallest fix.

**Spec.** Compare each relevant requirement with observable behavior: missing
or partial implementation, wrong behavior, and unsolicited scope. Cite the
requirement. Check that tests exercise public behavior with independent expected
results, rather than restating implementation or only asserting mock calls.
A missing test alone is not proof of a bug; explain the uncovered risk.

Keep Standards and Spec verdicts distinct so a clean result on one cannot hide
a failure on the other. For a large diff, independent reviewers may split these
lenses in parallel; use only available delegation tools and do not recursively
delegate. Otherwise do the same checks locally.

## 4. Verify before reporting

For each candidate, identify the specific input/interleaving, affected caller,
and wrong result. Check surrounding code and existing patterns before calling
it a defect. Use focused tests or a reproduction when useful and safe; report
what actually ran. For security, identify attacker control, missing boundary
check, and concrete impact. Unverified suspicions belong in a short uncertainty
note, not the confirmed findings.

Merge duplicate causes, enumerate relevant sibling instances in scope, and
suggest the smallest fix. Avoid unrelated cleanup, hypothetical hardening,
style preferences, flattery, and findings padded to meet a quota.

## 5. Report and stop

Lead with confirmed bugs, highest severity first. Each finding needs a concise
title, severity, `file:line`, triggering scenario, impact, and fix direction.
Calibrate severity to the actual conditions; separate blocking defects from
test gaps and optional maintenance suggestions.

Then give brief **Standards** and **Spec** verdicts with any distinct findings
and cited rules/requirements. Report each finding once, referencing its ID
across lenses if needed. End with checks run, unavailable context, and limitations.
If nothing actionable is found, say so without claiming the code is proven safe.

When called by review-rounds, return the findings and coverage limits to its
ledger for triage. This pass is not its confirmation gate. Stop after this
report; fixes and verification belong to the caller's workflow.

## Sources

Synthesized primarily from [Vercel code-review](https://github.com/vercel-labs/open-agents/blob/main/.agents/skills/code-review/SKILL.md),
with the separate Standards/Spec lenses and smell heuristics from
[Matt Pocock code-review](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md)
and behavior-focused tests from [his TDD guidance](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/tests.md).
Self-contained: these are attribution links, not runtime dependencies.
