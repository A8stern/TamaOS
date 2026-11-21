---
name: tamaos-rust-review-correctness
description: Review one immutable TamaOS Rust commit for concrete semantic, ownership, soundness, panic, overflow, error-handling, concurrency, and observable behavior defects. Use only for the correctness lane of $tamaos-code-review.
license: BSD-3-Clause
---

# TamaOS Rust Correctness Review

Review only the assigned commit and correctness lane. This workflow is adapted from `po4yka/rust-skills` `rust-review`; provenance is recorded in `docs/rust-skill-sources.md`.

## Review

1. Read the diff plus affected callers, invariants, and behavior tests.
2. Inspect Rust edition/MSRV and relevant `no_std` constraints.
3. Look for demonstrable ownership/lifetime mistakes, unsound `unsafe`, reachable panics, unchecked indexing/casts/arithmetic, lost errors, invalid state transitions, races, deadlocks, and resource misuse.
4. A blocker needs a concrete trigger, violated contract, and smallest correction. Do not block on architecture preference or missing verification evidence alone; route those in `notes`.

Return the schema-3 report required by `$tamaos-code-review` with lane `correctness` and skill `tamaos-rust-review-correctness`. Do not edit files.
