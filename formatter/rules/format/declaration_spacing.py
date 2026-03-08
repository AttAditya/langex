def count_leading_spaces(line: str) -> int:
  count = 0

  for char in line:
    if char == " ":
      count += 1

    else:
      break

  return count

def check_is_keyword(line: str):
  stripped = line.strip()
  keywords = [
    "def ", "class ", "@", "if ", "raise ",
    "try:", "for ", "while ", "with ", "async ",
    "return ", "continue ", "break ", "yield ",
  ]

  return any(stripped.startswith(keyword) for keyword in keywords)

def check_is_closing(line: str):
  stripped = line.strip()
  closings = [
    "]", ")", "}",
  ]

  return any(stripped.startswith(closing) for closing in closings)

def format_text(text: str) -> str:
  lines = text.split("\n")
  out = []

  for i, line in enumerate(lines):
    has_prev_line = i > 0
    has_next_line = i < len(lines) - 1
    is_keyword = check_is_keyword(line)
    is_closing = check_is_closing(line)
    is_blank = line.strip() == ""
    curr_indent = count_leading_spaces(line)
    prev_indent = 0
    is_prev_keyword = False
    is_indent_down = False
    is_next_closing = False

    if has_prev_line:
      prev_indent = count_leading_spaces(lines[i - 1])
      is_prev_keyword = check_is_keyword(lines[i - 1])
      is_indent_down = prev_indent > curr_indent

    if has_next_line:
      is_next_closing = check_is_closing(lines[i + 1])

    pre_space_required = False
    post_space_required = False

    if is_indent_down or (is_keyword and not is_prev_keyword):
      pre_space_required |= True

    if is_closing or is_blank or not has_prev_line:
      pre_space_required &= False

    if is_closing and not is_next_closing:
      post_space_required |= True

    if pre_space_required:
      out.append("")

    out.append (line)

    if post_space_required:
      out.append("")

  return "\n".join(out)

