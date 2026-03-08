def format_text(text: str) -> str:
  return "\n".join(line.rstrip() for line in text.split("\n"))

