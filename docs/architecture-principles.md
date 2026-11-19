# Shared architecture principles

Status: initial principles; confirm them against real constraints when each language project starts.

These principles are common input for every language architect. They guide decisions but do not force identical module layouts or patterns across languages.

## Start from drivers

Write down the required behavior, quality attributes, hardware/runtime constraints, non-goals, and unknowns before choosing structure. Do not use a familiar pattern without a driver that needs it.

## Keep decisions at the right level

Project-wide documents own product boundaries and cross-language contracts. Each language architect owns the idiomatic implementation architecture inside those boundaries. A language-specific limitation may justify a documented deviation rather than weakening the shared rule for every language.

## Make ownership and dependency direction explicit

Every meaningful component should have one responsibility and a clear dependency direction. Application/domain behavior depends on contracts; hardware, frameworks, storage, transport, and other volatile details remain at adapters or composition roots.

## Build the smallest reversible structure

Design for the next proven milestone. Add a layer, abstraction, extension point, or shared framework only when a current requirement or measured constraint needs it. Prefer decisions that are cheap to reverse while facts are still uncertain.

## Preserve testable behavior

Keep deterministic rules and policy independent from clocks, I/O, hardware, frameworks, and global state where practical. Define failure ownership and test seams as part of the architecture rather than after implementation.

## Use evidence and revisit triggers

Separate facts, assumptions, and provisional recommendations. Performance, memory, binary-size, hardware, and operational claims need a measurement plan. Consequential decisions record alternatives, trade-offs, validation, and a concrete reason to revisit them.

## Language-start checkpoint

Before substantial work begins in a programming language, its architect must:

1. confirm the applicable shared principles and project constraints;
2. define language-specific module, contract, error, concurrency, resource, dependency, and testing policies;
3. record deviations and unknowns;
4. propose ADRs only for decisions with meaningful trade-offs and reversal cost.

The language architect contract lives in `.agents/skills/tamaos-architecture/references/language-architect-contract.md`.
