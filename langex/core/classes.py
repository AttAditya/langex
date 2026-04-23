from langex.classes.class_meta import ClassMeta
from langex.constants.keys import LANGEX

__all__ = [
  "langex_class",
  "interface",
  "abstract",
  "implements",
  "implements_bases",
  "extends",
  "extends_bases",
]

def langex_class(cls) -> type:
  return ClassMeta(cls).use_primitive()

def interface(cls) -> type:
  return ClassMeta(cls).use_interfacing()

def abstract(cls) -> type:
  return ClassMeta(cls).use_abstraction()

def implements_bases(cls: type) -> type:
  return implements(cls.__base__, *cls.__bases__)(cls)

def implements(*interfaces: type):
  def requires_base_implements():
    if len(interfaces) != 1:
      return False

    cls = interfaces[0]
    meta = getattr(cls, LANGEX.CLASS_META)
    qual_meta = meta.qual
    qual_cls = cls.__qualname__

    return qual_meta != qual_cls

  if requires_base_implements():
    return implements_bases(interfaces[0])

  def decorator(cls: type):
    meta = ClassMeta(cls)
    meta.use_primitive()

    for interface in interfaces:
      meta.implement(interface)

    return cls

  return decorator

def extends_bases(cls: type) -> type:
  return extends(cls.__base__, *cls.__bases__)(cls)

def extends(*parents: type):
  def requires_base_extends():
    if len(parents) != 1:
      return False

    cls = parents[0]
    meta = getattr(cls, LANGEX.CLASS_META)
    qual_meta = meta.qual
    qual_cls = cls.__qualname__

    return qual_meta != qual_cls

  if requires_base_extends():
    return extends_bases(parents[0])

  def decorator(cls: type):
    meta = ClassMeta(cls)
    meta.use_primitive()

    for interface in parents:
      meta.extend(interface)

    return cls

  return decorator

