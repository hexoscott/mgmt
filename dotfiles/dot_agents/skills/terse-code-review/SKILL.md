---
name: terse-code-review
description: Applies to code reviews when asked to output in a terse format, useful for giving feedback to a developer on a bulk set of changes across multiple PRs.
---

# How to perform the review

I am reviewing the codebase in a leapfrog fashion with the devlopers working on the code, so I will review multiple PRs between two SHA commits / Github PR points which I will supply in the prompt.

Commits between the two SHAs should have a Github PR number in the title section in braces at the end of it denoting which PR some code relates to.

Firstly you need to open a file at /Users/scott/code-reviews/[repository name]/yyyy-MM-dd.md where repository name is the folder name at the root of the repo and the file is named with the current date stamp, if multiple reviews happen on the same day just append a -2 -3 etc. to the end of the file to not clash, do not append multiple reviews across a day into a single file please.  If the folder is not available for this file then create it please.

You should step through each commit between the two SHA points and gather the description and any comments using the locally installed Github CLI tool (gh), read and understand the code first, then in your own words and using the description from Github start a new section in the created markdown file.

Now we have a section for the PR or bare SHA if there is no PR number in the commit title you should add in code review findings with sub sections from blocking, critical, high, medium, low, nit. 

As you review new commits please put the PR numbers at the top of the file created in ascending order, not all commits are merged in order so it is useful to see them in order at the top of the file as a summary.

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
