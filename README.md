# npm-export-witness

Resolve an explicit query matrix through a bounded exports-map subset, recording the matching subpath key and selected nested condition trace.

Built for javascript library maintainers reviewing an exports-map change. Condition order and a more-specific null pattern can change an entry point despite a plausible-looking package manifest.

## Quickstart

Python 3.10+; no runtime dependencies. The build uses setuptools from the official Python registry. This repository is the install source; no external registry release is claimed.

```sh
git clone https://github.com/nripankadas07/npm-export-witness.git
cd npm-export-witness
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/npm-export-witness example.json
```

On Windows, use `.venv\Scripts\python` and `.venv\Scripts\npm-export-witness`. Windows behavior has not been exercised; Linux CI is configured to verify Python 3.10, 3.12 and 3.14. An input filename or `-` for standard input is required. Valid analysis returns exit 0, including negative findings; malformed or unsupported input returns exit 2 and a JSON error on stderr. Input is bounded to 1 MiB; duplicate JSON keys and nonfinite numbers fail.

The runnable [example](example.json) uses synthetic data. Run `python npm_export_witness.py example.json` directly for a source-only demo. Import `analyze(data)` for the Python API; unsupported input raises an exception. The tool makes no network request or operational write.

## Input and output contract

Top level exports contains a string/null, a condition object, or a subpath object. Queries is an array of exactly subpath (dot or ./ path) and conditions (string array). JSON object key order is preserved. Targets start ./ and cannot contain dot, parent, node_modules, empty or encoded segments. Conditional numeric keys and mixed subpath/condition maps fail.

The example's installed behavior is asserted in [test_installed_cli.py](test_installed_cli.py). [Unit cases](test_behavior.py) cover positive decisions and meaningful failure cases. The report records actual captured evidence; absence of a finding does not certify an operational environment.

## Limits

Not a complete Node resolver. No arrays, legacy main/imports mapping, filesystem existence, symlinks, loader/module-format validation, query/hash URLs, percent-encoded paths, deprecated folder mappings or type compatibility. One star per pattern/target, depth 16, 256 entries/queries. Conditions are supplied explicitly; default always matches. Both import and require together fail. Unmatched nested conditions allow outer fallback; null blocks.

## Validation and research

Run `python -m unittest -v` and `python -m compileall -q npm_export_witness.py`. [Validation](VALIDATION.md) records exercised configurations. [Research and candidate brief](RESEARCH.md) compares current alternatives and states the inferred demand. No customer adoption or measured performance advantage is claimed.

## Contributing and support

[Contribution guide](CONTRIBUTING.md) · [Support](SUPPORT.md) · [Security](SECURITY.md) · [MIT license](LICENSE)

Original implementation developed with AI assistance and reviewed through acceptance tests. No competitor source, branding or prose was copied. Primary specifications informed the explicitly supported semantics.
