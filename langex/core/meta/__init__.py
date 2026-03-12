from langex.core.meta.callable_meta import LangexCallableMeta
from langex.core.meta.class_meta import LangexClassMeta
from langex.core.meta.object_meta import LangexObjectMeta

class LangexMeta:
  def __init__(self):
    self.class_meta = LangexClassMeta()
    self.callable_meta = LangexCallableMeta()
    self.object_meta = LangexObjectMeta()

__all__ = [
  "LangexMeta",
]

