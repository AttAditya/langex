from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORED = {
  ".venv",
  "__pycache__",
  "build",
  "dist",
}

def ignored(path: Path) -> bool:
  return any(part in IGNORED for part in path.parts)

def discover(target: str = ".") -> list[Path]:
  base = (ROOT / target).resolve()
  files = []

  for path in base.rglob("*.py"):
    if ignored(path):
      continue

    files.append(path)

  return sorted(files)

