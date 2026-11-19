# TamaOS agent rules

## Project goal

TamaOS is a desktop virtual-pet and mini-console built on an ESP32-S3-DevKitC-1 N16R8 and written in Rust. The first milestone is a safe, breadboard-based prototype with an ST7789V display, rotary encoder, buttons, and a passive buzzer.

## Context routing

- Use `$tamaos-engineer` for repository structure, harness, CI, GitHub workflow, toolchains, architecture process, or engineering reliability.
- Use `$tamaos-hardware-engineer` for components, datasheets, power, signals, GPIO selection, wiring, measurements, and physical bring-up.
- Use `$tamaos-code` for implementation, tests, refactors, and bug fixes. Combine it with the applicable language skill.
- Before any push, use `$tamaos-code-review` to run the affected language's registered correctness, architecture, and verification review skills in three independent local reviewers, then run `make prepush`. A complete language review profile is required; CI does not replace this gate.
- Read `docs/architecture.md` when changing firmware boundaries or making an architectural decision.
- Read `docs/development-process.md` when changing the contribution or verification workflow.
- Read `harness/README.md` when changing commands or registering a project.
- For hardware work, use `$tamaos-hardware-engineer` and read `docs/tamagotchi-components.md`.
- Agent roles and delegation boundaries are documented in `docs/agents.md`.

## Non-negotiable rules

- Do not invent pinouts, GPIO assignments, voltage requirements, or module markings. Treat them as unknown until verified on the received hardware.
- Never present an untested wiring diagram as verified. Mark assumptions and the exact physical check that resolves them.
- Keep 3.3 V GPIO logic separate from 5 V power. All grounds must be common.
- Prefer the smallest implementation that proves the next milestone. Do not build a plugin system, scheduler, allocator-heavy UI framework, or dynamic game loader before a real requirement needs it.
- Keep hardware-specific code at the boundary. Pet rules, menu transitions, and persistence policy must be testable without the board.
- New dependencies need a short reason and should support `no_std` unless the selected platform architecture explicitly changes.
- Do not silently replace ordered hardware or change the product scope.

## Change workflow

1. Restate the acceptance criteria and unknowns.
2. Inspect existing code and decisions before proposing a new abstraction.
3. Make one coherent change at a time.
4. Run the relevant harness commands documented in `docs/development-process.md`.
5. Commit locally, complete the three-lane review for that exact SHA, and run `make prepush` before pushing.
6. Report what was verified on the host, what was verified on hardware, and what remains assumed.

## Architecture boundaries

Application logic depends on contracts, not concrete ESP drivers. The firmware composition root connects the layers:

```text
apps/firmware -> domain + UI + service contracts <- board / driver adapters
```

- `board`: pins, clocks, buses, timers, and board initialization.
- `drivers`: display, encoder/buttons, buzzer, and persistence adapters.
- `services`: input events, time, rendering, audio commands, and storage API.
- `domain`: deterministic pet state and rules.
- `ui`: screens, navigation, and view models; rendering is a separate adapter.
- `apps`: composition root and the main event loop.

Domain code must not depend on ESP-specific crates.

## Agent roles

Use extra agents only for independent, bounded work with an explicit output. Useful roles are:

- hardware researcher: datasheets, electrical constraints, and unresolved pinout questions;
- firmware implementer: one driver or vertical slice;
- test reviewer: host tests, failure cases, and hardware verification checklist;
- architecture reviewer: dependency direction, unnecessary abstraction, and ADR consistency.

One agent owns integration. Parallel agents must not edit the same files.

## Documentation policy

- Stable project truth belongs in the repository, not only in chat.
- Architectural decisions go in `docs/decisions/` once a choice is made and has meaningful trade-offs.
- Temporary task status belongs in the GitHub issue or pull request.
- Update documentation in the same change that invalidates it.
