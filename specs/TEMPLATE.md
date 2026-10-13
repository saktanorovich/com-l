# Spec: [Feature Name]

**Feature Slug**: `feature-name-in-kebab-case`
**Status**: Draft | Ready | In Progress | Done

---

## Tech Stack

| Concern         | Choice                           |
|-----------------|----------------------------------|
| Language        |                                  |
| Runtime/Version |                                  |
| Framework       | (or "none" if not applicable)    |
| Test Framework  |                                  |
| Package Manager |                                  |

---

## Description

[One or two paragraphs describing what this feature does and why it exists.
Write this for a developer who has never seen the project. Avoid
implementation details — describe behavior and purpose.]

---

## Requirements

Write each requirement as a user story:

- As a [type of user], I want [goal] so that [reason].
- As a [type of user], I want [goal] so that [reason].

---

## Acceptance Criteria

Each item here will become one or more tests. Be specific and measurable.

- [ ] [Criterion 1 — describe exact expected behavior or output]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Test Approach

**Primary approach**: Unit | Integration | E2E | (combination — explain)

**What to test**:
- [Describe the key behaviors / code paths that must be tested]

**What not to test**:
- [External services, third-party libraries, obvious language behavior, etc.]

**Test infrastructure** (fill in for Node.js/Jest projects — agents use these exactly, no invention):
- Test file naming: [e.g. `game-state.test.js` — kebab-case matching the source file name]
- Jest config: `jest.config.cjs` in `src/<slug>/` (CommonJS `.cjs` extension required when source is ESM)
- ESM package scope: `tests/<slug>/package.json` must contain `{ "type": "module" }`
- Run command: `cd src/<slug> && node --experimental-vm-modules node_modules/jest/bin/jest.js --config jest.config.cjs`
- Jest location: root `node_modules/` (installed once at repo root, not per-feature)
- Expected test count: [fill in after writing tests, e.g. "~50 tests across 13 describe blocks"]

---

## Smoke Test

**How to verify the feature runs end-to-end (not just that tests pass):**

- **Start command**: [e.g. `open index.html in browser`, `node src/server.js`, `npx serve src/`]
- **Expected result**: [describe the visible/measurable result that confirms the feature actually works — e.g. "Canvas renders at 800×600 with alien grid visible", "curl returns HTTP 200 with JSON body"]
- **Failure this catches**: [e.g. "blank page due to module import error", "process exits immediately", "missing route returns 404"]

The smoke test is the minimal manual check that the feature starts and does something observable.
It complements unit tests — a feature that passes all tests but shows a blank page is not done.

**Agent verification limit**: Agents can confirm HTTP responses and the absence of JS/import errors,
but cannot see visual output (canvas, rendered UI, pixel art). For browser/canvas features, choose one:
- Add a machine-checkable signal: e.g. `console.log('SMOKE_OK')` on first successful render frame,
  so the tech-lead can grep server logs or browser console output for it.
- Or explicitly state: "Human visual confirmation required — agent marks PASSED after confirming
  HTTP 200 for all modules and zero console errors."

---

## Constraints

- [Hard technical constraint, e.g. "must not use external HTTP libraries"]
- [Environment constraint, e.g. "must run on Node.js 20 LTS"]
- [Performance constraint, e.g. "must respond in under 100ms for inputs < 1MB"]

---

## Out of Scope

The following will NOT be implemented as part of this spec:

- [Feature or behavior explicitly excluded]
- [Edge case deferred to a future spec]
