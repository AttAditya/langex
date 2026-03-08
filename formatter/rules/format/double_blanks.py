def format_text(text: str) -> str:
  while "\n\n\n" in text:
    text = text.replace("\n\n\n", "\n\n")

  return text

