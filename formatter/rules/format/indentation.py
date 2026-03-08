def detect_indent(lines: list[str]) -> int:
  indents = []

  for line in lines:
    stripped = line.lstrip(" \t")

    if not stripped:
      continue

    leading = line[:len(line) - len(stripped)]
    spaces = leading.count(" ") + leading.count("\t") * 4

    if spaces:
      indents.append(spaces)

  if not indents:
    return 2

  return min(indents)

def format_text(text: str) -> str:
  lines = text.split("\n")
  old_width = detect_indent(lines)
  new_width = 2
  out = []

  for line in lines:
    stripped = line.lstrip(" \t")
    leading = line[:len(line) - len(stripped)]

    if not stripped:
      out.append("")
      continue

    spaces = leading.count(" ") + leading.count("\t") * old_width
    level = spaces // old_width
    out.append((" " * (level * new_width)) + stripped)

  return "\n".join(out)

