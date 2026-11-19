# Harness

The root `Makefile` is the stable entry point for humans, agents, and CI. The harness itself is intentionally language-agnostic.

## Commands

```sh
make setup
make check
make test
make build
make ci
```

Hardware actions require an explicit project so they cannot accidentally target every registered device:

```sh
make firmware PROJECT=firmware
make size PROJECT=firmware
make flash PROJECT=firmware
make monitor PROJECT=firmware
```

## Registering a project

Add one tab-separated line to `harness/projects`:

```text
firmware<TAB>apps/firmware
```

The project directory must contain an executable `.harness` script. It receives one action and translates it into the native commands for that project:

```sh
#!/bin/sh
set -eu

case "$1" in
  setup)    rustup show ;;
  check)    cargo fmt --check && cargo clippy --all-targets -- -D warnings ;;
  test)     cargo test ;;
  build|firmware) cargo build --release ;;
  size)     cargo size --release -- -A ;;
  flash)    cargo run --release ;;
  monitor)  espflash monitor ;;
  *)        echo "unsupported action: $1" >&2; exit 2 ;;
esac
```

This snippet is illustrative, not the TamaOS firmware configuration. Pin the actual Rust target and flashing commands after the toolchain spike.

Keep language-specific behavior inside the project adapter. Extract a shared adapter only after two real projects need the same implementation.
