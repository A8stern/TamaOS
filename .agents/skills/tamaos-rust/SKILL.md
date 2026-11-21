---
name: tamaos-rust
description: Implement and maintain Rust code in TamaOS using the repository architecture, no_std boundaries, Cargo harness, and explicit error and resource handling. Use with $tamaos-code for Rust source, manifests, tests, dependencies, or toolchain changes.
---

# TamaOS Rust

Pair this skill with `$tamaos-code`. Read `docs/languages/rust/architecture.md` and the task's architecture clearance before implementation.

## Rust contract

- Keep portable domain and UI logic `no_std`; platform crates and allocation belong only where the accepted platform architecture permits them.
- Express hardware, time, rendering, storage, and audio through contracts owned by the application boundary. Do not import ESP-specific crates into domain code.
- Prefer explicit types and errors over panics, unchecked casts, global mutable state, or speculative generics.
- Add dependencies only for a current requirement, with the reason and feature set visible in the manifest.
- Preserve the root harness. Put Cargo commands in the affected project's `.harness` adapter.

## Verification

Run the registered adapter through `make check`, `make test`, and `make build`. Rust checks should include `cargo fmt --check`, Clippy with warnings denied, tests, and a build for the relevant host or target. Report host and hardware evidence separately.

Do not select the ESP runtime, board target, allocator, async executor, or flashing tool until the toolchain spike and ADR resolve them.
