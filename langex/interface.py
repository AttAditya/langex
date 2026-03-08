from langex.core.use import access_langex, use_langex
from langex.immediate import immediate

@immediate
def _ignored_attributes():
  @use_langex
  class _BlankClass:
    pass

  return set(dir(_BlankClass))

def interface(cls):
  use_langex(cls)
  attributes = set(dir(cls))
  attributes -= _ignored_attributes
  lnx = access_langex(cls)
  class_meta = lnx.class_meta
  class_meta.is_interface = True

  for attribute_name in attributes:
    attribute = getattr(cls, attribute_name)

    if not callable(attribute):
      continue

    callable_lnx = access_langex(attribute)
    typehints = callable_lnx.callable_meta.typehints

    if typehints.has_typehints:
      class_meta.callables[attribute_name] = callable_lnx

  def raise_uninstantiable_error(*_, **_____):
    raise TypeError(" ".join([
      f"Class {cls.__name__} is an interface.",
      "It may not be instantiated."
    ]))

  setattr(cls, "__init__", raise_uninstantiable_error)

  return cls

def implements(*interfaces):
  callables = {}

  for interface in interfaces:
    lnx = access_langex(interface)
    class_meta = lnx.class_meta

    if not class_meta.is_interface:
      raise TypeError(" ".join([
        f"Class {interface.__name__} is not an interface.",
        "Only interfaces may be implemented."
      ]))

    conflict_callables = set()

    for callable_name in class_meta.callables:
      if callable_name in callables:
        overiding_callable = class_meta.callables[callable_name]
        existing_callable = callables[callable_name]

        if not existing_callable.matches_signature(overiding_callable):
          conflict_callables.add(callable_name)
          continue

      callables[callable_name] = class_meta.callables[callable_name]

  def decorator(cls):
    unimplemented_methods = callables.keys() - set(dir(cls))

    if conflict_callables:
      raise TypeError(" ".join([
        f"Class {cls.__name__} has methods that have ",
        "conflicting signatures in interfaces: ",
        ", ".join(conflict_callables),
      ]))

    if unimplemented_methods:
      raise NotImplementedError(" ".join([
        f"Class {cls.__name__} does not implement methods:",
        ", ".join(unimplemented_methods),
      ]))

    return cls

  return decorator

__all__ = [
  "interface",
  "implements",
]

