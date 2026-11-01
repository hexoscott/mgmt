# Issue contract

Each issue is an implementation brief, not a pointer to a conversation. Include
the relevant requirements and decisions in its body even when the full spec is
linked. Keep the spec authoritative for overall intent; when it changes, reconcile
the affected briefs. A worker should not need sibling comments to discover scope.

Use these fields, omitting only genuinely inapplicable detail:

```markdown
# <local key>: <capability or coherent change>

## Outcome and scope
What works when this issue is merged. Include owned requirement/decision IDs and
their relevant text. Link the spec for wider context.

## Ownership and exclusions
Responsibilities, shared contracts/symbols and migration changes owned here.
Name sibling-owned work explicitly; navigation paths are hints from <baseline>.
List provided capability IDs and their observable postconditions, matching plan.json.

## Inputs and dependencies
Existing capabilities with baseline evidence.
For each blocker: local key / real issue link, why it gates this work, and the
specific merged output/interface/invariant consumed. Mark merge-order-only edges.
Or state: no prerequisites beyond the baseline.
Separate context-only references from these execution dependencies.
List required capability IDs and their baseline evidence or named producers.
For a guard, list the work it protects and when that protection must already hold.

## Required behaviour and contracts
Enough domain rules, data/interface shapes and error semantics to implement
without designing a sibling's feature. Include compatibility and failure recovery.
Where operations cross transactions, network calls or streams, define resource
lifetimes, cancellation, response/commit behaviour and relevant capacity bounds.

## Acceptance and verification
- [ ] Observable positive scenario.
- [ ] Relevant failure/boundary scenario.
- [ ] Integration with the actual prerequisite output, where applicable.
Existing test seam and commands; implementation uses red-green-refactor.
Any checks requiring external infrastructure, and how they gate release.
Named integration-verification obligations where a source story spans producers.

## Concurrency and delivery
Safe concurrent work, overlapping symbols and the resolution rule, if any.
Migration/rollout/recovery obligations and external or human gates, if applicable.
```

Do not invent exact interfaces just to fill the template: resolve an important
missing contract in planning. Routine local design choices remain with the worker.
An explicit contract requirement belongs in the consuming issue, even if a producer
issue already describes it; this is intentional handoff context, not duplicate scope.
Keep the ledger and body consistent. Do not remove an acceptance criterion to make
a missing dependency disappear unless the reduced scope still meets the approved
requirement, with the remaining obligation explicitly owned elsewhere.

## Granularity example

For a single-site product becoming tenant-aware with subscriptions, a possible
grouping is:

| Issue | Owns | Blocked by |
| --- | --- | --- |
| Tenant ownership and isolation | Existing-data mapping, tenant identity and membership, scoped access through current entry points, isolation regressions | None, after migration decisions are settled |
| Tenant subscriptions | Billing account mapping, checkout, authenticated webhooks, idempotency/recovery, subscription state and billing management UI | Tenant ownership and isolation: stable tenant ID and billing-authorisation contract |
| Subscription entitlements | Agreed access policy across affected entry points, subscription transitions and failure cases | Tenant subscriptions: authoritative subscription-state contract |

This is an illustration, not a prescribed three-ticket migration. Combine
subscriptions and entitlements when they cannot be safe or useful independently.
Separate an extensive isolation migration only where compatible intermediate
states exist. Add independently needed capabilities according to the actual scope.

Avoid separate issues for a table, repository method, endpoint, webhook handler,
and tests when none can deliver the intended capability alone. Also avoid bundling
unrelated features merely to hit a low issue count.
