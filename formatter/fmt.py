import sys

from formatter.discover import discover
from formatter.format_file import format_file

def main():
  args: list[str] = sys.argv[1:]
  check_mode = False
  target = "."

  if args:
    if args[0] == "--check":
      check_mode = True

      if len(args) > 1:
        target = args[1]

    else:
      target = args[0]

  needs_format = False

  for path in discover(target):
    changed = format_file(path, check=check_mode)

    if changed:
      needs_format = True

  if check_mode and needs_format:
    raise SystemExit(1)

if __name__ == "__main__":
  main()

