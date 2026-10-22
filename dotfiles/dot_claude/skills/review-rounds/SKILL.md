---
name: review-rounds
description: "Use when the user asks for a deep or thorough code review, review rounds, a review that runs until clean or until nothing new turns up, a multi-agent review, or a pre-merge audit of a feature, diff, branch, PR or recent commits. Covers the wide first sweep, scoped reviewer briefs, class-wide fixes, self-checking fixes before the next round, and the two-clean-rounds gate. Not for a quick sanity read of a small diff; one pass before a commit is `pre-commit-review`."
user-invocable: true
---

Runs a code review to a stopping condition. Each round costs a dispatch, a
wait and a triage, so the run is fast when round 1 finds everything it can
and every fix lands class-wide and already checked. Rounds pile up for these
reasons, which this method removes:

- test gaps on code that already behaves correctly reset the gate. Each fix's
  new code then gives the next reviewer new survivors to sample, so the gate
  never closes. In past runs this caused most resets after round 1;
- mutation is sampled by a reviewer instead of enumerated, so survivors of one
  class (one member of a status list, one filter of two sibling counts) come
  up one per round;
- a fix lands on one instance, and its siblings surface one per round;
- the main agent's own fixes carry new defects into the next round;
- the main agent makes a product decision, and the user reverses it rounds
  later;
- new work joins mid-run and gets fix-round treatment instead of a sweep;
- low-stakes findings (an old internal comment) reset the gate.

## The ledger

Keep `<scratchpad>/review/ledger.md` from the start: scope range, invariants,
changed terms, current round, rounds clean since the last blocking fix, the
round the next convergence check falls due, and every finding fixed, deferred
or rejected. Update it at the end of every round. After a context compaction,
re-read this skill and the ledger before the next dispatch.

## The gate

Two consecutive rounds with no **blocking** finding, counted after the last
blocking fix.

- **Blocking**: wrong behaviour now. A specific input or interleaving gives
  a specific wrong result: a wrong number a human acts on, a tenant or
  permission leak, data loss, a lost update, a crash, a migration that fails
  on real data. A false claim is blocking when someone would act on it
  wrongly: user-facing copy, README and API docs, and comments this scope
  added or changed.
- **Test gap**: the behaviour is right, but a mutant survives. It is blocking
  only on the gate matrix (role checks, module switches, tenant filters) or
  where the failure would lose data. Fix every other test gap in the batch and
  watch the test go red. These gaps never reset the count.
- **Minor**: everything else, including hardening, style, an unasserted
  message wording, a pre-existing internal comment, a comment in an
  already-applied migration, and wording whose conclusion still holds. Fix
  minors in the same batch or defer them. They never reset the count.
- A batch with no production-code change (only tests, comments or copy)
  doesn't reset the count and doesn't need a fix round. The self-check covers
  it.

## Round 1: the wide sweep

Before dispatch, write the brief's two lists into the ledger:

- **Invariants**, written as things to verify ("X must never reach Y").
- **Changed terms**: every word whose meaning the scope changes (a unit, a
  cap, "item", "per box", a status name). The claims reviewer greps each one
  repo-wide.

Then dispatch every reviewer in one message so they run in parallel:

- **Slice reviewers**, 3 to 5: one per slice (store/data layer, HTTP and
  authorization, frontend, migrations, one subsystem). Name the **sibling
  flows** (every screen or handler that shares a pattern with one in scope,
  such as receive, goods-in and produce) and give them to the same slice.
