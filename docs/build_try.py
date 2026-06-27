"""
Run from repo root: python docs/build_try.py
Embeds the instrumation_report source into docs/try.html so the
Pyodide playground works from any origin (gh-pages, file://, etc.)
without any network requests to the library files.
"""
import json
from pathlib import Path

SRC = {
    "instrumation_report/__init__.py":        Path("instrumation_report/__init__.py"),
    "instrumation_report/measurement.py":     Path("instrumation_report/measurement.py"),
    "instrumation_report/section.py":         Path("instrumation_report/section.py"),
    "instrumation_report/report.py":          Path("instrumation_report/report.py"),
    "instrumation_report/templates/base.html":Path("instrumation_report/templates/base.html"),
}

lib = {k: v.read_text(encoding="utf-8") for k, v in SRC.items()}
lib_json = json.dumps(lib, ensure_ascii=False)

template = Path("docs/try.template.html").read_text(encoding="utf-8")
output   = template.replace("__LIB_FILES_JSON__", lib_json)
Path("docs/try.html").write_text(output, encoding="utf-8")
print(f"docs/try.html written ({len(output):,} bytes)")
