# instrumation-report

A lightweight Python library for generating structured UUT (Unit Under Test) test reports from measurement data. Outputs HTML, Excel, and PDF. Works standalone or alongside the [`instrumation`](https://github.com/abduznik/instrumation) library.

## Install

```bash
pip install instrumation-report

# PDF support (requires weasyprint system deps — see weasyprint docs)
pip install "instrumation-report[pdf]"
```

## Quick start

```python
from instrumation_report import Report, ReportHeader, Section, TestTable, Measurement

report = Report(header=ReportHeader(
    title="RF Subsystem Validation",
    subtitle="Production Test",
    engineer="Yan",
    uut_name="Signal Analyzer Module",
    uut_serial="SN-2024-001",
    revision="A",
))

section = Section(number="1", title="Voltage Tests")
table = TestTable(title="Power Supply Checks", sub_number="1.1")
table.add(Measurement("3.3V Rail", 3.31, "V", condition=(3.2, 3.4), test_number="1.1.1", expected="3.2-3.4V"))
table.add(Measurement("5V Rail",   5.02, "V", condition=(4.9, 5.1), test_number="1.1.2", expected="4.9-5.1V"))
section.add_table(table)
report.add_section(section)

report.generate_html("report.html")
report.generate_excel("report.xlsx")
report.generate_pdf("report.pdf")   # requires [pdf] extra
```

## Condition types

| Type | Example | Passes when |
|------|---------|-------------|
| Range tuple | `(1.0, 5.0)` | `lo <= value <= hi` |
| Lambda | `lambda v: v > 4.0` | callable returns `True` |
| Threshold float | `3.0` | `value >= threshold` |
| `None` | _(omit)_ | always N/A |

## Flat usage (simple reports)

```python
r = Report()
r.add(Measurement("Voltage", 4.7, "V", condition=(4.0, 5.0)))
r.add(Measurement("Current", 1.2, "A", condition=lambda v: v < 2.0))
r.generate_html("report.html")
```

## API

### `ReportHeader`

| Field | Type | Default |
|-------|------|---------|
| `title` | `str` | _(required)_ |
| `subtitle` | `str` | `""` |
| `engineer` | `str` | `""` |
| `uut_name` | `str` | `""` |
| `uut_serial` | `str` | `""` |
| `revision` | `str` | `""` |
| `date` | `str` | today (ISO 8601) |
| `extra_fields` | `dict` | `{}` |

### `Measurement`

| Field | Type | Default |
|-------|------|---------|
| `name` | `str` | _(required)_ |
| `value` | `float` | _(required)_ |
| `unit` | `str` | `""` |
| `condition` | lambda / tuple / float / None | `None` |
| `test_number` | `str` | `""` |
| `expected` | `str` | `""` |
| `notes` | `str` | `""` |
| `description` | `str` | `""` |

### `Section(number, title, subtitle="")`
- `add_table(table: TestTable)`

### `TestTable(title, sub_number)`
- `add(measurement: Measurement)`

### `Report(header=None)`
- `add_section(section: Section)`
- `add(measurement)` — flat backwards-compatible usage
- `generate_html(path)`
- `generate_excel(path)`
- `generate_pdf(path)` — requires `[pdf]` extra

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
pytest -v
```

## License

MIT
