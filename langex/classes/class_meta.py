from langex.classes.methods_meta import MethodsMeta
from langex.errors.instantiation import InstantiationError
from langex.errors.misapplication import MisapplicationError
from langex.functions.function_meta import FunctionMeta
from langex.utils.extracter import extract_methods

class ClassMeta:
  def __init__(self, cls, base_classes=None, *_):
    if base_classes is not None:
      raise MisapplicationError({
        "target": cls,
        "reason": "Traditional inheritance unsupported for Langex classes"
      })

    if isinstance(cls, ClassMeta):
      self.cls = cls.cls
      self.name = cls.name
      self.__name__ = cls.__name__
      self.methods_meta = cls.methods_meta.clone()
      self.is_interface = cls.is_interface
      self.is_abstract = cls.is_abstract
      self.ancestors = cls.ancestors
    else:
      self.cls = cls
      self.name = cls.__name__
      self.__name__ = cls.__name__
      self.methods_meta = MethodsMeta(self)
      self.is_interface = False
      self.is_abstract = False
      self.ancestors = set()

  def __call__(self, *args, **kwargs):
    if self.is_interface:
      raise InstantiationError({
        "target": self.name,
        "reason": "Class is interface"
      })

    if self.is_abstract:
      raise InstantiationError({
        "target": self.name,
        "reason": "Class is abstract"
      })

    cls_obj = self.cls(*args, **kwargs)
    methods = extract_methods(cls_obj)
    setattr(cls_obj, "ancestors", self.ancestors)

    for method_name in methods:
      method_meta = FunctionMeta(methods[method_name])
      method_meta.owner = cls_obj
      setattr(cls_obj, method_name, method_meta)

    return cls_obj

