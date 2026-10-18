---
name: pre-commit-review
description: "Use before proposing or making a commit of a non-trivial batch of work, or when the user asks for a pre-commit check. One self-review pass over the uncommitted changes: tests mutation-checked, lock changes checked both ways, comments checked against code, one fresh-context reviewer. Lighter than review-rounds."
user-invocable: true
---

One pass over the batch before it is committed, aimed at the defect classes
that review rounds keep finding after the fact: tests that cannot fail, lock
changes checked in only one direction, and comments that describe code that
isn't there. It is a single pass with no gate; a pre-merge audit or "review
until clean" is `review-rounds`.

The batch is everything uncommitted: `git diff`, `git diff --cached` and
untracked files. A batch with no behaviour change and no new claim about
behaviour (a typo, a rename) is trivial: say so and skip to committing.

## 1. Mutate every new or changed test

For each test the batch adds or changes, break the code it covers (delete the
branch, invert the guard, drop the filter, skip the call) and run that test.
A test is _red_ when it fails for the reason it exists. A test that stays
green is decoration: change the fixture or the assertion until the mutation
turns it red. Prefer the mutation a real regression would make, such as the
filter a hurried edit would drop or the case a refactor would merge.

- Undo a mutation by copying the file aside to the scratchpad first and
  copying it back. Leave `git checkout` and `git stash` alone on any file that
  holds uncommitted work: they discard the batch along with the mutation.
- `[build failed]` is not red. Make the mutation compile (`_ = unused`) and
  rerun.

Done when every new or changed test has gone red under at least one mutation.

## 2. Check every lock change both ways

For each lock the batch adds, removes or changes in strength (row locks,
advisory locks, transaction boundaries, the order locks are taken in), list
every other path that touches the same rows or takes the same lock, and give
each path two verdicts:

- **Deadlock**: can that path hold something this one waits for while it
  waits for something this one holds? Foreign-key checks take `FOR KEY SHARE`
  on the referenced row, so an insert counts as a lock on its parent.
- **Stale read**: does a writer that used to wait now go ahead and read data
  that is uncommitted or about to change?

A weakened lock usually reopens a stale read; a stronger or reordered one
usually risks a deadlock. Done when every path has both verdicts written down.
Where an interleaving is in doubt, prove it with transactions sequenced on
`pg_stat_activity` (hold one side open, wait until the other is blocked,
continue), in a scratch test file that is deleted afterwards.

## 3. Check every claim

For each new or changed comment, doc line and commit-message sentence that
says what code does, read the code it describes and confirm it is true now.
Weigh absolute words hardest: _every_, _never_, _only_, _all_, _always_. They
are the claims most often false by one exception. When the batch changes
what a term means (a unit, a cap, a status), grep the term repo-wide (README,
docs, migrations, UI copy) and check every sentence stating the old meaning.
Done when each claim is confirmed or corrected and each changed term is
grepped.

## 4. One fresh-context reviewer

Dispatch one reviewer agent on the batch's diff. Its brief carries:

- the diff command and the files in scope;
- the domain invariants, written as things to verify ("X must never reach Y");
- read the current files, not just the diff;
- trace each finding to a concrete failure (specific input or interleaving,
  specific wrong result), discarding what can't be;
- "nothing found" is the expected and most useful answer;
- findings only in the final message, under 2000 characters.

Re-check each finding against the current code before acting on it; reviewers
are sometimes wrong. Skip this step for a batch under about 50 changed lines
with no behaviour change.

## 5. Fix and report

A fix is new code: re-run steps 1 to 3 on what each fix touches. Then report
to the user, in a few lines, what each step found and fixed, and anything
skipped or deferred with its reason.

The batch is ready to commit when every step is done and every finding is
fixed or deferred with a reason the user can overrule.
