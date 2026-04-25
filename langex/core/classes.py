from typing import Callable, Iterable, TypeVar

from langex.classes.class_meta import ClassMeta

__all__ = [
  "langex_class",
  "interface",
  "abstract",
  "implements",
  "extends",
]

ClassType = TypeVar("ClassType", bound=type)
ClassTypes = Iterable[ClassType]
ApplyFn = Callable[[ClassType], None]
GetApplyFn = Callable[[ClassMeta], ApplyFn]
ClassDecorator = Callable[[ClassType], ClassType]

def langex_class(cls: ClassType) -> ClassType:
  return ClassMeta(cls).use_primitive()

def interface(cls: ClassType) -> ClassType:
  return ClassMeta(cls).use_interfacing()

def abstract(cls: ClassType) -> ClassType:
  return ClassMeta(cls).use_abstraction()

def _create_decorator(
  interfaces: ClassTypes,
  get_apply_func: GetApplyFn
) -> ClassDecorator:
  def decorator(cls: ClassType) -> ClassType:
    meta = ClassMeta(cls)
    meta.use_primitive()

    for interface in interfaces:
      apply_func = get_apply_func(meta)
      apply_func(interface)

    return cls

  return decorator

def implements(*interfaces: ClassType) -> ClassDecorator:
  return _create_decorator(
    interfaces,
    lambda meta: meta.implement
  )

def extends(cls: ClassType) -> ClassType:
  parents = (cls.__base__,) + cls.__bases__
  decorator = _create_decorator(
    parents,
    lambda meta: meta.extend
  )

  return decorator(cls)

