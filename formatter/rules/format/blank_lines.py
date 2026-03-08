def format_text(text: str) -> str:
  lines = text.split("\n")
  out = []

  for line in lines:
    blank = line.strip() == ""

    if blank:
      continue

    out.append(line)

  return "\n".join(out)

