from langex.core.classes import singleton

@singleton
class ExpectsData:
  def __init__(self):
    self.data = {}
    self.repeat = {}

  def get_key(self, name: str) -> str:
    if name not in self.repeat and name not in self.data:
      return name

    if name in self.repeat:
      self.repeat[name] += 1

      return f"{name}__{self.repeat[name]}"

    self.repeat[name] = 1
    tmpk = f"{name}__{self.repeat[name]}"
    self.data[tmpk] = {**self.data[name]}
    del self.data[name]
    self.repeat[name] += 1

    return f"{name}__{self.repeat[name]}"

  def add(self, name: str, func: callable, result: object):
    key = self.get_key(name)
    self.data[key] = {
      "name": name,
      "func": func,
      "result": result,
    }

    return func

  def run(self):
    passed = []
    failed = []
    errors = []

    for name in self.data:
      meta = self.data[name]
      func = meta["func"]
      expected = meta["result"]
      error = None

      try:
        result = func()
      except Exception as caught:
        error = caught
        result = caught.__class__

      if result == expected:
        passed.append(name)
      else:
        if error is not None:
          errors.append((name, error))
        else:
          failed.append(name)

    message = "\n\nTests Results:\n"
    message += f"Passed: {len(passed)}\n"
    message += f"Failed: {len(failed)}\n"
    message += f"Errors: {len(errors)}\n"
    message += "\n\n"
    message += "Failed Tests:\n"

    for name in failed:
      message += f"- {name}\n"

    message += "\n\nErrors:\n"

    for name, error in errors:
      message += f"- {name}: {error}\n"

    assert len(passed) == len(self.data), message
    print("All tests passed!")
    print(message)

