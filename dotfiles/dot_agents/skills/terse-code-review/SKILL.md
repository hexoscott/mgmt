---
name: terse-code-review
description: Applies to code reviews when asked to output in a terse format, useful for giving feedback to a developer on a bulk set of changes across multiple PRs.
---

# Code review reporting style

Write the final review as a terse, evidence-backed handoff.

Lead with the verdict: clean, mostly sound with follow-ups, or not ready to approve.
Report actionable findings first, ordered by severity.
For each finding, include:
severity and a concise title;
an exact file and line reference;
the concrete failure mode or user impact;
the smallest useful fix or regression test.
Distinguish confirmed defects from design questions, coverage gaps, and non-blocking polish.
State the review boundary explicitly, such as the PR diff or ending commit. Do not use later code as evidence unless clearly labelled as an additional check.
After the findings, briefly state what was implemented correctly and which checks passed.
Mention environmental test failures separately so they are not mistaken for regressions.
If there are no findings, say so plainly and identify any remaining testing uncertainty.
Avoid narrating the investigation, repeating the diff, generic praise, or speculative nits.
Keep the response compact enough to scan in under a minute. Compress wording, not meaningful coverage; offer deeper detail only when requested.
Keep the tone conversational and light, like you are making suggestions and avoid saying something is "wrong", rather that it could be improved where this is the case.  We are looking to guide the developer rather than berate them for any mistakes or omissions in the code.
