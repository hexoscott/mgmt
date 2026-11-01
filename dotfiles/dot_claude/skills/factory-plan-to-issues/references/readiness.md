# Planning ledger and readiness pass

Use one ledger, `plan.json`, alongside the spec and issue briefs. It describes
declared contracts and execution order, not a second copy of the spec. Build it
before long briefs; reconcile it after scope, contract or dependency changes.

## Ledger

```json
{
  "baseline": {
    "tenant-store": "Existing scoped store at abc123; cite source and isolation test"
  },
  "requirements": ["R-CI", "R-EXPORT"],
  "issues": [
    {
      "id": "CI",
      "owns": ["R-CI"],
      "provides": ["required-pr-checks"],
      "protects": ["EXPORT"]
    },
    {
      "id": "EXPORT",
      "blocked_by": ["CI"],
      "owns": ["R-EXPORT"],
      "requires": ["tenant-store", "required-pr-checks"],
      "provides": ["streamed-csv"]
    }
  ]
}
```

- `baseline`: capability ID → concrete evidence that the contract already holds.
- `requirements`: all atomic obligation IDs in the approved scope. Keep source-story
  mapping and final integration verifiers in the spec/briefs when splitting stories.
- Each issue needs an `id`. All list fields default to empty lists.
  Human/investigation gates use the same graph identities; their bodies
  state who resolves them and keep them outside the implementation queue.
- `owns`: obligations this ticket can actually deliver, each with one owner.
- `provides` / `requires`: stable capability IDs, defined concretely in the bodies.
  A materially changed contract needs a distinct ID from its baseline predecessor.
  Inputs must come from baseline, this ticket, or its completed blocker ancestry.
- `protects`: issue IDs for work that must not execute before this gate completes.
  Check its intended coverage against the spec; leaving a protected issue out of
  this list must not silently evade the guard. Existing protection can instead be
  a baseline capability required by the relevant issues.

Run the skill's `scripts/check_plan.py` with Python 3.9+ and the ledger path. It
uses only the standard library and reads files without changing them:

```sh
python3 /path/to/factory-plan-to-issues/scripts/check_plan.py plans/effort/plan.json
```

It rejects unknown/cyclic dependencies, overlapping capability providers, missing
or duplicate requirement owners, missing producer ancestry and late protective
gates. Passing means only that the declared graph is internally consistent. It
cannot infer omitted inputs, judge scope/contract content or prove runtime fit.

## Planner's failure check

Test relevant promises against concrete failure sequences before review:

- For time, count, money, deletion and availability promises, identify the unit,
  boundary and responsible mechanism. Replay missed runs, retries, delayed events,
  concurrent changes and recovery. Count retention alone does not establish a time
  deadline; preserving the last good copy cannot silently override an expiry promise.
- Trace state transitions across producers and consumers, including help/UI that
  advertises an unavailable feature, closed/historical entities and access changes.
- At shared transaction/network/stream boundaries, compare commit/buffering rules,
  deadlines, cancellation, locks and pool occupancy. Check long readers against
  migration/deletion jobs, not only each operation's happy path.
- Name the deployed compatibility baseline. Do not impose or remove rolling-release
  requirements merely because an intermediate branch exists.

Resolve contradictions in the plan. Ask the user when the approved promises cannot
coexist without a consequential tradeoff; do not choose which promise to weaken.

## Independent readiness review

Dispatch one fresh-context reviewer after the planner's own pass. Supply the actual
request/recorded decisions, canonical spec, relevant baseline source, ledger and
briefs. Exclude the planner's self-assessment, suspected findings and proposed fixes.
Keep the reviewer read-only and inside the task's existing resource/permission scope;
do not delegate further or publish anything as part of this check.

The review must verify:

1. **Worker closure.** For each ticket, begin with its body and declared producer
   outputs. Can a worker finish without inventing decisions, fetching inaccessible
   context or implementing a sibling? Verify the actual consumed behaviour, not just
   matching capability names. A graph/table entry is not proof of delivery.
2. **Coverage.** Compare against approved source, including units and failure cases.
   Every obligation has one actual delivery owner; compound stories have explicit
   parts and a final verifier whose prerequisites supply them.
3. **Concurrency.** Enumerate pairs with neither in the other's ancestry. Check
   shared contracts, schema/migrations, generated files, caller changes and semantic
   side effects. For overlap, identify disjoint edits and a deterministic resolution,
   combine the work or add justified ordering. Shared filenames alone are insufficient.
4. **Gates and intermediate states.** Simulate the runnable frontier through the
   graph. Verify that CI, isolation, authorisation and other required protections
   precede the work they guard. Separate early bootstrap from later launch automation.
   Each merged state must satisfy its declared invariants; live activation and offline
   implementation may have different prerequisites.
5. **Failure consistency.** Challenge the cross-ticket promises above against source
   and acceptance scenarios. Later tests cannot repair missing earlier scope.

Return concrete blockers with affected IDs, source requirement, a failing scenario
and repair direction; discard suspicions without a specific failure. Report covered
areas and unavailable evidence. A clean pass is a valid outcome.

The planner verifies findings, repairs spec/ledger/briefs together and reruns the
checker. Ask the same reviewer to verify the repairs and affected neighbours; do not
restart the whole planning exercise. Unresolved blockers remain explicit holds and
propagate to their dependants. Do not call a set ready merely because review ran.
Report checker result, independent review coverage, ready/held issues, remaining
human decisions and unmeasured execution limits. Publishing held drafts, when
authorised, does not authorise enqueueing them.
