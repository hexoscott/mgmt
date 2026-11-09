---
name: factory-plan-to-issues
description: Investigate a substantial codebase change, record decisions, and produce a spec and large, independently startable GitHub issues ordered in waves; also audit readiness of an existing spec or ticket set. Use when a change is too large for one long session and parts should run in parallel, not for implementing tickets.
---

# Factory plan to issues

Produce a plan another agent can execute without reconstructing the conversation.
Prefer fewer, larger implementation issues, each sized for one long implementation
session. A larger issue earns its size by keeping one responsibility together, not
by collecting unrelated features. Every published implementation issue is
**isolated**: it starts from the target branch alone and never waits on another
open issue. Merge conflicts between isolated issues are expected and acceptable.

For an existing plan, resume at the first missing stage. If asked only to check
readiness, start at step 5 without regenerating tickets or repeating interviews.
Snapshot full issue bodies, comments and actual blockers locally when auditing a
tracker. Keep observed relationships separate from proposed repairs; a read-only
review does not authorise changing the tracker.

## 1. Establish the effort

Read the project's instructions, glossary, architectural decisions, relevant
source and tests. Follow the actual data and request paths, including callers,
background jobs and integrations. Read any supplied planning artifacts and issue
comments; distinguish proposed behaviour from behaviour already on the target branch.

Establish the desired outcome, exclusions, target repository/branch, available
worker concurrency and execution constraints. Inspect the runner when accessible:
how it selects issues, recognises dependencies, supplies context, and treats
completion. Otherwise record these as unverified and ask only what affects planning.
Record which version is actually deployed and must coexist during rollout; do not
confuse a merged prototype with a production compatibility obligation.

Use the project's document location; otherwise start `plans/<effort>/plan.md` and
`plans/<effort>/issues/`. Keep this effort resumable in that record:

- Outcome, scope and current stage.
- Baseline branch/commit and relevant source/test locations as navigation hints.
- Decisions: stable ID, question, answer, rationale, alternatives, and source
  (user answer, repository evidence, research, or explicitly provisional assumption).
- Open questions and investigations, their impact, and what unlocks them.
- Spec, issue map, approval scope, and publication progress/real issue identifiers.

Reuse existing artifacts instead of opening a second competing plan. On resumption,
read this record, check relevant code/tracker changes, and continue from the first
unresolved point. Do not repeat answered questions unless new evidence changes them.

## 2. Investigate and interview

Map the problem broadly before drilling into individual solutions. Group unknowns
by behaviour, data, integrations, and operational changes; work first on decisions
that constrain the rest. Research facts in source or primary documentation before
asking the user. Use a small disposable experiment only when inspection cannot
answer a consequential technical question; record its result, not an implementation.

Ask a focused question or a small group of related questions at a time. Explain the
tradeoff and recommend an option. Challenge requirements that add cost without
advancing the outcome. Record answers as they arrive; never substitute an agent's
preferred answer for the user's decision. Continue independent research while an
answer is pending, but do not finalise work that depends on it.

For a tenant/payment migration, investigate ownership and isolation, existing-data
mapping, authorisation, account/subscription lifecycles, billing authority, webhook
delivery/retries, failure recovery and cutover. Use relevant topics, not a mandatory
questionnaire for every project. Separate product decisions from implementation
details the worker can safely choose.

Keep uncertainty visible. Unknown requirements, missing resources, and unresolved
contract decisions prevent affected work becoming executable. A research or human
setup task may resolve them, but it must not masquerade as an implementation issue.
Distinguish implementation/test prerequisites from production activation gates:
fixture-based payment tests need no live credentials, while a live cutover does.
If only part of the effort can be specified, propose a bounded phase and retain the
remainder explicitly; do not present that phase as the complete original outcome.

## 3. Write the spec

Synthesize from the recorded evidence and answers, preserving decision IDs. Include:

- Problem, desired user outcomes, exclusions, and relevant domain definitions.
- Numbered behavioural requirements, including meaningful failure/edge cases.
- Responsibility boundaries and producer/consumer contracts: data ownership,
  interfaces, invariants and compatibility expectations, with enough precision to
  implement separately. Prefer existing architectural seams.
- Data migration and rollout/recovery decisions where applicable; identify any
  irreversible step and human/external prerequisites.
- Verification: observable acceptance scenarios, existing test seams/prior art,
  feasible local/CI commands, and any checks needing live infrastructure.
- Open decisions and assumptions, each marked resolved, accepted, or still gating.

Keep requirements concise and testable. Do not inflate the spec with repetitive
user stories or use a document link in place of a necessary contract definition.
If an adequate spec already exists, retain it and record only necessary amendments.

## 4. Package coherent work

Start with the fewest issues that deliver the approved outcome. Put schema, domain
logic, callers, API/UI, tests and necessary documentation for a capability together
where they form one verifiable change. Use internal checklists for implementation
steps rather than making every step another issue.

