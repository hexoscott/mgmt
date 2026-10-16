---
name: review-rounds
description: "Use when the user asks for a deep or thorough code review, review rounds, a review that runs until clean or until nothing new turns up, a multi-agent review, or a pre-merge audit of a feature, diff, branch, PR or recent commits. Covers the wide first sweep, scoped reviewer briefs, class-wide fixes, self-checking fixes before the next round, and the two-clean-rounds gate. Not for a quick sanity read of a small diff; one pass before a commit is `pre-commit-review`."
user-invocable: true
---

Runs a code review to a stopping condition. Each round costs a reviewer
dispatch, a wait and a triage, so the run is fast when every round finds
everything it can and every fix arrives already checked. Past runs went 13 to
100+ rounds for three reasons this method removes:

- reviewers capped their reports and handed back a few findings each;
- fixes landed one instance at a time and unchecked, so the next round's yield
  was defects in the last round's fixes;
- open-ended sweeps (every unguarded line) always found one more thing, so the
  gate never closed.

## The gate

Two consecutive rounds with no **blocking** finding, counted after the last
blocking fix.

- **Blocking**: a concrete failure path: a specific input or interleaving
  that gives a specific wrong result. Covers a wrong number a human acts on, a
  tenant or permission leak, data loss, a crash, a migration that fails on
  real data, a test that cannot fail on an invariant in the brief, and a
  comment, doc or copy claim the code contradicts.
- **Minor**: everything else, including hardening, style, an untested line
  that no brief invariant depends on, and wording that is true but could be
  clearer. Fix minors in the same batch or defer them. They never reset the
  count.

Report the round number, the blocking count and what reset the gate. Stop early
only if the user says so; if you stop before the gate is met, say so plainly
and why.

## Round 1: the wide sweep

Dispatch every reviewer in one message so they run in parallel:

- **Slice reviewers**, 3 to 5: one per slice (store/data layer, HTTP and
  authorization, frontend, migrations, one subsystem).
- **One mutation reviewer**: every test the scope adds or changes, plus at
  least one test per brief invariant. See [Mutation](#mutation).
- **One claims reviewer**: every comment, doc line, UI string and commit
  message sentence in scope that says what code does, checked against the code.

## Briefs

Each brief carries:

- the exact diff range and the files in scope;
- the domain invariants, written as things to verify ("X must never reach Y");
- read the current files, not just the diff;
- read `~/.claude/skills/review-rounds/finding-classes.md` and apply every
  class to the slice. Done when every file in the slice is read and every class
  applied, not at the first few findings;
- trace each finding to a concrete failure, discarding what can't be, and mark
  it blocking or minor using the gate's definitions (paste them in);
- **write every finding to `<scratchpad>/review/round-<N>-<slice>.md`**, one
  entry each with severity, `file:line`, the failure, and the fix. There is no
  cap on count and no "what's right" section. The final message gives the path
  and the blocking/minor counts;
- "nothing found" is a valid answer, and a padded finding costs a verification;
- the items already fixed, deferred or rejected, so they aren't re-reported;
- read-only: write nothing outside the scratchpad.

A reviewer that goes idle without writing its file has not finished. Message it
to collect the report.

## Triage and fix

Start on each reviewer's file as it lands rather than waiting for the slowest.

1. **Verify** every claim against the current file. Reviewers review a moving
   tree, and some are simply wrong. Reject with what you computed. When two
   reviewers contradict each other, compute the answer yourself. When a
   diagnosis is wrong but the inconsistency is real, fix it the right way.
2. **Fix the class, not the instance.** For each confirmed finding, search the
   whole scope for the same pattern (the term, the type, the query shape, every
   sibling projection, every comment describing the same rule) and fix every
   instance in one change. A single-instance fix leaves the siblings for
   the next round to find, one per round.
3. **Test-first**: write a failing test, fix, see green. For anything subtle,
   revert the fix and watch the test go red.
4. **Self-check the batch** before the next round: run `pre-commit-review`
   steps 1 to 3 on the fixes (mutate each new or changed test, check lock
   changes both ways, check every claim). This catches defects in your own
   fixes inside this round instead of costing the next one.
5. **Commit** each coherent fix with a message saying what the defect was and
   how it would have bitten. If fixes share a test file and can't be split
   without a commit that fails its own tests, make one commit and describe all
   of it.

## Round 2 onward

**Fix rounds** cover only what changed: `git diff <last-round-sha>..HEAD`
plus the callers of every symbol it touches. Dispatch one reviewer on that diff
and one mutation reviewer on the tests it touched. That is the least-reviewed
code in the tree, and it is where the findings are.

When a fix round has no blocking finding, run a **confirmation round**: one
fresh reviewer over the full original scope, with the full brief. If it is also
clean, that makes two consecutive clean rounds and the gate is met. A blocking
finding goes back to triage and the next round is a fix round.

## Convergence check

At round 5, and every 5 rounds after, if the gate is not met, report the
blocking count per round, split between original work and your own fixes, and
ask the user whether to continue. Bring the diagnosis with it:

- **Fix defects dominate**: the self-check is shallow or being skipped. Tighten
  step 4 rather than running more rounds.
- **New defects in the original work after round 3**: round 1 under-covered
  something. Run one more wide sweep, briefed on the classes that keep turning
  up.
- **The same class keeps recurring**: its instances are being fixed one at a
  time. Sweep the class once across the whole scope.

## Mutation

- The target is bounded: tests the scope adds or changes, and the tests behind
  each brief invariant. An unmutated line outside that target is a minor
  finding. The bound is what lets the gate close.
- Spawn the mutation reviewer with `isolation: "worktree"`, and commit first,
  because the worktree is built from HEAD. A mutation reviewer that shares
  your tree can restore over your edits.
- Undo a mutation by copying the file aside and back. `git checkout` and
  `git stash` on a file also discard the uncommitted work it holds.
- A test only counts as red when it fails for the reason it exists.
  `[build failed]` and Go's "no tests to run" both mean the check never ran.

## Reporting

Per round: blocking and minor counts, what you fixed, what you rejected and
why, what you deferred and the reason, and the gate state. Separate defects in
the original work from defects in your own fixes. That ratio is the signal for
whether to keep going.
