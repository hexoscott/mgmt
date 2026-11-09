---
name: hexo-mode
description: Hexosoft coding discipline for scope, shape, tests and evidence. Use when implementing, fixing or refactoring code, including long human-in-the-loop sessions that make a large code change without a written plan.
---

# Hexo mode

Write less code, shape it well, prove it works. Restraint decides how much
changes, shape decides what the change looks like, evidence decides when it is
done.

Each bold name below is a rule. Cite rules by name in your reply; the human
may steer with them ("apply design twice").

A fully specified one-line edit skips straight to Change and Prove.

## 1. Frame

Open your first reply on a task with, in your own words, the goal, the problem
behind it, and the smallest change you expect to meet it. Then start. When the
evidence rules out the change asked for, show the evidence and stop.

**Sort the question.** Sort every open question before acting on it:

- _Observable_: running something answers it (behaviour, output, timing,
  layout, performance). Run it, or sketch a throwaway prototype, and let the
  result decide.
- _Preference_: a product or taste call no experiment settles. Ask, with your
  recommended answer first. Two cases are always Preference: readings of the
  request that differ in behaviour the human would notice, and a smallest
  change that differs from what was asked.
- _Irreversible_: force-push, deploy, data deletion, outbound messages. Pause
  for confirmation.
- Everything else is a reversible call. Make it, carry on, report it.

Done when the goal is restated and every open question is sorted.

## 2. Shape

**Data shape.** Name the data shape before writing logic. Pick the structure
that makes illegal states unrepresentable: a discriminated union over paired
flags, a state machine over lifecycle booleans, a table or registry over a
growing if/else. The tell that this was skipped is a new branch on an existing
chain, or a second boolean that must stay in sync with the first.

**Hexagon.** Domain logic is pure and framework-free. The domain owns its
ports, written in domain language; transport, storage and framework types stay
inside the adapter. Parse untyped input (HTTP, CLI, env, config, database rows,
third-party responses) once, in the adapter, into domain types, and trust those
types inside. A port earns its place with two implementations, the production
adapter and the test fake. Inline a wrapper with one caller and no second
implementation.

**Deep modules.** A module's interface is much smaller than what it hides.
Hide decisions (formats, ordering, retries, caching, error recovery) behind a
few general-purpose calls, and handle special cases inside rather than pushing
them onto callers. Collapse shallow layers: a pass-through that repeats the
methods and arguments of the layer below, or a split that forces callers to
know both halves. The `codebase-design` skill holds the full vocabulary.

**Design twice.** When the change adds or alters a port or a module's public
interface, write the caller's usage first, then sketch the types and
signatures with unimplemented bodies. Sketch two structurally different
shapes, and keep the deeper one. Implement against the sketch. A parameter the
sketch did not anticipate means the sketch, the requirement, or the
implementation is wrong: find which before absorbing it.

Done when the data shape is named and every new public signature exists as a
sketch. A change inside one function needs only the data shape.

## 3. Change

**Red first.** Before changing behaviour, write the test, run it, and watch it
go red for the reason it exists; then make it pass. For a bug, the red test is
the reproduction. Drive the code through its port or public interface, with
the expected value derived from the requirement, never from a run of the code.
A refactor has nothing to turn red: get the suite green before and after, and
add a characterisation test first where nothing covers the path.

**Smallest change.** Make the smallest change that meets the goal: only what
was asked, handling only the states callers can produce.

**Subtract first.** Within the code you are rewriting anyway, delete dead
code, redundant guards and stale branches first, then build on the simpler
base. List dead code beyond those lines in the reply.

**Surgical.** Every changed line traces to the goal. Match the local style.
Name unrelated problems in the reply and leave them in place. Remove whatever
your own change orphaned.

**Redesign over bolt-on.** When the goal would add a second flag that must
stay in sync with the first, another branch on an existing chain of special
cases, or a compatibility shim, and every caller lives in this repo, offer a
redesign as a Preference question: rebuild the affected area as if the
requirement had existed from day one, migrate every caller, and delete the old
path in the same change.

**Reader load.** A new reader answers "where does X come from?" and "what can
change X?" in under 30 seconds. Prefer returns over mutation, locals over
fields, derived state over synced state.

**Lever.** When one mechanical edit repeats across many sites, or a check will
need rerunning, write the codemod, generator or rerunnable check that does or
proves it, so a reviewer reruns it rather than trusting you. Do the first unit
by hand, then build the lever and rerun it on that unit to prove it matches.

## 4. Prove

**Two edits.** Every test you write or change survives both imagined edits:
break the behaviour and the test fails; restructure the internals with the
same observable results and the test still passes.

**Evidence ladder.** For each fact the change's correctness rests on, climb as
far as is cheap and state the rung reached:

1. Asserted.
2. Pointed at: a real `file:line`, or the library's own source.
3. Reasoned: the failure walked step by step and shown unreachable.
4. Run: a script or test against the real code that fails loudly if wrong.
5. Reproduced in the running app.

Rung 4 is the bar. "It compiles" and "tests pass" sit on rung 1 for any
behaviour the tests do not exercise.

**Root cause.** Reproduce first, then ask "why" until the answer is a wrong
decision in the code, and fix it there. A guard is a fix only when the state
it handles is legitimate; otherwise find what produced the state. Search for
the same pattern elsewhere: fix the reported path, and list each other
instance by `file:line`.

**Attack the premise.** After two fixes resting on the same premise fail the
same check, write the premise down and test it directly before writing a third.

Done when every behaviour the goal names has rung-4 evidence, or a stated
reason it stops lower.

## 5. Long sessions

Use this section when the change will take more than one verifiable unit. It
runs as one long session with the human in the loop, not as a plan split into
tickets.

- When the approach still holds preference calls, run the `grilling` skill
  before writing code.
- **Decision log.** Write each settled decision, from grilling or along the
  way, to a decision log in the session scratchpad (or a gitignored file when
  there is none), so it survives compaction. Re-read it after a compaction.
  An architectural decision also gets an ADR in the repo's docs.
- **Verifiable units.** Advance in units: known-good state, one change, its
  check passing. When the human wants commits, make one per unit, keeping each
  test with the change it proves, and order them so the history reads as an
  argument: subtraction before reshape, scaffold before feature. A reviewer
  then reviews commit by commit, and a bad unit reverts alone.

Done when every decision a later step depends on is in the log and each unit's
check passed before the next began.

## 6. Report

- After a long session, open with the restated goal.
- Name each rule that changed a decision, and the decision it changed. A rule
  named with no decision behind it was not applied.
- Label each claim with its evidence-ladder rung. Run any check you could hand
  the human instead of handing it over.
- List open decisions, the unrelated problems and dead code you left in place,
  and other instances of a fixed pattern.

## 7. Learn

**Structure over text.** When the human corrects the same class of mistake
twice, propose a fix at the highest level that holds: architecture that makes
the mistake impossible, then a type, then a lint or CI check whose error names
the fix, then a test. A doc or agent rule comes last, reserved for judgment
calls nothing can enforce. On approval, land it in its own commit.
