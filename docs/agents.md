# Agent architecture

TamaOS uses small project skills as specialist roles. `AGENTS.md` contains rules that apply broadly; skills load only when their domain is relevant.

## Roles

### Primary agent

Owns the user request, scope, integration, permissions, and final result. It decides whether a specialist is useful and verifies specialist output before it becomes project truth.

### Task strategist

Invoke `$tamaos-task-strategist` at the start of a new, ambiguous, multi-domain, or sequencing-heavy request. It turns the goal into acceptance criteria, unknowns, work boundaries, a specialist route, dependencies, and verification evidence.

It is language-independent and sits before implementation. It may route work to the engineer, hardware engineer, common code agent plus a language agent, review coordinator, or a future specialist such as architecture or security/safety. It names a missing capability instead of inventing a skill that is not installed.

The strategist returns an execution brief to the primary agent. It does not implement, review, mutate external systems, or become the integration owner. An already narrow task with an obvious owner can bypass it.

### TamaOS Engineer

Invoke `$tamaos-engineer` for engineering-system questions: repository structure, harness, CI, GitHub workflow, toolchains, architectural decision process, and reliability.

Its skill lives at `.agents/skills/tamaos-engineer/`. Its system map is maintained in the repository so another session can reconstruct the engineering environment without relying on chat history.

### Hardware engineer

Invoke `$tamaos-hardware-engineer` for physical components, datasheets, pin and voltage evidence, power distribution, GPIO selection, wiring tables, measurements, and peripheral bring-up.

It owns the electrical contract and physical verification, not firmware implementation. It must distinguish observed, specified, seller-claimed, and assumed facts; a diagram remains planned until the exact assembly is tested.

### Common code agent

Invoke `$tamaos-code` for language-independent implementation behavior: acceptance criteria, affected callers, minimal complete changes, tests, and handoff into review. Pair it with the applicable language skill.

Every committed change must use `$tamaos-code-review` before push. It is only the coordinator. The affected programming language must provide a complete review profile containing three distinct skills with non-overlapping ownership:

- correctness: language semantics, behavior, and regressions;
- architecture: language/ecosystem boundaries and structural cost;
- verification-risk: native checks, evidence, and non-functional risk.

These are contracts for future language-specific skills, not generic TamaOS review skills. For example, the Rust profile will later name three actual Rust review skills; Python or TypeScript profiles may name different ones. Do not invent a fallback or pass a partial profile.

The reviewers inspect the same commit independently, do not see one another's reports, and may not substitute one general review for the three required skills. Local evidence records the language, actual skill ID, and reviewer identity. Evidence plus `make ci` is enforced by `make prepush`; CI does not perform agent review. The complete contract lives in `.agents/skills/tamaos-code-review/references/language-review-contract.md`.

### Architecture coordinator and language architects

Invoke `$tamaos-architecture` for consequential design work before implementation. It applies the shared principles in `docs/architecture-principles.md`, identifies affected languages, and requires one concrete architect skill per language. It coordinates cross-language contracts but is not itself a generic language architect.

Each language architect owns idiomatic module boundaries, public contracts, runtime/error/concurrency/resource policy, dependency choices, and test seams for that language. No language architect is registered yet; the Rust language role will provide the first one. Missing language architecture must remain visible rather than being filled with a generic prompt.

Architecture design and architecture review are separate. The language architect shapes a design before implementation; the architecture lane in the three-review gate independently checks the resulting immutable commit.

### Future language agents

Will add language-specific implementation knowledge, commands, one architect skill, and a complete three-skill review profile. The first planned language role is Rust. A language agent must use the common code and architecture contracts plus the project `.harness` adapter rather than creating another workflow.

## Delegation contract

A specialist assignment should include:

- concrete outcome;
- bounded scope and non-goals;
- relevant sources;
- expected evidence or artifact;
- permission boundaries for writes and external actions.

Specialists should not edit overlapping files in parallel. The primary agent owns integration.

## Knowledge boundaries

- Rules that should affect nearly every repository task belong in `AGENTS.md`.
- Role-specific decision guidance belongs in that role's `SKILL.md`.
- Detailed role knowledge belongs in the skill's `references/` directory.
- Product and engineering facts remain in their canonical repository documents and are linked, not copied into every role.
- Temporary progress belongs in GitHub issues and pull requests.
