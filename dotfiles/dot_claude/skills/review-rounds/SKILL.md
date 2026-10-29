---
name: review-rounds
description: "Use when the user asks for a deep or thorough code review, review rounds, a review that runs until clean or until nothing new turns up, a multi-agent review, or a pre-merge audit of a feature, diff, branch, PR or recent commits. Not for a quick sanity read of a small diff; one pass before a commit is `pre-commit-review`."
user-invocable: true
---

Runs a code review to a gate. Every round costs a dispatch, a wait and a
triage, so speed comes from each round finishing its own work: one review,
complete feedback, never **drip-fed** across rounds. A round is not closed
when the reviewers report; it is closed when its fixes are **drained** (a
fresh verifier finds nothing left in them) and its findings are fixed
class-wide. The next round exists to confirm, not to finish.

Rounds have piled up for these reasons:

- a reviewer samples instead of enumerating, so one class surfaces one member
  per round (survivors, sibling flows, error wordings);
- the main agent's own fixes carry new defects: state that is never cleared,
  starvation, a classifier that now over-matches. In one 19-round run more
  than half the blocking findings after round 6 were in fixes;
- a test gap, minor or comment fix earns its own round;
- a product decision is picked by the agent and reversed by the user later;
- a review the user wanted (standards, spec) runs after the gate as a second
  cycle.

## The ledger

Keep `<scratchpad>/review/ledger.md` from the start. Its top block is
overwritten every round: scope range, current round, gate state, next step.
Below it: invariants, changed terms, and every finding fixed, deferred or
rejected, then a one-line log per round. After a context compaction, re-read
this skill and the ledger before the next dispatch.

## Severity

- **Blocking**: wrong behaviour now. A specific input or interleaving gives a
  specific wrong result: a wrong number a human acts on, a tenant or
  permission leak, data loss, a lost update, a crash, a starved or stuck
  queue, a migration that fails on real data. A false claim is blocking when
  someone would act on it wrongly: user-facing copy, README and API docs, and
  comments this scope added or changed.
- **Test gap**: the behaviour is right, but a mutant survives. Blocking only
  on the gate matrix (role checks, module switches, tenant filters) or where
  the failure would lose data.
- **Minor**: everything else, including hardening, style, standards and smell
  findings, an unasserted message wording, a pre-existing internal comment, a
  comment in an already-applied migration, and wording whose conclusion still
  holds.

Test gaps and minors are fixed inside the round that found them, or deferred
with a reason. They never cost a round of their own.

## First pass: my-review

Before round 1's dispatch, resolve the scope and write the invariants and
changed terms into the ledger as described in step 1 below. Then read and run
[my-review](../my-review/SKILL.md) once over that exact scope. This is the first
review pass, before specialist reviewers or mutation work.

Record its findings and coverage limits in the ledger, triage them using step
3, and carry their dispositions into every reviewer brief. Apply authorized
fixes through step 4; unresolved findings stay open for round 1. Do not repeat
this pass for fixes, drains, or confirmation rounds. A new scope mid-run gets
its own first pass. A clean first pass does not satisfy the gate.

## A round

