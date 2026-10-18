# Finding classes that recur

Ranked by how often they turn up and how badly they hide. A reviewer applies
every class to its slice; a class that does not apply is skipped silently.

## 1. Tests that cannot fail

The dominant class, and the one that lets everything else through. Variants:

- **The fixture could never produce the failure.** A leak assertion on a row
  where the leaked field was always null; a "not valued" assertion on a fixture
  where nothing was ever priced.
- **Asserting the absence of something absent anyway.** Checking no "£"
  renders, where the failing branch renders a skeleton that has no text at all.
- **Asserting on literals a format string always contains.** The message
  mentions every column name whatever it did, so the check passes for any
  record at all.
- **Passing for the wrong reason.** A 403 test using a principal that a
  different, unrelated gate would refuse anyway.
- **A wait that resolves too early.** Awaiting a static heading that renders
  during the loading state, then asserting synchronously on data that has not
  arrived. Passes alone, fails under full-suite load, on a different test each
  run.

Find these by mutation: delete or invert the code the test covers and confirm
the test goes red.

## 2. Comment and copy drift after a behaviour change

A change alters what a term means; the surrounding comments, docs and UI copy
keep asserting the old meaning. The real damage is downstream: someone
implements the comment. Check every doc, struct comment and bit of
user-facing copy that describes behaviour the diff changed, and whether any
consumer has coded against the stale description.

Rewording churns when one term carries two meanings (e.g. "lead time" ≥0 in
one comment, >0 in another). Report every comment describing the same rule
together, not just the one that is wrong, and weigh absolute words hardest:
_every_, _never_, _only_, _all_, _always_.

## 3. Migrations

- **`ADD CONSTRAINT CHECK` validates existing rows.** A constraint with no
  preceding clean-up fails, rolls back and blocks the deploy on precisely the
  databases holding the data it exists to prevent, and nowhere else, so it
  passes everywhere you test it.
- **Destructive clean-ups must record what they destroyed**, with ids, and the
  record must cover every branch of the clean-up. The branch the migration
  exists for is often the one omitted, because its rows do not appear in the
  obvious buckets.
- **Backfills must not fabricate.** Prefer NULL, where the column has a defined
  "unknown", over a clamped or borrowed value that looks plausible. Check the
  backfill's claim to be "invisible on the numbers" against the edge cases.
- Down must be correct, and it usually cannot undo data loss: say so.

## 4. Guards that bound the wrong thing

Bounding two factors independently when the invariant is on their product.
Any such pair either permits the pathological combination or forbids ordinary
data, often both. Check every ceiling against real data for each variant of
the thing being bounded: a limit absurd for one unit may be ordinary for
another.

## 5. Error and recovery dead ends

Clearing state on failure removes the controls that would retry. Check every
recovery path leads somewhere recoverable, including the second failure: the
intended recovery move often routes back to the query that just failed.

## 6. Leaks through secondary projections

A sensitive field added to one query leaks through every sibling path that
shares the type: child lists, ancestor chains, barcode or lookup resolution,
batch replays. When a field gains a gate, list every projection of that type,
not just the one in the diff.

## 7. Audit and logging that records nothing

`before, _ := Get(...)` keeps the zero value on failure and logs it as a real
row of empty fields, indistinguishable from a row that genuinely said so.
Read-before-mutate must actually read before the mutation, from a projection
that carries the fields the entry exists to record.

## 8. Lost updates from stale forms

A form loaded before another user's edit re-sends every field it holds, not
just the one the user touched, and overwrites the newer values. Fixing the
field the finding names leaves every other field in the payload to be found
one per round. Check every field the save path sends: send only changed
fields, or compare a version on write.

## 9. Sibling flows sharing a pattern

Two screens or handlers that do the same job (receive, goods-in, produce)
copy each other's patterns: a form lock, a double-tap guard, an async picker
that can resolve stale. A fix to one flow leaves the defect in the others.
Name every sibling flow and check each one for the pattern.
