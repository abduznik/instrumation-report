from instrumation_report import Section, TestTable, Measurement


def test_test_table_add():
    t = TestTable(title="Power Checks", sub_number="1.1")
    m = Measurement("V", 3.3, "V", condition=(3.2, 3.4))
    t.add(m)
    assert len(t.measurements) == 1
    assert t.measurements[0] is m


def test_section_add_table():
    s = Section(number="1", title="Voltage Tests")
    t = TestTable(title="Power Checks", sub_number="1.1")
    s.add_table(t)
    assert len(s.tables) == 1
    assert s.tables[0] is t


def test_section_subtitle_default():
    s = Section(number="2", title="RF Tests")
    assert s.subtitle == ""


def test_section_multiple_tables():
    s = Section(number="1", title="Tests")
    for i in range(3):
        s.add_table(TestTable(title=f"Table {i}", sub_number=f"1.{i}"))
    assert len(s.tables) == 3


def test_nesting():
    section = Section(number="1", title="Voltage Tests")
    table = TestTable(title="Power Supply Checks", sub_number="1.1")
    table.add(Measurement("3.3V Rail", 3.31, "V", condition=(3.2, 3.4), test_number="1.1.1"))
    table.add(Measurement("5V Rail", 5.02, "V", condition=(4.9, 5.1), test_number="1.1.2"))
    section.add_table(table)

    assert len(section.tables[0].measurements) == 2
    assert section.tables[0].measurements[0].status == "PASS"
    assert section.tables[0].measurements[1].status == "PASS"
