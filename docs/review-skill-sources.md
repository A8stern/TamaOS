# Review skill sources

The local review gate uses three separately discoverable TamaOS skills. Each is a narrow adaptation of an MIT-licensed public skill, pinned here so its origin and the chosen behavior remain auditable.

| Local skill | Upstream | Pinned revision | Adopted method | Deliberately excluded |
|---|---|---|---|---|
| `$tamaos-review-correctness` | [felipereisdev/code-review-skill](https://github.com/felipereisdev/code-review-skill) | `c4cd79a50acf33f0451655344bd8f52a7b5f077b` | Evidence-driven diff review, concrete trigger/effect, candidate refutation | Architecture, test sufficiency, publishing, fixes, stack-specific bulk |
| `$tamaos-review-architecture` | [JuanMarchetto/architecture-reviewer-skill](https://github.com/JuanMarchetto/architecture-reviewer-skill) | `ab0b1c68cdf96633eaa49a651dbc957ebf55b0a1` | Compare documented architecture with actual dependencies and responsibilities | Whole-repository scoring, doc generation, automatic edits |
| `$tamaos-review-verification` | [obra/superpowers: verification-before-completion](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) | `22f0b463e7a5e579904dd6211a520321035526f7` | Fresh evidence before completion claims | Correctness and architecture judgment |

The adaptations are intentionally separate rather than three copies of a general code-review prompt. Repository rules and each local `SKILL.md` define their non-overlapping authority and common evidence schema.

## License notices

All three upstream works use the MIT License.

Copyright (c) 2026 Felipe Reis

Copyright (c) 2026 Juan Marchetto

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notices and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
