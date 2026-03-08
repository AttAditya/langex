from pathlib import Path

from formatter.discover import ROOT

from formatter.rules.lint.line_length import check as check_line_length

def lint_file(path: Path):
  text = path.read_text()
  errors = []

  for line_no, actual, limit in check_line_length(text):
    errors.append(
      f"{path.relative_to(ROOT)}:{line_no} GS007 "
      f"line too long ({actual} > {limit})"
    )

  for error in errors:
    print(error)

