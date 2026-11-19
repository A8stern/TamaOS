---
name: tamaos-review-verification
description: Review one immutable TamaOS commit for missing or stale verification evidence, ineffective tests, build gaps, and relevant security, safety, performance, recovery, or data-loss risk. Use only as the verification lane of the local three-skill review gate.
license: MIT
---

# TamaOS Verification Review

Perform a read-only evidence audit for one exact commit. This skill adapts the evidence-before-claims discipline of the upstream verification skill recorded in `docs/review-skill-sources.md`.

## Inputs

Require the full commit SHA, intended base, acceptance criteria, claimed checks, and applicable repository rules. Treat another agent's success statement as a hypothesis. Inspect the committed snapshot and run safe, relevant local verification commands when the environment permits; never install dependencies, flash hardware, or mutate external state without separate authority.

## Owned questions

- Is every acceptance criterion backed by a meaningful check or explicitly pending physical verification?
- Do tests exercise the changed behavior and failure path, or can they pass while the defect remains?
- Are build, feature, platform, packaging, migration, or clean-tree conditions relevant to the change left unverified?
- Are security, privacy, electrical safety, performance, memory, timing, recovery, or data-loss claims stronger than their evidence?
- Does each completion claim name a fresh command or physical observation whose result actually proves it?

Read full command output and exit status before treating a check as passing. Distinguish static inspection, executed evidence, fixture-only evidence, host verification, and hardware verification. Missing hardware cannot be replaced by a build claim.

## Exclusions

- Do not duplicate a statically demonstrated behavior bug; `$tamaos-review-correctness` owns it.
- Do not prefer a different component structure or abstraction; `$tamaos-review-architecture` owns it.
- Do not block merely because more tests are imaginable. Name the concrete risk and the smallest evidence that clears it.
- Do not edit files, create commits, or read another reviewer's report.

## Report

Return only one JSON object for the coordinator:

```json
{
  "schema": 2,
  "commit": "<full SHA>",
  "lane": "verification-risk",
  "skill": "tamaos-review-verification",
  "reviewer": "<distinct agent ID>",
  "verdict": "pass",
  "blocking_findings": [],
  "notes": []
}
```

Use `fail` when `blocking_findings` is non-empty. Each finding must contain `location`, `missing_or_invalid_evidence`, `risk`, and `smallest_clearing_check`. Notes must list commands actually run and unverified surfaces.