- **Mutation reviewers**, one per stack (backend, frontend), each in a
  worktree. They enumerate mutants mechanically from the scope's production
  code, not from its tests. See [Mutation](#mutation). This is the most
  important reviewer: every test gap it misses comes back later, one per
  round.
- **One claims reviewer**: every changed term grepped across the whole repo
  (README, docs, migrations, UI copy, comments outside the diff), plus every
  comment, doc line, UI string and commit message sentence in scope that says
  what code does, each checked against the code.

## Briefs

Each brief carries:

- the exact diff range and the files in scope;
- the invariants and changed terms from the ledger;
- read the current files, not just the diff;
- read `~/.claude/skills/review-rounds/finding-classes.md` and apply every
  class to the slice. Done when every file in the slice is read and every class
  applied, not at the first few findings;
- trace each finding to a concrete failure, discarding what can't be, and mark
  it blocking or minor using the gate's definitions (paste them in);
- **write every finding to `<scratchpad>/review/round-<N>-<slice>.md`**, one
  entry each with severity, `file:line`, the failure, the fix, and every
  sibling instance found. There is no cap on count and no "what's right"
  section. The final message gives the path and the blocking/minor counts;
- "nothing found" is a valid answer, and a padded finding costs a verification;
- the ledger's fixed, deferred and rejected items, so they aren't re-reported;
- read-only: write nothing outside the scratchpad.

A reviewer that goes idle without writing its file has not finished. Message it
to collect the report.

## Triage and fix

Start on each reviewer's file as it lands rather than waiting for the slowest.
Merge duplicate reports before fixing.

**Product decisions go to the user before any fix.** When a fix depends on
what should happen rather than on how to make it happen (whether a locked
item takes new work, whether a held job blocks its order), collect every such
finding from the round and ask the user in one message. Don't pick an answer
and flag it afterwards. A choice reversed later costs a scope change and
another wide sweep.

1. **Verify** every claim against the current file. Reviewers review a moving
   tree, and some are simply wrong. Reject with what you computed. When two
   reviewers contradict each other, compute the answer yourself. When a
   diagnosis is wrong but the inconsistency is real, fix it the right way.
2. **Fix the class, not the instance.** For each confirmed finding, list its
   siblings before writing the fix, then fix every one in one change:
   - a claim: grep its term repo-wide and fix every sentence stating the same
     rule;
   - a flow: apply the fix to every sibling flow;
   - a form or payload field: fix every field the same path sends (a stale
     form that re-sends one changed field re-sends them all);
   - a query, type or projection: every sibling query and projection.
3. **Test-first**: write a failing test, fix, see green. A test that was
   never seen red for its own reason cannot be trusted to fail. A test that
   cannot fail is what spawns most later rounds.
4. **Self-check the batch** before the next round. Mutate the fix's own
   production code the way the mutation reviewer would (every branch, every
   list member dropped and every absent status added, every field, every
   filter) and run the tests for each mutant. Then run `pre-commit-review`
   steps 2 and 3, and re-check each brief invariant against the fix itself (a
   new constraint or lock can break one). Fix-round reviewers used to find a
   survivor in the main agent's fixes almost every round; this step is what
   stops that. Done when every mutant is red or argued equivalent, every
   changed term is grepped, and every invariant holds.
5. **Commit** each coherent fix with a message saying what the defect was and
   how it would have bitten. If fixes share a test file and can't be split
   without a commit that fails its own tests, make one commit and describe all
   of it.

## Round 2 onward

**Fix rounds** run only after a batch that changed production code. They
cover only what changed: `git diff <last-round-sha>..HEAD` plus the callers
of every symbol it touches. Dispatch one reviewer, in a worktree, that both
reviews that diff and mutates it exhaustively. That is the least-reviewed
code in the tree, and it is where the findings are.

When a fix round has no blocking finding, run a **confirmation round**: one
fresh reviewer over the full scope, with the full brief. If it is also
clean, that makes two consecutive clean rounds and the gate is met. A blocking
finding goes back to triage and the next round is a fix round.

A test gap the confirmation round finds means round 1's mutation missed a
class. Sweep that class across the whole scope in the same batch (every
status list, every sibling count, every payload field), not just the instance
reported.

## New work mid-run

When the user adds work (a feature, a sweep, a follow-up), it is a new
**scope**, not a fix. Add its invariants and changed terms to the ledger and
run a round 1 wide sweep on it: slices including its sibling flows, mutation
with its gate matrix, claims. The gate resets and closes over the combined
scope.

## Convergence check

When the ledger says it is due (round 5, and every 5 rounds after) and the
gate is not met, stop and ask the user whether to continue. Report the
blocking count per round, split between original work and your own fixes,
with the diagnosis:

- **Fix defects dominate**: the self-check is shallow or being skipped. Tighten
  step 4 rather than running more rounds.
- **New defects in the original work after round 3**: round 1 under-covered
  something. Run one more wide sweep, briefed on the classes that keep turning
  up.
- **The same class keeps recurring**: its siblings are being fixed one at a
  time. Sweep the class once across the whole scope.

## Mutation

- **Enumerate, don't sample.** Write the mutant list to
  `<scratchpad>/review/mutants-<stack>.md` before running anything, taken
  from the scope's production diff:
  - every guard and branch: invert it, or delete it;
  - every WHERE or filter conjunct: drop it (tenant, deleted_at, status, the
    parent id);
  - every status or enum list: drop each member in turn, and add each status
    that is absent;
  - every field a payload, projection or update sends: drop it, or swap it
    with a sibling field;
  - every lock: weaken it, or remove it;
  - plus the **gate matrix**: for every route or handler the scope touches,
    each role check, module switch and tenant filter on it, whether or not its
    tests changed.

  Run the relevant tests per mutant. The report lists every mutant with red,
  survived, or equivalent (argued in one line). Lines outside this list are
  out of target. In past runs a late exhaustive sweep found 20 survivors that
  sampled rounds had been finding one at a time.
- Fixtures must be able to tell mutants apart: distinct counts per category
  (not 1 held, 1 cancelled, 1 complete), and ids that differ across tables so
  a join on the wrong id can't pass by coincidence.
- Spawn mutation reviewers with `isolation: "worktree"`, and commit first,
  because the worktree is built from HEAD. A mutation reviewer that shares
  your tree can restore over your edits.
- Undo a mutation by copying the file aside and back. `git checkout` and
  `git stash` on a file also discard the uncommitted work it holds.
- A test only counts as red when it fails for the reason it exists.
  `[build failed]` and Go's "no tests to run" both mean the check never ran.
- Run the suite before dispatch. A suite already red at dispatch gets fixed
  first, or every reviewer reports it.

## Reporting

Per round: blocking and minor counts, what you fixed, what you rejected and
why, what you deferred and the reason, and the gate state. Separate defects in
the original work from defects in your own fixes. That ratio is the signal for
whether to keep going. If you stop before the gate is met, say so plainly and
why.
