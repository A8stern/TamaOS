# Development process

## 1. Source of truth

- Repository documents hold stable requirements, architecture, hardware facts, and decisions.
- GitHub issues hold scoped work, acceptance criteria, unknowns, and hardware observations.
- Pull requests hold implementation discussion and verification evidence.
- Chat is a workspace, not the only copy of a decision.

## 2. Work item shape

Use `$tamaos-task-strategist` to create this shape when a request crosses domains, has unclear ownership, or needs sequencing. A narrow task may be routed directly to its owner.

Every implementation issue should contain:

```text
Outcome:
Acceptance criteria:
Known facts:
Unknowns / risks:
Architecture clearance: not-needed | aligned (<sources>) | user-decision-required
Host verification:
Hardware verification:
Out of scope:
```

If a task touches wiring, include the source for every pin and voltage claim and a pre-power continuity/voltage checklist.

Every new implementation capability goes from task strategy to the affected language architect before coding. If it fits accepted architecture, record `aligned` and the applicable sources. If it requires or contradicts an architectural decision, stop at `user-decision-required`, present the options to the user, and record the accepted decision in architecture documentation or an ADR before implementation.

## 3. GitHub flow

- Protect `main` once the remote repository exists.
- Use short-lived branches named `feat/...`, `fix/...`, `docs/...`, or `spike/...`.
- Keep pull requests small enough to review as one idea.
- Require passing checks and one review for firmware changes once CI is available.
- Prefer squash merging so one issue-sized change becomes one main-branch commit.
- Use draft pull requests for hardware experiments whose result is not yet known.
- Before pushing a branch, run the affected language profile's three required review skills in three independent reviewers for the exact commit and run `make prepush`.

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

`make prepush` runs `make ci` and validates local review evidence for the current commit. Evidence must name one language profile, three distinct actual skill IDs for its correctness, architecture, and verification-risk slots, and three distinct reviewer IDs. The architecture report must name the task clearance and accepted architecture sources used for comparison. A mismatch is blocking and returns to implementation; if it exposes a genuinely new decision, it returns to the user before the architecture can change. A missing or partial language profile blocks review; there is no generic fallback. The three reviews are intentionally local and must not be moved into GitHub Actions.

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

Role definitions and routing live in `docs/agents.md`. Unclear or multi-domain intake uses `$tamaos-task-strategist`; consequential design uses `$tamaos-architecture` plus each affected language architect; engineering-system work uses `$tamaos-engineer`; physical hardware work uses `$tamaos-hardware-engineer`; implementation uses `$tamaos-code` plus an applicable language skill; `$tamaos-code-review` owns the mandatory local review gate.

## 8. Next setup work

1. Run the Rust embedded toolchain spike and record the platform decision.
2. Register the real firmware adapter.
3. Add firmware-specific non-hardware checks to CI.
4. After parts arrive, create one bring-up issue per peripheral.
