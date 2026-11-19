---
name: tamaos-review-correctness
description: Review one immutable TamaOS commit for observable behavior defects, regressions, broken contracts, and failure-handling bugs. Use only as the correctness lane of the local three-skill review gate; do not review architecture or test sufficiency.
license: MIT
---

# TamaOS Correctness Review

Perform a read-only, evidence-driven review of one exact commit. This skill adapts the precision and candidate-refutation approach of the upstream code-review skill recorded in `docs/review-skill-sources.md`.

## Inputs

Require the full commit SHA, intended base, acceptance criteria, and applicable repository rules. Inspect the committed diff and enough unchanged callers, contracts, and state transitions to prove or refute each candidate. Do not review uncommitted content as part of the verdict.

## Owned questions

- Does a concrete input, state, ordering, or failure path produce the wrong observable result?
- Did the change break a caller, compatibility contract, error propagation, cleanup, or resource state?
- Did deletion or replacement remove an invariant without restoring it elsewhere?
- Can identity normalization, aliasing, empty values, boundaries, overflow, lifetime, concurrency, or aggregation bypass the intended behavior?

For every candidate blocker, try to refute it against the real surrounding code. Keep only high-confidence findings with a concrete trigger and effect. A clean review is valid; do not manufacture findings.

## Exclusions

- Do not judge component boundaries, coupling, abstraction choice, or ADR alignment; `$tamaos-review-architecture` owns them.
- Do not judge whether tests, builds, or other evidence are sufficient; `$tamaos-review-verification` owns them.
- Do not report formatting, naming, taste, speculative improvement, or pre-existing debt as blockers.
- Do not edit files, create commits, or read another reviewer's report.

## Report

Return only one JSON object for the coordinator:

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

Use `fail` when `blocking_findings` is non-empty. Each finding must contain `location`, `scenario`, `impact`, and `smallest_safe_correction`. Notes may state inspected scope and non-blocking limits; they must not hide a blocker.
