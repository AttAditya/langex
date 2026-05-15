from os import listdir
from os.path import isfile, join

from langex.testing.data import ExpectsData

class TestHelpers:
  class Expects:
    def __init__(self, value: any):
      self.value = value

    def generate_name(self, func):
      lines = func.__code__.co_firstlineno
      module = func.__code__.co_filename
      qual = func.__qualname__
      name = func.__name__

      return f"{name} {qual} {module}:{lines}"

    def __rmatmul__(self, func):
      name = self.generate_name(func)
      ExpectsData.add(name, func, self.value)

  def should_include_dir(self, path: str) -> bool:
    return not path.endswith("__pycache__")

  def discover_filebase(
    self,
    base_path: str,
    init_file: str
  ) -> list[str]:
    files = []
    file_queue = [base_path]

    while file_queue:
      current_path = file_queue.pop(0)

      for entry in listdir(current_path):
        entry_path = join(current_path, entry)

        if isfile(entry_path):
          if not init_file.endswith(entry_path):
            files.append(entry_path)
        elif self.should_include_dir(entry_path):
          file_queue.append(entry_path)

    return files

  def import_files(self, files: list[str]):
    for file in files:
      __import__(file.replace("/", ".").rstrip(".py"))

  def discover_test(self, func):
    func()

    return func

  def base_path(self, initial_file: str, module_name: str) -> str:
    if module_name == "__main__":
      return initial_file.split("/")[:-1][-1]

    parts = initial_file.split("/")[:-1]
    module_parts = module_name.split(".")[:-1]

    for part in module_parts:
      if part in parts:
        parts.remove(part)

    return parts[-1]

  def run_tests(self, initial_file: str, module_name: str):
    base_path = self.base_path(initial_file, module_name)
    discovered_files = self.discover_filebase(base_path, initial_file)
    self.import_files(discovered_files)
    ExpectsData.run()

