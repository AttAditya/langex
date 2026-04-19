from langex.functions.function_meta import FunctionMeta

def extract_methods(cls: type | object) -> dict[str, FunctionMeta]:
  methods = {}

  for attr_name in dir(cls):
    if attr_name.startswith("__"):
      continue

    if attr_name.endswith("__"):
      continue

    attr = getattr(cls, attr_name)

    if callable(attr):
      methods[attr_name] = FunctionMeta(attr)

  return methods

