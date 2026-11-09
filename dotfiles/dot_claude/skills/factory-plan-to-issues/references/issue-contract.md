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

## Wave and inputs
Wave number. Every input is on the target branch before this issue is published:
existing capabilities, and merged outputs of earlier waves, each with evidence
(file, commit or merged PR) re-grounded when this wave is promoted.
List required capability IDs with that evidence.
Separate context-only references from these inputs.
For a guard, list the work it protects and when that protection must already hold.

## Required behaviour and contracts
Enough domain rules, data/interface shapes and error semantics to implement
without designing a sibling's feature. Include compatibility and failure recovery.
Where operations cross transactions, network calls or streams, define resource
lifetimes, cancellation, response/commit behaviour and relevant capacity bounds.

## Acceptance and verification
- [ ] Observable positive scenario.
- [ ] Relevant failure/boundary scenario.
- [ ] Integration with the actual merged output of an earlier wave, where applicable.
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
a missing input disappear unless the reduced scope still meets the approved
requirement, with the remaining obligation explicitly owned elsewhere.

## Granularity example

For a single-site product becoming tenant-aware with subscriptions, a possible
grouping is:

| Issue | Owns | Wave |
| --- | --- | --- |
| Tenant ownership and isolation | Existing-data mapping, tenant identity and membership, scoped access through current entry points, isolation regressions | 1, after migration decisions are settled |
| Plan catalogue and pricing page | Plan definitions, prices and the public pricing page, none tenant-scoped | 1 |
| Tenant subscriptions and entitlements | Billing account mapping, checkout, authenticated webhooks, idempotency/recovery, subscription state, billing management UI, and the access policy across affected entry points | 2: consumes the merged tenant ID, billing-authorisation contract and plan catalogue |

This is an illustration, not a prescribed migration. Subscriptions and
entitlements share one issue because entitlements consume the subscription-state
contract; splitting them would add a third wave. Separate an extensive isolation
migration only where compatible intermediate states exist. Add independently
needed capabilities according to the actual scope.

Avoid separate issues for a table, repository method, endpoint, webhook handler,
and tests when none can deliver the intended capability alone. Also avoid bundling
unrelated features merely to hit a low issue count.
