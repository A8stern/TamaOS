---
name: tamaos-review-architecture
description: Review one immutable TamaOS commit for architectural drift, boundary violations, misplaced responsibilities, incompatible contracts, and unjustified structural cost. Use only as the architecture lane of the local three-skill review gate.
license: MIT
---

# TamaOS Architecture Review

Perform a read-only comparison of the committed change against `docs/architecture.md`, accepted ADRs, and repository ownership rules. This skill adapts the architecture-drift method of the upstream skill recorded in `docs/review-skill-sources.md`.

## Inputs

Require the full commit SHA, intended base, acceptance criteria, and applicable architecture sources. Inspect the committed diff plus the minimum dependency and ownership context needed to establish a structural claim.

## Owned questions

- Does the change violate documented dependency direction or the hardware/domain boundary?
- Did a component acquire a responsibility owned by another component or agent?
- Does the change create unnecessary coupling, duplicate ownership, a cycle, or an undocumented structural change to a public or persistence contract?
- Is an abstraction speculative for the accepted milestone, or is a required seam missing from the accepted design?
- Does implementation contradict an accepted ADR or leave stable architecture documentation materially false?

Every blocker must cite the documented intent, actual file-level evidence, concrete present impact, and the smallest directionally correct remedy. Do not require a fashionable pattern or future scalability without a current project force. A healthy change may pass with no findings.

## Exclusions

- Do not re-review a contract problem that already has a concrete wrong-behavior scenario; `$tamaos-review-correctness` owns it. Review the contract here only when its shape, ownership, or dependency direction is itself the defect.
- Do not judge test coverage, build evidence, security evidence, or hardware proof; `$tamaos-review-verification` owns them.
- Do not block on naming, formatting, optional cleanup, or documentation detail that does not change structural truth.
- Do not edit code or documentation, create commits, or read another reviewer's report.

## Report

Return only one JSON object for the coordinator:

```json
{
  "schema": 2,
  "commit": "<full SHA>",
  "lane": "architecture",
  "skill": "tamaos-review-architecture",
  "reviewer": "<distinct agent ID>",
  "verdict": "pass",
  "blocking_findings": [],
  "notes": []
}
```

Use `fail` when `blocking_findings` is non-empty. Each finding must contain `location`, `documented_intent`, `actual_structure`, `impact`, and `smallest_safe_correction`.
