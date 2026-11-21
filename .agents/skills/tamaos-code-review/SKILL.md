---
name: tamaos-code-review
description: Run the mandatory local TamaOS review gate for a committed change before push. Coordinates the three independent review skills registered for the affected programming language; does not run in CI.
---

# TamaOS Code Review

Review one immutable local commit with three distinct, independent reviewers. This workflow is local evidence for the pre-push gate; GitHub Actions does not create or store it.

## Preconditions

- Identify the full `HEAD` SHA, intended base, acceptance criteria, and relevant repository rules.
- Identify the task's architecture clearance and its canonical basis, or a recorded `not-needed` reason.
- Review the committed diff. Do not claim uncommitted changes were reviewed.
- Ensure all three reviewers can inspect the same sources and run read-only checks.

## Resolve the language profile

Read [references/language-review-contract.md](references/language-review-contract.md). Identify the programming language materially changed by the commit and resolve its registered review profile.

The profile must provide three concrete language-specific skills: correctness, architecture, and verification-risk. These roles are contracts, not generic fallback skills. If the language has no complete profile, stop and report the missing profile; do not pass the gate with improvised reviewer prompts.

For the architecture lane, also resolve the corresponding language architect from `$tamaos-architecture`. The reviewer must compare the commit with that architect's recorded clearance and accepted architecture sources. If the basis is missing or ambiguous, stop or ask the architect for the applicable source; do not infer approval from the code itself.

## Run three independent skills

Launch exactly three reviewer agents concurrently when delegation is available. Give each the same commit, base, acceptance criteria, relevant rules, language, and its one registered skill.

Reviewers must be distinct, read-only, and unaware of the other reports until all three finish. A reviewer must use only its assigned review skill for judgment and must not load either of the other two review skills. They must not edit files, coordinate findings, or broaden their lane. If independent agents are unavailable, stop: running three skills sequentially in one context does not satisfy this gate.

## Evidence and decision

Normalize each report into:

```json
{
  "schema": 3,
  "commit": "<full SHA>",
  "language": "rust",
  "lane": "architecture",
  "skill": "<registered language-specific architecture-review skill ID>",
  "architect_skill": "<consulted language architect skill ID>",
  "reviewer": "<distinct agent ID>",
  "verdict": "pass",
  "architecture_basis": ["<clearance, architecture document, or ADR>"],
  "blocking_findings": [],
  "notes": []
}
```

Write the three files under `.harness-state/reviews/<SHA>/` as `correctness.json`, `architecture.json`, and `verification-risk.json`. This directory is local and ignored by Git.

A lane passes only when it has no unresolved blocking finding. The architecture report must name the consulted language architect skill. An architecture mismatch must state the accepted basis, observed implementation, mismatch, and required correction or user decision. The coordinator may deduplicate reports after collection but may not silently dismiss a blocker. Fix it, or return a genuinely new architectural decision to the user and record it before obtaining a new report. If the commit changes, discard the old evidence and rerun all three reviewers independently.

Run `make review` to validate evidence, then `make prepush` to rerun the build/check harness and validate the same evidence immediately before push.

The language review contract owns lane separation and the report interface. Repository invariants override general preferences. A safety or security blocker remains blocking, and equivalent solutions prefer the smaller change.
