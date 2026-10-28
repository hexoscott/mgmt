# Mutation

Read by mutation reviewers, drain verifiers, and the main agent's
self-check. Every test gap a mutation pass misses comes back later, one per
round.

## Enumerate, don't sample

Write the mutant list to `<scratchpad>/review/mutants-<stack>.md` before
running anything, taken from the production diff in scope:

- every guard and branch: invert it, or delete it;
- every WHERE or filter conjunct: drop it (tenant, deleted_at, status, the
  parent id);
- every status or enum list: drop each member in turn, and add each status
  that is absent;
- every field a payload, projection or update sends: drop it, or swap it with
  a sibling field;
- every lock: weaken it, or remove it;
- every text classifier (regex, error wording, keyword list): feed each known
  sample of every other class through it, both directions;
- plus the **gate matrix**: for every route or handler the scope touches, each
  role check, module switch and tenant filter on it, whether or not its tests
  changed.

Run the relevant tests per mutant. The report lists every mutant as red,
survived, or equivalent (argued in one line). Lines outside this list are out
of target. A late exhaustive sweep once found 20 survivors that sampled rounds
had been finding one at a time.

## Making red mean something

- A test only counts as red when it fails for the reason it exists.
  `[build failed]` and Go's "no tests to run" both mean the check never ran.
- Fixtures must tell mutants apart: distinct counts per category (not 1 held,
  1 cancelled, 1 complete), and ids that differ across tables so a join on the
  wrong id can't pass by coincidence.
- Run the suite before dispatch. A suite already red at dispatch gets fixed
  first, or every reviewer reports it.

## Keeping the tree safe

- Spawn mutation reviewers with `isolation: "worktree"`, and commit first,
  because the worktree is built from HEAD. A mutation reviewer that shares
  your tree can restore over your edits.
- Undo a mutation by copying the file aside and back. `git checkout` and
  `git stash` on a file also discard the uncommitted work it holds.
