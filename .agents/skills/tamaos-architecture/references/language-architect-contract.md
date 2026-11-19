# Language architect contract

Every programming language used for implementation must provide its own concrete architect skill. The common architecture skill supplies project principles and cross-language coordination; it is not a fallback language architect.

## Required capability

A language architect must understand the selected language and ecosystem well enough to own:

- package/module boundaries and dependency direction;
- public contracts and representation boundaries;
- runtime, error, concurrency, ownership, memory, and resource models relevant to that language;
- dependency selection and ecosystem-specific structural costs;
- test seams, portability boundaries, and migration constraints.

Recommended names follow `<project>-<language>-architect`, but routing must use the actual installed skill ID rather than infer one from the language name.

## Initial language architecture

Before substantial implementation starts in a language, its architect reads the task brief, `docs/architecture.md`, `docs/architecture-principles.md`, applicable ADRs, and the real toolchain constraints. It then establishes the smallest sufficient language architecture:

```text
Language and runtime:
Drivers and constraints:
Module ownership and dependency direction:
Public contracts:
Error, concurrency, and resource model:
Dependency policy:
Test and portability boundaries:
Known deviations from shared principles:
Validation and revisit triggers:
```

Keep this as a maintained language architecture document once the language project exists. Do not create placeholder documents for languages that are not in use.

## Change work

Invoke the language architect again only when a change alters established boundaries, public contracts, runtime/resource policy, major dependencies, or another decision with meaningful reversal cost. Routine implementation follows the existing architecture.

For a multi-language decision, each architect owns only its language portion. The common coordinator owns the cross-language contract and makes conflicts explicit; it does not resolve them by silently overriding one architect.

## Registration

No language architect profile is registered yet. When a language agent is created, record its concrete architect skill alongside that language's implementation and review skills in the agent routing documentation. A missing profile blocks architecture work for that language.
