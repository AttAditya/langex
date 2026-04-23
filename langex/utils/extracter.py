from langex.functions.function_meta import FunctionMeta
from langex.constants.keys import LANGEX

def extract_methods(cls: type | object) -> dict[str, FunctionMeta]:
  methods = {}

  for attr_name in cls.__dict__:
    if attr_name.startswith("__"):
      continue

    if attr_name.endswith("__"):
      continue

    attr = getattr(cls, attr_name)

    if callable(attr):
      if not hasattr(attr, LANGEX.MARKER):
        attr = FunctionMeta(attr)

      methods[attr_name] = attr

  return methods

