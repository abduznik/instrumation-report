import pytest
from instrumation_report import Measurement


# ── condition evaluation ───────────────────────────────────────────────────

def test_lambda_pass():
    assert Measurement("F", 1002, "Hz", condition=lambda v: v > 1000).evaluate() is True

def test_lambda_fail():
    assert Measurement("F", 999, "Hz", condition=lambda v: v > 1000).evaluate() is False

def test_tuple_pass():
    assert Measurement("V", 4.7, "V", condition=(4.0, 5.0)).evaluate() is True

def test_tuple_fail_high():
    assert Measurement("V", 5.1, "V", condition=(4.0, 5.0)).evaluate() is False

def test_tuple_fail_low():
    assert Measurement("V", 3.9, "V", condition=(4.0, 5.0)).evaluate() is False

def test_tuple_boundary_low():
    assert Measurement("V", 4.0, "V", condition=(4.0, 5.0)).evaluate() is True

def test_tuple_boundary_high():
    assert Measurement("V", 5.0, "V", condition=(4.0, 5.0)).evaluate() is True

def test_threshold_pass():
    assert Measurement("I", 3.5, "A", condition=3.0).evaluate() is True

def test_threshold_exact():
    assert Measurement("I", 3.0, "A", condition=3.0).evaluate() is True

def test_threshold_fail():
    assert Measurement("I", 2.9, "A", condition=3.0).evaluate() is False

def test_no_condition_returns_none():
    assert Measurement("T", 25.0, "C").evaluate() is None

def test_invalid_condition_raises():
    m = Measurement("X", 1.0, "", condition="bad")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        m.evaluate()


# ── status property ────────────────────────────────────────────────────────

def test_status_pass():
    assert Measurement("V", 4.5, "V", condition=(4.0, 5.0)).status == "PASS"

def test_status_fail():
    assert Measurement("V", 3.0, "V", condition=(4.0, 5.0)).status == "FAIL"

def test_status_na():
    assert Measurement("T", 25.0, "C").status == "N/A"


# ── fields ─────────────────────────────────────────────────────────────────

def test_all_fields():
    m = Measurement(
        name="Rise Time",
        value=0.8,
        unit="ms",
        condition=0.5,
        test_number="1.1.1",
        expected=">= 0.5 ms",
        notes="nominal",
        description="Edge transition",
    )
    assert m.test_number == "1.1.1"
    assert m.expected == ">= 0.5 ms"
    assert m.notes == "nominal"
    assert m.description == "Edge transition"
