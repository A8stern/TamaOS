---
name: tamaos-rust-review-verification
description: Review one immutable TamaOS Rust commit for missing build and test evidence, ineffective tests, target/feature gaps, and unaddressed safety, resource, performance, recovery, or data-loss risk. Use only for the verification-risk lane of $tamaos-code-review.
license: Apache-2.0
---

# TamaOS Rust Verification Review

Review only the assigned commit and verification-risk lane. Rust testing guidance is adapted from `full-stack-skills/rust-skills`; provenance is recorded in `docs/rust-skill-sources.md`.

## Review

1. Map acceptance criteria and changed behavior to effective unit, integration, compile, and hardware checks.
2. Inspect the relevant Cargo feature/target matrix and recorded results for formatting, Clippy, tests, builds, size, and hardware evidence.
3. Check error paths, boundary values, deterministic time, persistence/recovery, concurrency, resource limits, unsafe contracts, and regression protection when affected.
4. Do not redesign the code or duplicate a demonstrated correctness bug. Block only when completion or a relevant risk lacks adequate evidence.

Return the schema-3 report required by `$tamaos-code-review` with lane `verification-risk` and skill `tamaos-rust-review-verification`. Do not edit files.
