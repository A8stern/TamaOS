# Development process

## 1. Source of truth

- Repository documents hold stable requirements, architecture, hardware facts, and decisions.
- GitHub issues hold scoped work, acceptance criteria, unknowns, and hardware observations.
- Pull requests hold implementation discussion and verification evidence.
- Chat is a workspace, not the only copy of a decision.

## 2. Work item shape

Every implementation issue should contain:

```text
Outcome:
Acceptance criteria:
Known facts:
Unknowns / risks:
Host verification:
Hardware verification:
Out of scope:
```

If a task touches wiring, include the source for every pin and voltage claim and a pre-power continuity/voltage checklist.

## 3. GitHub flow

- Protect `main` once the remote repository exists.
- Use short-lived branches named `feat/...`, `fix/...`, `docs/...`, or `spike/...`.
- Keep pull requests small enough to review as one idea.
- Require passing checks and one review for firmware changes once CI is available.
- Prefer squash merging so one issue-sized change becomes one main-branch commit.
- Use draft pull requests for hardware experiments whose result is not yet known.
- Before pushing a branch, complete the local three-reviewer gate for the exact commit and run `make prepush`.

Initial labels:

- `area:hardware`, `area:firmware`, `area:ui`, `area:pet`, `area:tooling`;
- `type:feature`, `type:bug`, `type:spike`, `type:decision`;
- `status:blocked-on-hardware`, `status:needs-verification`;
- `risk:electrical`, `risk:data-loss`.

## 4. Harness contract

The root `Makefile` is the stable command surface. It delegates to the language-agnostic runner in `harness/`; registered projects translate actions through their own executable `.harness` adapter:

```text
setup       install/check the pinned toolchain and targets
check       formatting + compile checks + portable tests
test        host-side tests
firmware    build the selected board profile
size        report firmware section sizes
flash       flash explicitly selected hardware
monitor     open serial logs
ci          all non-hardware checks used by GitHub Actions
```

`flash` must never run as part of `check`, `test`, or `ci`. Do not add placeholder commands before the toolchain spike determines the actual build path.

`make prepush` runs `make ci` and validates local review evidence for the current commit. The three reviews are intentionally local and must not be moved into GitHub Actions.

Register projects explicitly in `harness/projects`; never discover and execute arbitrary manifests recursively. The adapter contract and examples live in `harness/README.md`.

## 5. Definition of done

A change is done when:

- acceptance criteria are met;
- relevant host checks pass;
- hardware verification is either recorded or explicitly marked pending;
- assumptions and limitations are visible;
- architecture/docs changed with the code when needed;
- no unrelated refactor is mixed into the change.

## 6. Decision records

Create an ADR under `docs/decisions/` only for consequential choices with alternatives and a reversal cost. Use:

```text
# ADR-NNNN: Title
Status: proposed | accepted | superseded
Context:
Decision:
Consequences:
Validation / revisit trigger:
```

Expected early ADRs are the platform/runtime choice, persistence scheme, and memory/rendering strategy. Do not create ADRs for routine implementation details.

## 7. Agent collaboration

The primary agent owns the plan and integration. Delegate only independent research or review with a concrete deliverable. Good parallel work includes datasheet validation versus host-test design; overlapping edits to the firmware entry point are not good parallel work.

For every agent-produced result, the primary agent must verify the cited source or run the relevant check before merging it into project truth.

Role definitions and routing live in `docs/agents.md`. Engineering-system work uses `$tamaos-engineer`; physical hardware work uses `$tamaos-hardware-engineer`; implementation uses `$tamaos-code` plus an applicable language skill; `$tamaos-code-review` owns the mandatory local review gate.

## 8. Next setup work

1. Create the architecture agent.
2. Create the Rust language agent and run the toolchain spike.
3. Record the platform decision and register the real firmware adapter.
4. Add firmware-specific non-hardware checks to CI.
5. After parts arrive, create one bring-up issue per peripheral.
