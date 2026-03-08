import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

def get_local_roots() -> set[str]:
  roots = set()

  for path in ROOT.iterdir():
    if path.name.startswith("."):
      continue

    if path.is_dir():
      roots.add(path.name)

  return roots

LOCAL_ROOTS = get_local_roots()
STDLIB_ROOTS = set(getattr(sys, "stdlib_module_names", set()))

def make_import_blocks(lines: list[str]) -> list[str]:
  blocks = []
  i = 0

  while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped.startswith("import ") or stripped.startswith("from "):
      block = [line]
      balance = line.count("(") - line.count(")")
      i += 1

      while i < len(lines) and balance > 0:
        block.append(lines[i])
        balance += lines[i].count("(") - lines[i].count(")")
        i += 1

      blocks.append("\n".join(block))
      continue

    i += 1

  return blocks

def bucket_import_blocks(blocks: list[str]) -> dict[str, list[str]]:
  buckets = {
    "import_plain": [],
    "import_alias": [],
    "from_plain": [],
    "from_alias": [],
    "from_parenthesized": [],
  }

  for block in blocks:
    stripped = block.strip()

    if not stripped:
      continue

    if stripped.startswith("import "):
      if " as " in stripped:
        buckets["import_alias"].append(block)

      else:
        buckets["import_plain"].append(block)

      continue

    if stripped.startswith("from "):
      if "(" in stripped and ")" in stripped:
        buckets["from_parenthesized"].append(block + "\n")

      elif " as " in stripped:
        buckets["from_alias"].append(block)

      else:
        buckets["from_plain"].append(block)

      continue

  return buckets

def get_module_name(block: str) -> str:
  first_line = block.strip().split("\n", 1)[0]

  if first_line.startswith("import "):
    module = first_line[len("import "):].split(",", 1)[0].strip()
    module = module.split(" as ", 1)[0].strip()

    return module

  if first_line.startswith("from "):
    module = first_line[len("from "):].split(" import ", 1)[0].strip()

    return module

  return ""

def get_root_name(block: str) -> str:
  module = get_module_name(block)

  if module.startswith("."):
    return module

  return module.split(".", 1)[0]

def get_origin_group(block: str) -> int:
  root = get_root_name(block)

  if not root:
    return 3

  if root.startswith("."):
    return 3

  if root in STDLIB_ROOTS:
    return 0

  if root in LOCAL_ROOTS:
    return 2

  return 1

def group_by_package(blocks: list[str]) -> dict[str, list[str]]:
  buckets: dict[str, list[str]] = {}

  for block in blocks:
    root = get_root_name(block)
    buckets.setdefault(root, []).append(block)

  for root in buckets:
    buckets[root] = sorted(buckets[root])

  return dict(sorted(buckets.items()))

def sort_group(blocks: list[str]) -> list[str]:
  if not blocks:
    return []

  origin_buckets: dict[int, list[str]] = {
    0: [],
    1: [],
    2: [],
    3: [],
  }

  for block in blocks:
    origin_buckets[get_origin_group(block)].append(block)

  out = []

  for origin in [0, 1, 2, 3]:
    if not origin_buckets[origin]:
      continue

    package_groups = group_by_package(origin_buckets[origin])

    for package_blocks in package_groups.values():
      if out:
        out.append("")

      out.extend(package_blocks)

  return out

def split_top_import_section(lines: list[str]) -> tuple[list[str], list[str]]:
  import_lines = []
  rest_lines = []
  i = 0
  collecting = True

  while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if collecting and not stripped:
      import_lines.append(line)
      i += 1
      continue

    if collecting and (
      stripped.startswith("import ") or stripped.startswith("from ")
    ):

      block = [line]
      balance = line.count("(") - line.count(")")
      i += 1

      while i < len(lines) and balance > 0:
        block.append(lines[i])
        balance += lines[i].count("(") - lines[i].count(")")
        i += 1

      import_lines.extend(block)
      continue

    collecting = False
    rest_lines.extend(lines[i:])
    break

  return import_lines, rest_lines

def format_text(text: str) -> str:
  lines = text.split("\n")
  import_lines, rest_lines = split_top_import_section(lines)
  blocks = make_import_blocks(import_lines)

  if not blocks:
    return text

  buckets = bucket_import_blocks(blocks)
  ordered = []

  for group_name in [
    "import_plain",
    "import_alias",
    "from_plain",
    "from_alias",
    "from_parenthesized",
  ]:

    sorted_group = sort_group(buckets[group_name])

    if not sorted_group:
      continue

    if ordered:
      ordered.append("")

    ordered.extend(sorted_group)

  sorted_import_text = "\n".join(ordered).strip()
  rest_text = "\n".join(rest_lines).lstrip("\n")

  if rest_text:
    return sorted_import_text + "\n\n" + rest_text

  return sorted_import_text

