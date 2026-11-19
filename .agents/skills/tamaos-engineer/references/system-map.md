# TamaOS engineering system map

Use this as an index, not as a substitute for inspecting live state. When this file disagrees with the repository or GitHub, verify the live state and update this map in the same change.

## Sources of truth

| Concern | Canonical source |
|---|---|
| Repository-wide agent rules | `AGENTS.md` |
| Agent roles and routing | `docs/agents.md` |
| Product and firmware boundaries | `docs/architecture.md` |
| Development and GitHub process | `docs/development-process.md` |
| Harness contract | `harness/README.md` |
| Registered executable projects | `harness/projects` |
| Hardware facts and unknowns | `docs/tamagotchi-components.md` |
| Work scope and temporary status | GitHub issue or pull request |
| Observed automated verification | local command output and GitHub Actions |

## Current topology

- Repository: public `A8stern/TamaOS` on GitHub.
- Default branch: `main`.
- `main` requires a pull request and the `ci` status check, including for administrators.
- Linear history and conversation resolution are required; force-push and branch deletion are disabled.
- No approving review is currently required, so the owner can merge a passing solo pull request.
- Merge convention: squash one issue-sized change into one `main` commit.

Verify live GitHub settings before claiming they still hold.

## Command and CI path

```text
human / agent / CI
        |
        v
    root Makefile
        |
        v
    harness/run
      |       |
      |       `-> registered <project>/.harness adapters
      `-> repository checks and harness unit tests
```

The stable root commands are `make setup`, `make check`, `make test`, `make build`, and `make ci`. Hardware operations require an explicit project. `flash` and `monitor` must never run from CI.

The project registry is currently empty because no firmware workspace or verified toolchain exists yet. The first real project is expected to be the ESP32-S3 firmware after the toolchain spike.

GitHub Actions runs `make ci` on pushes and pull requests targeting `main`.

## Current agent routing

- `$tamaos-engineer`: engineering system, integration, architecture process, toolchains, CI, GitHub, and hardware bring-up process.
- Future common code agent: language-independent implementation and review rules.
- Future language agents: language/toolchain-specific implementation, beginning with Rust.

The primary agent owns integration and user communication. A specialist returns evidence and recommendations; it does not silently expand scope or mutate external systems.
