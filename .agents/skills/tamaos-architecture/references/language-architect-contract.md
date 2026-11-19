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

Invoke the language architect for every new implementation capability to confirm that it fits the established architecture, and whenever a change alters boundaries, public contracts, runtime/resource policy, major dependencies, or another decision with meaningful reversal cost. Routine fixes and internal refactors may follow the existing architecture without another pass.

For a multi-language decision, each architect owns only its language portion. The common coordinator owns the cross-language contract and makes conflicts explicit; it does not resolve them by silently overriding one architect.

## Review consultation

The language-specific architecture reviewer is independent from the design architect, but must review against the architect's recorded clearance and canonical architecture sources. When those sources are ambiguous, the reviewer asks the language architect to identify the applicable accepted decision; the architect may clarify the basis but may not retroactively waive a divergence.

If implementation differs from the clearance or accepted architecture, the reviewer returns a blocking finding containing:

```text
Architecture basis:
Observed implementation:
Mismatch:
Required correction or user decision:
```

If resolving the finding requires a new architectural choice, implementation stops and the choice returns to the user through the architecture coordinator.

## Registration

No language architect profile is registered yet. When a language agent is created, record its concrete architect skill alongside that language's implementation and review skills in the agent routing documentation. A missing profile blocks architecture work for that language.
