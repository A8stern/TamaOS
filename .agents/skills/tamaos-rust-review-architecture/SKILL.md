---
name: tamaos-rust-review-architecture
description: Review one immutable TamaOS Rust commit against its architecture clearance for crate/module boundaries, public API shape, dependency direction, no_std separation, and unjustified structural cost. Use only for the architecture lane of $tamaos-code-review.
license: Apache-2.0
---

# TamaOS Rust Architecture Review

Review only the assigned commit and architecture lane. Rust API-design guidance is adapted from `full-stack-skills/rust-skills`; provenance is recorded in `docs/rust-skill-sources.md`.

## Review

1. Consult `$tamaos-rust-architect`, the task clearance, `docs/architecture.md`, `docs/architecture-principles.md`, `docs/languages/rust/architecture.md`, and applicable ADRs.
2. Compare the diff with accepted crate/module ownership, public contracts, dependency direction, `no_std` boundary, error/resource policy, and current-milestone scope.
3. Check Rust API shape only where it affects a public contract: type safety, visibility, evolvability, and panic behavior.
4. Do not duplicate ordinary behavior bugs or missing-test findings. A blocker states architecture basis, observed implementation, mismatch, and required correction or user decision.

Return the schema-3 report required by `$tamaos-code-review` with lane `architecture`, skill `tamaos-rust-review-architecture`, architect skill `tamaos-rust-architect`, and a non-empty `architecture_basis`. Do not edit files or waive a divergence.
