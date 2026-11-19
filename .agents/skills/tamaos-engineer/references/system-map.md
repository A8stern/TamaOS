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
| Registered language review profiles | `harness/review-profiles.json` |
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

The stable root commands are `make setup`, `make check`, `make test`, `make build`, and `make ci`. `make review` validates three local review reports and `make prepush` combines that gate with `make ci`. Hardware operations require an explicit project. `flash` and `monitor` must never run from CI.

`make setup` enables the tracked local pre-push hook. Review evidence is stored under ignored `.harness-state/` and is never produced by CI.

The project registry is currently empty because no firmware workspace or verified toolchain exists yet. The first real project is expected to be the ESP32-S3 firmware after the toolchain spike.

GitHub Actions runs `make ci` on pushes and pull requests targeting `main`.

## Current agent routing

- `$tamaos-engineer`: engineering system, integration, architecture process, toolchains, CI, and GitHub.
- `$tamaos-hardware-engineer`: component identification, electrical constraints, wiring, GPIO selection, measurements, and physical bring-up.
- `$tamaos-code`: language-independent implementation and test completeness.
- `$tamaos-code-review`: coordinator and common contract for three independent local review slots required before push.
- Future language agents: language/toolchain-specific implementation and three concrete review skills, beginning with Rust.

No language review profile is registered yet. Until the Rust agent supplies all three actual skill IDs, the local review gate is intentionally incomplete and must not fall back to generic review prompts.

The primary agent owns integration and user communication. A specialist returns evidence and recommendations; it does not silently expand scope or mutate external systems.
