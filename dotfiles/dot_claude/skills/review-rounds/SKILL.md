---
name: review-rounds
description: "Use when the user asks for a deep or thorough code review pass, a review that runs until it stops finding things, review rounds, a multi-round or multi-agent review, or a pre-merge audit of a feature. Also use when they ask to review a diff, branch, PR or recent commits with more rigour than a single read — including phrases like 'go over this in phases', 'keep going until nothing new turns up', 'review until clean', or 'run a code review agent pass'. Covers dispatching scoped reviewer agents, triaging their findings, verifying claims before acting, mutation-testing assertions, and the two-consecutive-clean-rounds stopping gate. Not for a quick sanity read of a small diff."
user-invocable: true
---

Runs a code review to a stopping condition rather than to a single pass. The
method exists because the naive version fails in three specific ways: reviewers
report defects that were already fixed, reviewers are sometimes wrong, and
fixes introduce new defects at roughly the rate the original code did.

## The gate

Run rounds until **two consecutive rounds find nothing worth actioning**.

- A round that finds something resets the count. Two clean rounds means two
  clean rounds *after the last fix*, not two clean rounds total.
- "Nothing worth actioning" is a judgement, not a vote count. A round reporting
  only style preferences and speculative hardening is clean.
- Tell the user which round you are on and what reset the count. If they asked
  for the gate, they will want to know it has not been met.

**Expect the later rounds to find defects in the earlier rounds' fixes.** This
is the normal shape, not a sign something has gone wrong. From round 3 or so,
point reviewers at the fix commits (`git diff HEAD~N..HEAD`) rather than at the
original feature — that is the least-reviewed code in the tree, and it is where
the findings actually are.

Stop early only if the user says so. If you stop before the gate is met, say
plainly that it was not met and why you are stopping anyway.

## Dispatching reviewers

Scope each agent to a **slice**, not to "the diff": store/data layer, HTTP and
authorization, frontend, tests, one subsystem. Three or four scoped reviewers
beat one broad one, and they can run in parallel.

Each brief must carry:

- The **exact diff range** and the files in scope.
- The **domain invariants**, written as things to verify rather than facts to
  assume ("X must never reach Y" not "X never reaches Y").
- The instruction to **read current files, not just the diff**.
- The instruction to **trace every finding to a concrete failure**: specific
  input or interaction, specific wrong output. Anything that cannot be
  substantiated that way is discarded.
- An explicit **"nothing found" is the expected and most useful answer** — do
  not pad. Without this, reviewers manufacture findings to look productive.
- A list of **already-fixed items** by name, so they do not re-report them.
- **Reply with findings in your final message**, under a character limit, no
  "what's right" section. Otherwise reports arrive truncated with the findings
  cut off, or padded with pages of verified-clean prose.

Reviewers commonly go idle without delivering. Message them to collect the
report rather than assuming they found nothing.

## Verify before acting

Reviewers review a moving tree. **Re-check every claim against the current
file before you act on it.** In practice a meaningful fraction of findings are
already fixed, and some are simply wrong.

When two reviewers contradict each other, compute the answer yourself. When a
reviewer's *diagnosis* is wrong but they have noticed a real inconsistency,
fix the inconsistency the right way rather than the way they proposed — a
reviewer saying "this fix was reverted" may actually be seeing an intentional
change with a stale comment above it.

Do not report a fix you have not verified. For behavioural fixes, write the
failing test first, then fix, then confirm it passes. For anything subtle,
revert the fix and confirm the test goes red.

## The finding classes that actually recur

Ranked by how often they turn up and how badly they hide.

### 1. Tests that cannot fail

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

**Find these by mutation.** Delete or invert the code the test covers and
confirm the suite goes red. If it stays green, the test is decoration. This is
the single highest-yield technique in the whole method and it is cheap against
one file.

### 2. Comment and copy drift after a behaviour change

A change alters what a term means; the surrounding comments, docs and UI copy
keep asserting the old meaning. The real damage is downstream: **someone
implements the comment.** Check every doc, struct comment and bit of user-facing
copy that describes behaviour the diff changed, and check whether any consumer
has coded against the stale description.

### 3. Migrations

- **`ADD CONSTRAINT CHECK` validates existing rows.** A constraint with no
  preceding clean-up fails, rolls back and blocks the deploy on precisely the
  databases holding the data it exists to prevent — and nowhere else, so it
  passes everywhere you test it.
- **Destructive clean-ups must record what they destroyed**, with ids, and the
  record must cover *every* branch of the clean-up. Verify the branch the
  migration exists for is actually included; it is often the one omitted,
  because its rows do not appear in the obvious buckets.
- **Backfills must not fabricate.** Prefer NULL, where the column has a defined
  "unknown", over a clamped or borrowed value that looks plausible. Check the
  backfill's own claim to be "invisible on the numbers" against the edge cases.
- Down must be correct, and it usually cannot undo data loss — say so.

### 4. Guards that bound the wrong thing

Bounding two factors independently when the invariant is on their **product**.
Any such pair either permits the pathological combination or forbids ordinary
data, and often both at once. Also: check every ceiling against *real* data for
each variant of the thing being bounded — a limit that is absurd for one unit
may be ordinary for another.

### 5. Error and recovery dead ends

Clearing state on failure removes the controls that would retry. Check every
recovery path leads somewhere recoverable, including the *second* failure —
the intended recovery move often routes back to the query that just failed.

### 6. Leaks through secondary projections

A sensitive field added to one query leaks through every sibling path that
shares the type: child lists, ancestor chains, barcode or lookup resolution,
batch replays. When a field gains a gate, sweep every projection of that type
and add one test asserting the invariant across all of them, rather than one
test per instance.

### 7. Audit and logging that records nothing

`before, _ := Get(...)` keeps the **zero value** on failure and logs it as a
real row of empty fields — indistinguishable from a row that genuinely said so.
Read-before-mutate must actually read before the mutation, from a projection
that carries the fields the entry exists to record.

## Triage

Fix / defer / reject, and say which:

- **Fix** anything with a concrete failure path, however narrow, if the fix is
  proportionate. Silent data loss, a wrong number a human will act on, and a
  low-privilege user breaking a higher-privilege surface all rank above
  cosmetic correctness.
- **Defer** with a one-line reason the user can overrule.
- **Reject** what you have verified is wrong, and say what you computed.

Commit each coherent fix as it lands, with a message saying what the defect was
and how it would have bitten — not just what changed. If several fixes share a
test file and cannot be split without a commit that fails its own tests, make
one commit and describe all of it rather than splitting badly or writing a
message that covers only part of the work.

## Reporting

Give the user, per round: what was found, what you fixed, what you rejected and
why, and whether the gate has been met. Distinguish defects in the original
work from defects in your own fixes — the ratio is the signal for whether to
keep going.
