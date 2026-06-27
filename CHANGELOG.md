# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased] — v0.0.2 Roadmap

### Planned: instrumation digital twin integration
`instrumation-report` v0.0.2 will be the official report layer for the
**[instrumation](https://github.com/abduznik/instrumation)** digital twin platform.
Instead of constructing `Measurement` objects by hand you will be able to pass a
live twin handle and the library will pull readings, metadata, and state directly.

```python
# What the API will look like
from instrumation import DeviceTwin
from instrumation_report import Report

twin = DeviceTwin("psu-rack-01")
report = Report.from_twin(twin)          # header auto-populated from twin descriptor
report.run_sequence("voltage_rails")     # executes test sequence, captures readings
report.generate_html("result.html")      # measurements already attached
twin.push_results(report)                # write pass/fail back to twin state
```

Specific items:
- **`Report.from_twin(twin)`** — factory that reads `uut_name`, `uut_serial`,
  `revision`, and `extra_fields` from the instrumation device descriptor
- **`Report.run_sequence(name)`** — runs a named test sequence defined in the twin
  and attaches the resulting `Measurement` objects automatically
- **Streaming ingestion** — `twin.stream()` yields readings in real-time; report
  re-renders incrementally as they arrive
- **`twin.push_results(report)`** — writes the final PASS/FAIL summary back to the
  twin's live state for dashboard consumption
- **`generate_json()`** — machine-readable export for twin data pipelines and CI
  result aggregators

### Planned: PyVISA and ATE instrument adapters
A thin adapter layer so readings from real bench instruments and ATE racks flow
into `Measurement` objects without manual string parsing:

```python
from instrumation_report.adapters import visa, ate

# PyVISA — any GPIB/USB/LAN instrument
import pyvisa
rm = pyvisa.ResourceManager()
dmm = rm.open_resource("GPIB0::22::INSTR")
m = visa.measure(dmm, name="Output Voltage", unit="V",
                 query="MEAS:VOLT:DC?", condition=(11.8, 12.2))

# Generic ATE / ICT rack via socket or serial
m = ate.measure(rack, slot=3, channel=1, name="Continuity",
                condition=lambda r: r < 1.0)

report.add(m)
```

Specific items:
- **`instrumation_report.adapters.visa`** — wraps a `pyvisa.Resource`, sends a
  SCPI query string, parses the float response, returns a `Measurement`
- **`instrumation_report.adapters.ate`** — generic slot/channel abstraction for
  ICT and functional ATE racks (National Instruments, Keysight, Pickering, etc.)
- **`instrumation_report.adapters.serial`** — reads one line from a serial port
  (e.g. Arduino test jig) and parses it into a `Measurement`
- All adapters are optional extras so they don't pull in hardware SDKs for users
  who only need offline report generation
  (`pip install "instrumation-report[visa]"`, `[ate]`, etc.)

### Planned: General improvements
- `Measurement.timestamp` field for time-series test logs
- CSV export alongside Excel
- Custom HTML template support via `Report(template_path=...)`
- `--output` CLI entrypoint so reports can be generated without writing Python

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
