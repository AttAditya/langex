from langex.core.meta import LangexMeta

def use_langex(target):
  if not hasattr(target, "__langex__"):
    setattr(target, "__langex__", LangexMeta())

  return target

def access_langex(target):
  if not hasattr(target, "__langex__"):
    use_langex(target)

  return target.__langex__

__all__ = [
  "use_langex",
  "access_langex",
]

