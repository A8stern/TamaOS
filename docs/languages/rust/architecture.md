# Rust architecture

Status: initial language architecture and clearance for the portable domain scaffold.

## Language and runtime

- Rust is the implementation language.
- Portable domain code is `no_std` and does not allocate by default.
- The ESP runtime, target, allocator, async executor, and flashing stack remain unresolved until the toolchain spike and platform ADR.

## Ownership and dependency direction

```text
apps/firmware -> portable domain/UI + service contracts <- board/driver adapters
```

The initial `tama-domain` crate owns deterministic types and rules only. It cannot depend on board, driver, rendering, storage, or runtime crates. Firmware and additional crates are created only when a real vertical slice needs them.

## Contracts and failures

- Semantic events cross the input boundary; GPIO edges and debounce state stay in adapters.
- Elapsed time is passed explicitly.
- Expected runtime failures use explicit result/error types once fallible behavior exists.
- Panics, unchecked unsafe code, and hidden global mutable state are not application contracts.

## Dependencies and verification

The initial domain crate has no third-party dependencies. Host formatting, Clippy, tests, and build are required through its `.harness` adapter. Hardware evidence remains separate and pending.

## Current architecture clearance

Architecture status: `aligned`.

The minimal workspace, portable `tama-domain` crate, and semantic input event types implement boundaries already accepted in `docs/architecture.md`. This clearance does not decide the ESP platform/runtime or authorize hardware-specific code.
