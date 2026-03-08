MAX = 80

def check(text: str) -> list[tuple[int, int, int]]:
  errors = []

  for line_no, line in enumerate(text.split("\n"), start=1):
    actual = len(line)

    if actual > MAX:
      errors.append((line_no, actual, MAX))

  return errors

