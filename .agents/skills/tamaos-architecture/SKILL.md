---
name: tamaos-architecture
description: Coordinate consequential TamaOS design work through shared project principles and a concrete architect skill for every affected programming language. Use for boundaries, contracts, dependencies, runtime structure, and ADR decisions before implementation; not for ordinary code changes or post-commit architecture review.
---

# TamaOS Architecture

Coordinate architecture without pretending that one generic agent understands every language ecosystem. Apply the shared project principles, then route language decisions to each affected language's registered architect skill.

## Start architecture work

1. Read `docs/architecture.md`, `docs/architecture-principles.md`, applicable ADRs, and the task brief.
2. Identify the affected languages and resolve a concrete architect skill for each using [references/language-architect-contract.md](references/language-architect-contract.md).
3. Stop if an affected language has no architect profile. Name the missing capability; do not improvise a generic language architecture.
4. Give each language architect the same drivers, constraints, cross-language contracts, non-goals, and decision questions.
5. Reconcile their outputs at shared boundaries. One integration owner records accepted decisions in the canonical documents.

Use this workflow at the start of a real language project and for consequential changes with meaningful trade-offs or reversal cost. Ordinary implementation inside established boundaries does not require a new architecture pass.

## Expected result

Return or update only the artifacts the decision needs:

- architectural drivers and constraints;
- component ownership, dependency direction, and public contracts;
- language-specific runtime, error, concurrency, resource, dependency, and test-boundary decisions;
- considered alternatives and trade-offs;
- assumptions, validation plan, and revisit triggers;
- an ADR proposal when the decision is consequential.

Separate project-wide invariants from language-specific choices. A language architect may propose a deviation from a shared principle, but must state why, the cost, the evidence needed, and the revisit trigger.

## Boundaries

- Do not implement the design or choose syntax and style details.
- Do not own toolchain installation, CI, or repository mechanics; `$tamaos-engineer` owns those.
- Do not own product scope; `$tamaos-task-strategist` frames the task and routes it.
- Do not replace the architecture lane of `$tamaos-code-review`: design work happens before implementation, review checks an immutable commit afterward.
- Do not create frameworks, layers, or extension points for hypothetical future requirements.
