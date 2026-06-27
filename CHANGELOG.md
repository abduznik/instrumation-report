# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.0.1] — 2026-06-27

### Added
- `Measurement` dataclass with `name`, `value`, `unit`, `condition`, `test_number`, `expected`, `notes`, `description` fields
- `condition` supports range tuple `(lo, hi)`, callable/lambda, threshold float, or `None` (N/A)
- `Section` and `TestTable` for structured multi-section test plans
- `ReportHeader` for UUT metadata (engineer, serial, revision, custom `extra_fields`)
- `Report` class with `add()`, `add_section()`, `generate_html()`, `generate_excel()`, `generate_pdf()`
- HTML output via Jinja2 — self-contained file with PASS/FAIL badges and summary block
- Excel output via openpyxl — colour-coded rows, merged header, summary table
- PDF output via weasyprint (optional `[pdf]` extra) — A4 page breaks, page counter
- 47 tests across measurement, section, and report modules
- GitHub Actions CI: test matrix (Python 3.10/3.11/3.12), build, PyPI OIDC publish, gh-pages deploy
- 5-page documentation wiki with light/dark theme toggle
- Pyodide live playground (`try.html`) — library source embedded at build time, runs entirely in-browser
- RF Subsystem Validation example (HTML, Excel, PDF) in `examples/`

### Fixed
- `TestTable.sub_number` now defaults to `""` — `TestTable(title="X")` no longer raises `TypeError`