Split only where both parts start from the same baseline, neither consumes the
other's output, and each delivers a verifiable outcome alone; or where one ticket
would exceed the runner's practical implementation/review limits. Do not size by
lines, hours invented without evidence, or a fixed ticket count. A context window
limit alone does not establish a good responsibility boundary.

Give each atomic requirement one delivery owner. Split a compound story into
separate obligations when different tickets supply its parts, retaining its source
story ID and a named final integration verifier. An owner must be able to complete
its obligation from its own work and its baseline, which includes earlier waves
once merged; an ID in an index is not evidence of delivery. Assign shared
contract/schema changes and migrations an explicit owner. Keep a needed preparatory
refactor with its first consumer unless it earns an earlier wave of its own.

For every consumed capability, establish exactly one of:

1. It already exists on the baseline, with evidence.
2. This issue implements it completely.
3. An issue in an earlier wave supplies it, with a precise output contract.

**Waves.** Wave 1 is every issue that starts from the baseline. An issue that
consumes another issue's output, or needs a gate (human setup, CI bootstrap) to
hold first, belongs in a later wave than that producer or gate. First try merging
a consumer into its producer; keep it separate only when the combined issue would
exceed the runner's practical limits. Work never merges into the gate that
protects it. Aim for one wave; a third wave needs a stated reason. Every
inter-issue reference is either a wave prerequisite or context only. Issues in
the same wave have no merge order: whichever merges second resolves conflicts.
Publish a later-wave issue only after every producer it consumes has merged and
every gate protecting it is done, each verified on the target branch; a closed
issue or PR is not that evidence. Then re-ground its draft against the merged code,
citing that evidence in its brief, and repeat step 5 on it before publishing.

Before expanding ticket prose, write the compact capability/ownership ledger in
[the readiness protocol](references/readiness.md) and run its checker. Record
provided/required capabilities, each issue's wave and which work each gate
protects. A gate protecting implementation must hold on the baseline or sit in an
earlier wave than that work, even if a human must deliver it. Do not defer
required PR checks to a final release-workflow issue.
Review this first graph and consequential questions before drafting long bodies;
ask the user only where an answer or scope approval is actually missing.

Audit overlap by changed behaviour and shared symbols, not just filenames. Two
additive routes can coexist in one router. Two rewrites of tenant resolution cannot
be assumed independent. For unavoidable overlap, state the owner, the disjoint edit
boundaries, and the deterministic merge/regeneration steps. If resolution requires
a fresh design decision, combine the work or move one into a later wave. Do not promise
conflict-free rebases or make correctness depend on another worker's open branch.

Keep each ticket green when merged into the target branch. For migrations, use
compatible intermediate states where feasible; put removal behind all consumers.
If no safe intermediate state exists, retain the coupled work in one issue or
identify that the proposed runner cannot execute it as planned.

Write each draft using [the issue contract](references/issue-contract.md).

## 5. Audit before release

Follow [the readiness protocol](references/readiness.md): run the declared-graph
checker, check promises against failure scenarios, then dispatch one independent
reviewer with a fresh context. This is a required stage of this skill, not a second
skill the user must remember to invoke. The checker cannot establish whether the
ledger omitted a capability or the prose contradicts the spec; the reviewer must
read actual source, contracts and acceptance criteria.

Remove needless wave prerequisites, not real constraints. Merge issues that need
each other's output and represent one responsibility; otherwise recut the contracts
or move the consumer to a later wave, and re-audit. Resolve defects in the
spec and draft bodies, not by accumulating corrective comments.
Repair confirmed findings and have the reviewer recheck the affected contracts and
dependants. Record ready/held status per issue and unresolved execution blockers.
If independent review is unavailable, keep the result a draft and state that limit.

Present the concrete spec and issue map together: title, outcome, owned area,
wave with the reason for any wave after the first, concurrency and remaining gates.
Invite corrections about
scope and granularity. If approval of this scope/publication is still needed, ask
here, after drafts are reviewable; honour approval already given. Do not release
affected tickets while a consequential user decision remains unanswered.

## 6. Publish and verify

For GitHub, follow [publication and runner checks](references/github.md). A request
to design this workflow alone does not authorise publishing issues in another repo.
Without publication authority, leave complete local drafts and report that boundary.

Publish one wave at a time; later waves stay local drafts. After publication,
report the spec, the published wave, held later-wave drafts, manual gates and
anything not verified. When a wave has merged, promote the next per step 4's
**Waves**. On later changes, update the canonical spec, affected issue bodies and
plan.json together; reconcile already-implemented work
before changing ownership. Do not hide a prerequisite in a comment or silently widen
an in-flight issue. Pause affected queued work through the runner's supported gate
when a changed plan would otherwise let it start incorrectly.

## Sources

Inspired by Matt Pocock's [wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md),
[to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md)
and [to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md).
Self-contained; these links are attribution, not required skill invocations.
