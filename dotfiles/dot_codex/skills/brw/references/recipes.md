# Reuse and maintain private recipes

Recipes are deterministic browser workflows stored in a private provider. This skill explains their lifecycle; it is not a database of operational recipes. Read this reference for repeated work such as recurring downloads, report retrieval, form entry, or draft preparation.

## Search, pin, run

1. Discover `brw_recipe_search` and `brw_recipe_run` with `brw_tools` and inspect their current definitions.
2. Search using the user's intent and the exact site origin. Select only a result whose purpose, origins, and declared risk match the task.
3. Pass the `id`, `version`, and `digest` from that same result unchanged to run, along with declared runtime inputs and the intended string `tab_id`. Search exposes metadata, not private executable steps; do not invent hidden requirements.
4. Inspect status, failed steps, attempts, and artifact handles. Read only the evidence needed to confirm the requested result.

If there is no matching recipe or no configured provider, complete the authorized browser task using ordinary tools. Do not install a daemon or change provider configuration merely to open a page. A saved workflow grants no standing authorization for its external effects.

## Promote a successful repeated task

When reuse is reasonably likely, preserve a proven sequence whose targets can be resolved semantically, inputs can be declared, and completion can be checked. Avoid encoding exploratory browsing, unresolved failures, coordinate-only flows, human challenges, or approval decisions.

Use `brw_trace` entries and live page inspection as evidence. Translate temporary refs such as `e17` into a role plus a stable accessible name, test ID, or href selector. Each target must resolve unambiguously at execution time. A trace exported as a batch is not yet a valid recipe.

Read the current [recipe authoring guide](https://github.com/Don-Works/brw/blob/main/skills/brw/references/recipes.md) and [schema](https://github.com/Don-Works/brw/blob/main/internal/recipe/schema.go) before drafting JSON. Use the installed `brwctl recipe` help/parser as the authority for its supported version. Declare immutable ID/version, intent metadata, exact origins, risk, inputs, and ordered steps. Never embed credentials, captured session state, or private record values; pass variable data at runtime.

Each browser actuation declares its effect, and recipe-level risk must cover it. Attach transient download, popup, or network postconditions to the triggering action so observation is armed before the event. Use bounded waits. An external write needs an idempotency key and durable, specific completion state; it receives at most one actuation attempt per run. Prefer a positive completion marker tied to the intended record and page context.

Create drafts outside every Git checkout, in an owner-only private directory, with file mode `0600`. For a configured local provider:

```sh
brwctl recipe validate --file /absolute/private/draft.json
brwctl recipe install --file /absolute/private/draft.json --root /absolute/configured/recipe-root
```

The local root must be owner-only (`0700`); symlinks and Git checkouts are rejected. Use the root actually configured for the daemon, rather than assuming the CLI default reaches that provider. For an HTTPS provider, use its authorized authoring interface instead of local installation.

After validation and installation, search again and confirm the expected version/digest. Exercise a read-only recipe on a representative task and clean up its temporary outputs. Do not perform an external write just to test promotion; use a task-authorized action, an approved test environment, or a safe preflight. Stored bodies stay in the private provider, never in this skill or the application repository.

## Reusable patterns

- **Recurring original download:** Find the requested document using runtime inputs, arm download completion on the triggering action, then capture that exact completed download as an artifact. Match the source tab and unique file identity; do not substitute an old same-name file or a printed reconstruction. Extension-backed captures preserve the user's original file and may need host Downloads permission.
- **Report or record retrieval:** Navigate to the known view, resolve a record by declared input, verify the page context, then capture text or semantic JSON. Keep its handle and read only relevant excerpts.
- **Prepare a draft:** Find the intended composer and fill the declared text; verify its exact value. Keep delivery as a separate workflow invoked only when the user authorizes that send. An empty composer can support rerun preflight, but is not by itself proof of delivery.
- **Verify a repeated form task:** Resolve fields by semantic identity, fill variable inputs, and assert the intended values. Any final submit/save action needs task authorization and a durable result tied to the intended record.

These are authoring patterns, not executable recipes. Build actual selectors from the observed site.

## Repair failures

Distinguish changed site structure from authentication expiry, permissions, incorrect inputs, outages, rate limits, or human challenges. Only deterministic site drift justifies a new recipe version.

Inspect the affected page, correct the smallest semantic target or event mismatch, and increment the semantic version. Validate, install, and search again. Never overwrite an existing ID/version with different content or weaken origins/postconditions to force a pass.

An ambiguous failed write must be reconciled against durable state before further action; do not blindly rerun it. `attempts: 0` means the current UI already satisfied the postcondition, not that a previous remote transaction occurred. Report only what the evidence establishes.

Long-running schedules, webhook triggers, credentials, and authorization belong to the caller or an external scheduler; brw executes bounded browser transactions.

Sources: [official recipe guide](https://github.com/Don-Works/brw/blob/main/skills/brw/references/recipes.md) and [recipe architecture](https://github.com/Don-Works/brw/blob/main/docs/recipes-and-artifacts.md), reviewed 2026-09-11.