Every round runs the same five steps. Round 1 sweeps the whole scope; later
rounds are confirmations (see [The gate](#the-gate)).

### 1. Dispatch

Before round 1, write two lists into the ledger:

- **Invariants**, written as things to verify ("X must never reach Y").
- **Changed terms**: every word whose meaning the scope changes (a unit, a
  cap, "item", "per box", a status name).

Commit, run the suite (fix it first if red), then dispatch every reviewer in
one message so they run in parallel:

- **Slice reviewers**, 3 to 5 (`Code Reviewer` agent type where available):
  one per slice (store/data layer, HTTP and authorization, frontend,
  migrations, one subsystem). Name the **sibling flows** (every screen or
  handler that shares a pattern with one in scope, such as receive, goods-in
  and produce) and give them to the same slice.
- **Mutation reviewers**, one per stack, each with `isolation: "worktree"`,
  following [mutation.md](mutation.md). The most important reviewer: every
  survivor it misses comes back later, one per round.
- **Claims reviewer**: every changed term grepped across the whole repo
  (README, docs, migrations, UI copy, comments outside the diff), plus every
  comment, doc line, UI string and commit message sentence in scope that says
  what code does, each checked against the code.
- **Spec reviewer**, when an originating spec or issue exists (issue refs in
  commit messages, a path the user gave, a spec under `docs/` or `specs/`):
  what the spec asked for that is missing or partial, what the code does that
  wasn't asked for, and what looks implemented but wrong. Quote the spec line
  for each.
- **Standards reviewer**: every file in the repo that documents how code is
  written (`CLAUDE.md`, `AGENTS.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`),
  plus the Fowler smell baseline in [my-review](../my-review/SKILL.md),
  step 3. The repo's standard overrides the baseline; smells are
  judgement calls and always minor; skip what tooling enforces.
- **Codex adversarial reviewer**, round 1 only, when the codex plugin is
  installed: a challenge to the approach itself (design choices, assumptions,
  where it fails under real conditions), from a different model. Launch it
  with Bash `run_in_background: true` alongside the agents, passing the
  invariants as focus text:

  ```bash
  node "$(ls -d ~/.claude/plugins/cache/*/codex/*/ | tail -1)scripts/codex-companion.mjs" \
    adversarial-review --wait --base <scope-start> "<invariants>" \
    > <scratchpad>/review/round-1-codex.md 2>&1
  ```

  It follows its own format, not step 2's brief. Its findings mostly land as
  product decisions in triage step 2.

### 2. Brief

Each brief carries:

- the exact diff range and the files in scope; read the current files, not
  just the diff;
- the invariants, changed terms, and the ledger's fixed, deferred and rejected
  items, so they aren't re-reported;
- the severity definitions above, pasted in;
- read `~/.claude/skills/review-rounds/finding-classes.md` and apply every
  class, plus these lenses on every slice: correctness, security, error
  handling on critical paths, concurrency, API contracts, performance;
- trace each finding to a concrete failure, discarding what can't be;
- **write every finding to `<scratchpad>/review/round-<N>-<slice>.md`**: one
  entry each with severity, `file:line`, the failure, the fix, and every
  sibling instance. No cap on count, no praise, no "what's right" section.
  "Nothing found" is a valid answer, and a padded finding costs a
  verification;
- **self-verify before reporting done.** After the first pass, run a second:
  for each finding, sweep its class across the whole slice and list every
  sibling; then end the file with a **coverage table**: every file in the
  slice (read in full: yes/no) against every finding class and lens
  (finding / clean / not applicable). Done when the table has no blank cell;
- the final message gives the path and the blocking / test gap / minor counts;
- read-only: write nothing outside the scratchpad (mutation reviewers work in
  their own worktree).

A report with a blank cell in its coverage table, or a reviewer that goes idle
without writing its file, has not finished: message it to complete the table.

### 3. Triage

Start on each reviewer's file as it lands. Merge duplicates.

1. **Verify** every claim against the current file. Reviewers review a moving
   tree, and some are simply wrong. Reject with what you computed. When two
   reviewers contradict each other, compute the answer yourself. When a
   diagnosis is wrong but the inconsistency is real, fix it the right way.
2. **Product decisions go to the user before any fix.** When a fix depends on
   what should happen rather than on how (whether a locked item takes new
   work, whether a held job blocks its order), collect every such finding in
   the round and ask in one message. A choice the user reverses later costs a
   scope change and another wide sweep.

### 4. Fix

1. **Fix the class, not the instance.** List each finding's siblings before
   writing the fix, then fix every one in one change:
   - a claim: grep its term repo-wide and fix every sentence stating the same
     rule;
   - a flow: every sibling flow;
   - a form or payload field: every field the same path sends;
   - a query, type or projection: every sibling query and projection;
   - a class the ledger shows recurring a second time: **invert the default**
     so the class closes structurally (deny unless recognised, persist instead
     of remembering in memory) rather than adding its next member.
2. **Test-first**: write a failing test, fix, see it **red** then green, for
   the reason the test exists.
3. **Self-check** the batch:
   - mutate the fix's own production code per [mutation.md](mutation.md) and
     run the tests for each mutant;
   - check every comment in each function the fix touched, not only the lines
     it changed, and grep every term the fix changed;
   - re-check each invariant against the fix (a new constraint or lock can
     break one), and run `pre-commit-review` step 2 on any lock change;
   - **pre-mortem** each fix: write down the blocking finding the drain
     verifier is most likely to report against it, using classes 10 and 11
     of `finding-classes.md`, then check that it is false.
4. **Commit** each coherent fix with a message saying what the defect was and
   how it would have bitten. Fixes that share a test file and can't be split
   without a commit failing its own tests go in one commit that describes all
   of it.

### 5. Drain

Dispatch one fresh **drain verifier** with `isolation: "worktree"` over
`git diff <round-start>..HEAD` plus the callers of every symbol it touches.
Its brief is step 2's, scoped to that diff, with the mutation list and the
pre-mortems from step 4 attached for it to attack. That diff is the
least-reviewed code in the tree.

Anything it finds goes back to step 3 inside the same round, and a new
verifier drains the new fixes. Skip the drain for a batch with no
production-code change; the self-check covers it.

### Closing the round

The round is closed when every box is ticked in the ledger:

- [ ] every reviewer's coverage table is complete;
- [ ] every finding is fixed, deferred with a reason, or rejected with what
      you computed;
- [ ] every fix's siblings were listed and fixed;
- [ ] every new test was seen red for its own reason;
- [ ] every self-check mutant is red or argued equivalent;
- [ ] the last drain verifier reported no blocking finding and no test gap;
- [ ] every fix is committed.

## The gate

The gate is met by a **confirmation round** with no blocking finding, run
after a round that closed. A confirmation is one fresh reviewer over the full
scope with the full step 2 brief and coverage table, plus one mutation
reviewer over any class the ledger shows recurring.

- A blocking finding in the confirmation is fixed and drained in that round,
  and another confirmation follows.
- Test gaps and minors in the confirmation are fixed and drained in that
  round, and the gate holds unless that drain finds a blocking defect.
- A test gap the confirmation finds means round 1's mutation missed a class.
  Sweep that class across the whole scope in the same batch.

To save a wait, dispatch the confirmation alongside a round's last drain
verifier. It counts for the gate only if that drain needed no further
production change.

## New work mid-run

When the user adds work (a feature, a sweep, a follow-up), it is a new
**scope**, not a fix. Add its invariants and changed terms to the ledger and
run round 1 on it in full. The gate resets and closes over the combined scope.

## Convergence check

At round 5, and every 5 rounds after, with the gate not met, stop and ask the
user whether to continue. Report the blocking count per round, split between
original work and your own fixes, with the diagnosis:

- **Fix defects dominate**: the pre-mortems are shallow or the drain is being
  skipped. Tighten step 4.3 rather than running more rounds.
- **New defects in the original work after round 3**: round 1 under-covered
  something. Check the coverage tables for the gap, then run one more wide
  sweep briefed on the classes that keep turning up.
- **The same class keeps recurring**: invert the default.

## Reporting

Per round: blocking, test gap and minor counts; what you fixed, rejected (and
why) and deferred (and the reason); drain verifiers run; gate state. Separate
defects in the original work from defects in your own fixes. If you stop
before the gate is met, say so plainly and why.
