def format_text(text: str) -> str:
  lines = text.split("\n")

  while lines and lines[0].strip() == "":
    lines.pop(0)

  return "\n".join(lines)

