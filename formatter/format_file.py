from pathlib import Path

from formatter.discover import ROOT

from formatter.rules.format.blank_lines import format_text as blank_lines
from formatter.rules.format.double_blanks import format_text as double_blanks
from formatter.rules.format.eof_newline import format_text as eof_newline
from formatter.rules.format.import_sort import format_text as import_sort
from formatter.rules.format.indentation import format_text as indentation
from formatter.rules.format.line_endings import format_text as line_endings

from formatter.rules.format.declaration_spacing import (
  format_text as declaration_spacing,
)

from formatter.rules.format.leading_blank_lines import (
  format_text as leading_blank_lines,
)

from formatter.rules.format.trailing_commas import (
  format_text as trailing_commas,
)

from formatter.rules.format.trailing_spaces import (
  format_text as trailing_spaces,
)

def format_text(text: str) -> str:
  text = blank_lines(text)
  text = line_endings(text)
  text = trailing_spaces(text)
  text = import_sort(text)
  text = indentation(text)
  text = leading_blank_lines(text)
  text = declaration_spacing(text)
  text = trailing_commas(text)
  text = double_blanks(text)
  text = eof_newline(text)

  return text

def format_file(path: Path, check: bool = False) -> bool:
  original = path.read_text()
  formatted = format_text(original)

  if formatted == original:
    return False

  if check:
    print(f"{path} needs formatting")

    return True

  path.write_text(formatted)
  print(f"formatted {path}")

  return True

