from os import listdir
from os.path import isfile, join

def should_include_dir(path: str):
  if not isfile(path):
    return not path.endswith("__pycache__")

def discover_filebase():
  files = []
  file_queue = ["tests"]

  while file_queue:
    current_path = file_queue.pop(0)

    for entry in listdir(current_path):
      entry_path = join(current_path, entry)

      if isfile(entry_path):
        if not __file__.endswith(entry_path):
          files.append(entry_path)
      elif should_include_dir(entry_path):
        file_queue.append(entry_path)

  return files

def start(files: list[str]):
  for file in files:
    __import__(file.replace("/", ".").rstrip(".py"))

def main():
  files = discover_filebase()
  start(files)

if __name__ == "__main__":
  main()

