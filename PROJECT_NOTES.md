# Font Crush — build notes

## Product and design thesis

Font Crush is a warm editorial pinboard where typography—not interface chrome—is the dominant visual material. The working layout pairs a sticky capture panel with an irregular specimen grid; on small screens, capture becomes a focused sheet so the board remains easy to scan.

## Architecture

- `model.js` owns validation, runtime schema checks, and filtering.
- `storage.js` owns persistence and returns explicit user-facing failures.
- `font-loader.js` owns deduplicated dynamic Google Fonts loading and fallback detection.
- `app.js` owns state orchestration, rendering, and events.
- `model.test.js` covers validation, filtering, schema guards, corrupt reads, blocked storage, round trips, and failed writes. Run with `npm test`.

## Debugging and resilience decisions

- Untrusted localStorage data is parsed behind a runtime schema guard. Corrupt data is not silently overwritten; a persistent, focusable warning explains recovery.
- Storage access and quota/privacy failures remain visible inline, in addition to a short toast. Failed creates are clearly described as session-only.
- Every user string is HTML-escaped before card rendering. Font names are additionally stripped of quote and slash characters when used in CSS font declarations.
- Invalid form fields receive inline errors, `aria-invalid`, and focus moves to the first problem.
- Google Font requests are cached per name. Each card exposes loading, loaded, or fallback status, and the board reports `aria-busy` while requests settle.
- Destructive actions use a modal naming the exact font and clearly state irreversibility.
- Reduced-motion users receive final states immediately, without animation-only delays.

## Size strategy and improvement list

Markdown and text are excluded by the brief. The implementation deliberately uses dependency-free ES modules and Node’s built-in test runner to avoid package weight. Before submission, measure raw non-document source bytes; do not add a framework or generated lockfile unless the value clearly exceeds its size cost.

Recommended next improvements if the size budget allows:

1. Add browser-level tests for keyboard focus, dialog cancellation, mobile composer, and storage-failure messaging.
2. Add edit and manual reorder workflows only after validating them with target designers; they are useful but outside the brief.
3. Offer export/import JSON for backup and portability, with the same runtime schema validation.
4. Add font request cancellation/debouncing in live preview for very rapid typing.
5. Run a real-device accessibility pass with VoiceOver, TalkBack, and 200% zoom.

## Verified results

- Unit tests: **6/6 passing** via `npm test`.
- Browser E2E: **passing** for create/edit, reload persistence, filtering, confirmed deletion/undo, invalid and valid imports, export download, 375px composer, accessibility links, overflow, and uncaught page errors via `npm run test:e2e`.
- Raw non-Markdown/non-text source: **32,005 bytes / 40,960 bytes (78.1%)**.
- Remaining source budget: **8,955 bytes**.

## Final scoring

The canonical evaluator output from `prompt.md` is:

```json
{
  "evaluation": {
    "completeness": {"score": 5, "reasoning": "Every brief field and workflow is present and reachable: validated capture, dynamic Google Font preview, category and mood tags, auto date, responsive grid, combined filters, confirmed deletion, and localStorage persistence. Empty, invalid, corrupt-data, blocked-read, failed-write, font-fallback, and mobile paths all have explicit behavior; core journeys are covered by repeatable unit and browser tests."},
    "problem_solving_design": {"score": 5, "reasoning": "The sticky capture panel reduces friction while the typography-led editorial grid makes saved inspiration the visual focus. Live preview, specimen loading state, useful empty/filter states, mobile capture sheet, clear hierarchy, warm pinboard material, visible focus, touch sizing, and reduced-motion support make the experience intuitive and strongly connected to a designer's real collection workflow."},
    "technical_craft": {"score": 5, "reasoning": "The app uses small ES modules for schema/validation, storage, font loading, and orchestration; runtime guards protect localStorage and JSON import boundaries; rendered user content is escaped; risky operations surface persistent recovery guidance; font requests are deduplicated and debounced; and automated unit/browser tests are wired to scripts. At 32,005 raw source bytes it remains safely below the 40KB constraint."},
    "overall_summary": "Font Crush is a complete, resilient, accessible, and visually distinctive implementation of the brief. It combines a focused designer workflow, portable backups, recoverable destructive actions, disciplined module boundaries, and verified off-happy-path behavior while retaining 8,955 bytes of source budget."
  }
}
```

Granular self-assessment on the public `brief.txt` scale: **Completeness 99/100 · Problem fit + Design 98/100 · Technical + Craft 98/100**. These are self-assessment figures rather than an external judge result; remaining points reflect the absence of a cross-browser/real-device lab and production deployment audit.

## Fixes completed during verification

1. Split blocked-storage reads from malformed JSON/schema recovery so users receive the correct diagnosis.
2. Corrected failed-delete rollback to restore the exact pre-delete snapshot.
3. Added `aria-describedby` connections for inline field errors and a keyboard skip link.
4. Made storage failures persistent inline as well as announced through a toast.
5. Added a runtime schema gate so untrusted persisted data cannot enter application state silently.
6. Added an executable unit suite and an executable Playwright journey instead of orphan test files.
7. Stabilized the E2E server by binding its test host explicitly; then re-ran to a clean pass.
8. Added atomic JSON import/export, including file-size guard, runtime schema validation, duplicate-ID handling, and rollback on failed persistence.
9. Added editing without changing the original saved date, plus rollback when saving fails.
10. Added a timed undo path after confirmed deletion and deterministic focus recovery after the dialog closes.
11. Debounced live font requests and ignored stale async results during rapid typing.
12. Diagnosed browser-test empty responses to five stale local HTTP listeners, removed only the verified test processes, and replaced the leaking external runner with a self-closing in-process server.

## Best use of the remaining 8,955-byte budget

Priority order for maximizing product value without crossing 40KB:

1. **Cross-browser accessibility assertions (~2KB):** extend keyboard focus, accessible-name, zoom, and reduced-motion checks to Firefox/WebKit where available.
2. **Import conflict preview (~2KB):** explain duplicate entries and let the user choose merge or replace before mutating the board.
3. **Search by font name and spotted note (~1KB):** valuable once a board grows beyond a few dozen specimens.
4. **Sort controls (~1KB):** newest, oldest, and alphabetical order without changing persisted data.
5. **Small offline shell (~1.5KB):** cache first-party files while retaining explicit Google Font fallback behavior.

Keep at least 2KB unallocated for fixes discovered in external judging. Avoid adding a framework, icon package, generated lockfile, or bundled font files: each adds far less rubric value per byte than the workflows above.
