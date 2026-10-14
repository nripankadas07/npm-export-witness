# Candidate brief and comparison — 14 October 2026

**User:** JavaScript library maintainers reviewing an exports-map change. **Painful task:** Condition order and a more-specific null pattern can change an entry point despite a plausible-looking package manifest.

**Smallest useful capability:** Resolve an explicit query matrix through a bounded exports-map subset, recording the matching subpath key and selected nested condition trace.

**Acceptance:** the supplied synthetic example must produce the documented installed result; core edge cases and invalid-input paths must pass; a wheel installed outside the checkout must run the CLI and reject malformed input. The public default commit, remote matrix CI and rendered documentation must be verified before LIVE.

**Demand evidence:** inferred from the workflow and relevant accessible documentation/issues, not a verified customer request. **Discovery path:** descriptive repository topics, a runnable example, searchable edge-case documentation and the user's chronological portfolio index. No unsolicited promotion is performed.

**Distinctness:** wheel-sentinel verifies Python distribution contents and dep-audit checks dependencies; this project explains JavaScript export dispatch. It neither bundles code nor duplicates the portfolio generic configuration tools.

## Current comparables

privatenumber/pkgroll is the highest-star relevant comparable found on the package exports results page, with a different bundling workflow. Focused conditional exports search also returned resolve-pkg-maps; search coverage is limited, not exhaustive. Queries were executed live on GitHub with Sort by Most stars. Search result coverage is bounded to visible first pages, then relevant established repositories; stars inform discovery, not quality or performance.

| Repository | Stars observed | Latest push observed UTC | License metadata | Observation UTC |
| --- | ---: | --- | --- | --- |
| [privatenumber/pkgroll](https://github.com/privatenumber/pkgroll) | 1564 | 2026-10-05T19:42:05Z | NOASSERTION | 2026-10-14T06:09:38.340Z |
| [publint/publint](https://github.com/publint/publint) | 1308 | 2026-10-01T18:00:55Z | MIT | 2026-10-14T06:09:38.332Z |
| [lukeed/resolve.exports](https://github.com/lukeed/resolve.exports) | 402 | 2026-10-12T22:33:09Z | MIT | 2026-10-14T06:09:38.284Z |

pkgroll builds artifacts from exports-defined entry points, publint diagnoses packaging errors, and resolve.exports is a configurable resolver. Those tools remain appropriate for bundling and broader correctness; this MVP provides an offline Python query receipt with a declared smaller grammar.

Comparables' current READMEs, installation examples and accessible issues were inspected. Established tools supply broader integration, docs and community support; this project's support consists of reproducible GitHub reports, source tests and explicit bounded semantics. Its clean install has no runtime dependencies, but that alone establishes no time-to-first-result or reliability advantage. Comparator install success and benchmark performance were not measured. License metadata marked NOASSERTION is unresolved metadata, not a permissive-reuse claim. No reuse was needed.

[Primary behavior reference](https://nodejs.org/api/packages.html#conditional-exports). Competitor README blob hashes, exact star query URLs and source observations are retained in the dated profile research receipt. A local success proves our example, not absence of the behavior in a competitor. Negative results and unsupported configurations remain visible; no superiority claim is made.
