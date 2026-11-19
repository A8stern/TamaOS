---
name: tamaos-code-review
description: Run the mandatory local TamaOS review gate for a committed change before push. Coordinates three independent reviewers, each using a different required review skill; does not run in CI.
---

# TamaOS Code Review

Review one immutable local commit with three distinct, independent reviewers. This workflow is local evidence for the pre-push gate; GitHub Actions does not create or store it.

## Preconditions

- Identify the full `HEAD` SHA, intended base, acceptance criteria, and relevant repository rules.
- Review the committed diff. Do not claim uncommitted changes were reviewed.
- Ensure all three reviewers can inspect the same sources and run read-only checks.

## Three independent skills

Launch exactly three reviewer agents concurrently when delegation is available. Give each the same commit, base, acceptance criteria, and relevant rules. Explicitly assign exactly one skill to each reviewer:

1. **correctness** — invoke `$tamaos-review-correctness`.
2. **architecture** — invoke `$tamaos-review-architecture`.
3. **verification-risk** — invoke `$tamaos-review-verification`.

Reviewers must be distinct, read-only, and unaware of the other reports until all three finish. A reviewer must use only its assigned review skill for judgment and must not load either of the other two review skills. They must not edit files, coordinate findings, or broaden their lane. If independent agents are unavailable, stop: running three skills sequentially in one context does not satisfy this gate.

## Evidence and decision

Normalize each report into:

```json
{
  "schema": 2,
  "commit": "<full SHA>",
  "lane": "correctness",
  "skill": "tamaos-review-correctness",
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

- `$tamaos-review-correctness` owns observable behavior defects.
- `$tamaos-review-architecture` owns boundaries, contracts, coupling, and structural cost.
- `$tamaos-review-verification` owns missing evidence and security, safety, performance, resource, and recovery risks.
- Route by the claim being made: a concrete trigger producing wrong behavior belongs to correctness; a boundary or ownership violation whose harm exists even when current behavior works belongs to architecture; an unproven claim or non-functional risk without a demonstrated behavior defect belongs to verification.
- When a reviewer notices an out-of-scope concern, mention the target skill in `notes` without making it a blocking finding. The assigned reviewer for that skill decides it independently.
- Repository invariants override general preferences. A safety or security blocker remains blocking regardless of lane.
- Equivalent solutions prefer the smaller change; subjective style is never a blocker unless a scoped rule requires it.
