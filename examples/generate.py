"""
Example: RF Subsystem Validation Report
Generates report.html, report.xlsx, and report.pdf in this directory.
Run from the repo root:  python examples/generate.py
"""
from pathlib import Path
from instrumation_report import Report, ReportHeader, Section, TestTable, Measurement

OUT = Path(__file__).parent

report = Report(header=ReportHeader(
    title="RF Subsystem Validation",
    subtitle="Production Test — Board Rev A",
    engineer="Abduznik",
    uut_name="Signal Analyzer Module",
    uut_serial="SN-2024-001",
    revision="A",
    extra_fields={"Batch": "LOT-88B", "Test Station": "TS-02"},
))

# ── Section 1: Power Supply ───────────────────────────────────────────────

s1 = Section(number="1", title="Power Supply Checks",
             subtitle="DC rail validation at nominal load")

t1 = TestTable(title="Voltage Rails", sub_number="1.1")
t1.add(Measurement("3.3V Rail",  3.31,  "V", condition=(3.2,  3.4),
                   test_number="1.1.1", expected="3.2 – 3.4 V",    notes="Nominal"))
t1.add(Measurement("5V Rail",    5.02,  "V", condition=(4.9,  5.1),
                   test_number="1.1.2", expected="4.9 – 5.1 V"))
t1.add(Measurement("12V Rail",   11.0,  "V", condition=(11.5, 12.5),
                   test_number="1.1.3", expected="11.5 – 12.5 V",  notes="Under spec — check regulator"))
t1.add(Measurement("-5V Rail",   -4.98, "V", condition=lambda v: -5.1 <= v <= -4.9,
                   test_number="1.1.4", expected="-5.1 – -4.9 V"))
s1.add_table(t1)

t2 = TestTable(title="Current Draw", sub_number="1.2")
t2.add(Measurement("3.3V Current", 0.42, "A", condition=(0.0, 0.6),
                   test_number="1.2.1", expected="< 0.6 A"))
t2.add(Measurement("5V Current",   0.88, "A", condition=(0.0, 1.0),
                   test_number="1.2.2", expected="< 1.0 A"))
t2.add(Measurement("12V Current",  1.35, "A", condition=(0.0, 1.2),
                   test_number="1.2.3", expected="< 1.2 A",        notes="Exceeds limit"))
s1.add_table(t2)
report.add_section(s1)

# ── Section 2: RF Performance ─────────────────────────────────────────────

s2 = Section(number="2", title="RF Performance",
             subtitle="Measured at 25 °C ambient, 50 Ω termination")

t3 = TestTable(title="Frequency Response", sub_number="2.1")
t3.add(Measurement("Center Frequency", 2401.5, "MHz", condition=(2400, 2403),
                   test_number="2.1.1", expected="2400 – 2403 MHz"))
t3.add(Measurement("Bandwidth (-3dB)",    82.4, "MHz", condition=(80, 90),
                   test_number="2.1.2", expected="80 – 90 MHz"))
t3.add(Measurement("Insertion Loss",       2.1, "dB",  condition=lambda v: v < 3,
                   test_number="2.1.3", expected="< 3 dB"))
t3.add(Measurement("Return Loss",         18.5, "dB",  condition=15.0,
                   test_number="2.1.4", expected=">= 15 dB"))
s2.add_table(t3)

t4 = TestTable(title="Noise & Spurious", sub_number="2.2")
t4.add(Measurement("Noise Figure",       3.8, "dB",     condition=lambda v: v < 5,
                   test_number="2.2.1", expected="< 5 dB"))
t4.add(Measurement("Phase Noise @1 kHz", -88, "dBc/Hz", condition=lambda v: v < -85,
                   test_number="2.2.2", expected="< -85 dBc/Hz"))
t4.add(Measurement("Spurious Level",     -62, "dBc",    condition=lambda v: v < -60,
                   test_number="2.2.3", expected="< -60 dBc"))
t4.add(Measurement("Harmonic 2nd",       -45, "dBc",    condition=lambda v: v < -40,
                   test_number="2.2.4", expected="< -40 dBc",  notes="Marginal"))
s2.add_table(t4)
report.add_section(s2)

# ── Section 3: Environmental ──────────────────────────────────────────────

s3 = Section(number="3", title="Environmental",
             subtitle="Recorded during test — informational only")

t5 = TestTable(title="Ambient Conditions", sub_number="3.1")
t5.add(Measurement("Temperature", 24.3, "°C",  description="Ambient"))
t5.add(Measurement("Humidity",    41.0, "%RH", description="Relative humidity"))
t5.add(Measurement("Supply Temp", 38.5, "°C",
                   condition=lambda v: v < 50,
                   test_number="3.1.3", expected="< 50 °C", notes="PSU heatsink"))
s3.add_table(t5)
report.add_section(s3)

# ── Generate ──────────────────────────────────────────────────────────────

report.generate_html(str(OUT / "report.html"))
print("report.html  ✓")

report.generate_excel(str(OUT / "report.xlsx"))
print("report.xlsx  ✓")

try:
    report.generate_pdf(str(OUT / "report.pdf"))
    print("report.pdf   ✓")
except ImportError:
    print("report.pdf   skipped  (pip install 'instrumation-report[pdf]')")
