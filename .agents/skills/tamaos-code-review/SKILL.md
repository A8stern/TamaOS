---
name: tamaos-code-review
description: Run the mandatory local TamaOS review gate for a committed change before push. Coordinates three independent reviewers for correctness, architecture, and verification risk; does not run in CI.
---

# TamaOS Code Review

Review one immutable local commit with three distinct, independent reviewers. This workflow is local evidence for the pre-push gate; GitHub Actions does not create or store it.

## Preconditions

- Identify the full `HEAD` SHA, intended base, acceptance criteria, and relevant repository rules.
- Review the committed diff. Do not claim uncommitted changes were reviewed.
- Ensure all three reviewers can inspect the same sources and run read-only checks.

## Three independent lanes

Launch exactly three reviewer agents concurrently when delegation is available. Give each the same commit, base, acceptance criteria, and relevant rules, plus exactly one lane:

1. **correctness** — read [references/correctness.md](references/correctness.md).
2. **architecture** — read [references/architecture.md](references/architecture.md).
3. **verification-risk** — read [references/verification-risk.md](references/verification-risk.md).

Reviewers must be distinct, read-only, and unaware of the other reports until all three finish. They must not edit files, coordinate findings, or broaden their lane. If independent agents are unavailable, stop: three sequential personas do not satisfy this gate.

## Evidence and decision

Normalize each report into:

```json
{
  "schema": 1,
  "commit": "<full SHA>",
  "lane": "correctness",
  "reviewer": "<distinct agent ID>",
  "verdict": "pass",
  "blocking_findings": [],
  "notes": []
}
```

Write the three files under `.harness-state/reviews/<SHA>/` as `correctness.json`, `architecture.json`, and `verification-risk.json`. This directory is local and ignored by Git.

A lane passes only when it has no unresolved blocking finding. The coordinator may deduplicate reports after collection but may not silently dismiss a blocker. Fix it or obtain a new report from that lane. If the commit changes, discard the old evidence and rerun all three reviewers independently.

Run `make review` to validate evidence, then `make prepush` to rerun the build/check harness and validate the same evidence immediately before push.

## Conflict prevention

- Correctness owns observable behavior defects.
- Architecture owns boundaries, contracts, coupling, and design cost.
- Verification-risk owns missing evidence and security, safety, performance, resource, and recovery risks.
- Repository invariants override general preferences. A safety or security blocker remains blocking regardless of lane.
- Equivalent solutions prefer the smaller change; subjective style is never a blocker unless a scoped rule requires it.
