# GitHub publication and runner checks

Use an available GitHub integration or `gh`; native dependencies are required for
a runner that schedules from them. Body mentions, checklists, sub-issue links and
project status fields do not substitute for dependency edges.

Inspect the project's existing labels and automation before publishing. Do not
invent an activation label or modify the runner as part of planning. Distinguish
permission to publish draft issues from permission to enqueue unattended execution.

## Safe publication order

1. Save the reviewed spec, complete issue drafts, checked plan.json and independent
   readiness findings locally. No unresolved execution blocker may be hidden behind
   a passing graph check. Give
   drafts stable effort-local keys; record any existing matching issue URLs.
2. Create or update the spec/index without execution labels. Keep it out of the
   implementation queue: its role is reference and progress, not a second build.
3. Create implementation issues **without runner eligibility**. Save each resulting
   repository, number, database ID and URL immediately in the publication record.
   For retries after an uncertain response, search/read back before creating again.
4. Replace local references with real links and attach sub-issues where supported.
   Add the intended native blockers; their direction is consumer blocked by producer.
   Preserve unrelated pre-existing relationships on reused issues and reconcile any
   unexpected edge before release. Do not close superseded existing issues without
   authority to do so.
5. Read back complete bodies, labels, parent links and **all pages** of blockers.
   Compare the actual edge set with the intended graph, including unexpected edges;
   verify no cycles and check the runnable frontier against the plan. Check closed
   external prerequisites actually delivered their promised output to the target
   branch; investigate cancellation or missing implementation.
6. Only after the whole graph passes, enable the approved implementation issues for
   the runner, if enqueueing is authorised. Blocked issues may be eligible when the
   runner demonstrably honours their edges. Leave human/setup/unknown-contract work
   ineligible. If a manual task truly gates implementation, give it a non-runner
   issue and make it a native blocker; a deployment-only gate need not hold offline
   implementation. Re-read final labels and report which issues are now runnable.

On partial failure, stop activation, record what succeeded and what remains, and
resume by reconciling those real issues. Do not claim publication is complete or
fall back to prose blockers for a runner that ignores them. When updating existing
eligible issues, first use the runner's supported hold/stop mechanism for affected
work; account for already-running workers before changing their contracts.

## GitHub dependency mechanics

These are operation shapes; resolve the repository and real identifiers first.
Use structured integration arguments, or files with `--body-file` for multiline
bodies. Do not interpolate untrusted prose into shell commands.

```sh
gh api repos/OWNER/REPO/issues/BLOCKER_NUMBER --jq '{id,number,state,html_url}'
gh api --method POST repos/OWNER/REPO/issues/CONSUMER_NUMBER/dependencies/blocked_by -F issue_id=BLOCKER_DATABASE_ID
gh api --paginate repos/OWNER/REPO/issues/CONSUMER_NUMBER/dependencies/blocked_by --jq '.[] | {id,number,state,html_url}'
```

The numeric `issue_id` is the blocker's database ID, distinct from its issue
number and GraphQL node ID. An HTTP success is not the dependency audit: compare
read-back results. See [GitHub's dependency API](https://docs.github.com/en/rest/issues/issue-dependencies).

## Scott's Code Factory

Verify the installed/current runner before relying on these observations from
`hexoscott/code-factory` on 2026-11-01:

- Queue eligibility uses `Factory` plus `Ready` or `ready-for-agent`; the spec/index
  should carry neither combination. `Needs-Human` holds an issue, including one
  with a stage label. Explicit `--issue` runs can bypass the ready label.
- New starts and explicit `--issue` runs check open native `blocked_by` issues.
  Normal polling resumes stage-labelled issues without rechecking blockers: when
  replanning one, keep `Needs-Human` until all newly required outputs are delivered
  and its existing branch/stage is reconciled. Adding edges alone does not hold it.
  Closing a prerequisite can unblock new starts; do not close an undelivered
  producer as though it completed.
- Workers receive their own body/comments and up to ten directly related issues,
  one level deep, filtered by writer permissions. They have no GitHub access.
  Embed all necessary decisions/contracts in the worker's own issue; parent links
  and transitive dependency chains are not a reliable context delivery mechanism.
- Work can run concurrently (currently up to three issues). Each issue must land
  green on the target branch. An open integration branch is not a prerequisite
  delivery mechanism for separate issues in this runner.
- Agent stages currently have a two-hour total limit. Size coherent work so each
  stage remains feasible; deep review does not remove execution limits.
- Changes under `.github/` require human handling in this runner. Separate or flag
  that operational gate where the feature needs workflow changes. Required PR CI
  and protection must be bootstrapped before the feature PRs they protect; later
  nightly/release automation can have different prerequisites.

Confirm against `internal/factory/issues.go`, `internal/github/github.go`,
`internal/prompts/templates/ground-rules.md`, `internal/agent/agent.go`, and the
runner README. These are compatibility notes, not instructions to change Factory.
