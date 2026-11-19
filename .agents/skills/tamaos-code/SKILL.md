---
name: tamaos-code
description: Implement language-independent code changes in TamaOS. Use for application code, tests, refactors, and bug fixes; combine with the applicable language skill and complete the local three-reviewer gate before push.
---

# TamaOS Code

Own code changes from acceptance criteria through verified local commit. Use a language-specific skill for language and toolchain details when one exists.

## Workflow

1. Establish observable acceptance criteria, affected callers, risks, and non-goals.
2. Read the applicable `AGENTS.md` files and existing implementation before choosing an abstraction.
3. Make the smallest complete change, including affected tests, fixtures, configuration, and documentation.
4. Run the narrowest useful checks, then the applicable project harness commands.
5. Commit the complete change locally before review so every reviewer examines the same immutable SHA.
6. Invoke `$tamaos-code-review`. It must run the correctness, architecture, and verification review skills in three independent reviewers. Resolve every blocking finding; any new commit invalidates all earlier reviews and requires all three skills to run again.
7. Run `make prepush`. Push only after it passes.

## Ownership boundaries

- `$tamaos-engineer` owns the repository harness, CI, GitHub workflow, toolchains, and integration policy.
- The future architecture skill will own cross-component design choices and ADR recommendations.
- Language skills own language idioms, compiler/linter configuration, dependency details, and language-specific testing.
- This skill owns implementation completeness and the handoff into local review.

Do not bypass the review gate, represent CI as a substitute for independent review, or infer permission for external writes.
