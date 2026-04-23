from langex.classes.methods_meta import MethodsMeta
from langex.constants.keys import LANGEX
from langex.errors.instantiation import InstantiationError
from langex.errors.misapplication import MisapplicationError
from langex.errors.unimplemented import UnimplementedError
from langex.errors.validation import ValidationError
from langex.functions.function_meta import FunctionMeta
from langex.utils.extracter import extract_methods

class ClassMeta:
  def __init__(self, cls: type):
    self.cls = cls
    self.name = cls.__name__
    self.qual = cls.__qualname__
    self.instanciate = cls.__new__
    self.class_type = LANGEX.CLASS_TYPE.UNSET
    self.follows: set[ClassMeta] = set()
    self.methods = MethodsMeta(self)
    self._inject()

  def _create_class_instance(self, *args, **kwargs):
    if self.is_interface():
      raise InstantiationError({
        "target": self.qual,
        "reason": "Cannot instanciate langex interface class"
      })

    if self.is_abstract():
      raise InstantiationError({
        "target": self.qual,
        "reason": "Cannot instanciate langex abstract class"
      })

    instance = object.__new__(*args, **kwargs)
    setattr(instance, LANGEX.MARKER, True)
    setattr(instance, LANGEX.CLASS_META, self)
    methods = extract_methods(self.cls)

    for method_name in methods:
      method = methods[method_name]
      func_ref = method.func
      signature = None

      if method_name in self.methods.implemented:
        signature = self.methods.implemented[method_name]

      if method_name in self.methods.abstracted:
        signature = self.methods.abstracted[method_name]

      method.signature = signature
      method.func = lambda *a, **k: func_ref(
        instance, *a, **k
      )

      setattr(instance, method_name, method)

    return instance

  def _inject(self):
    setattr(self.cls, LANGEX.MARKER, True)
    setattr(self.cls, LANGEX.CLASS_META, self)
    setattr(self.cls, "__new__", self._create_class_instance)

  def is_interface(self) -> bool:
    return self.class_type == LANGEX.CLASS_TYPE.INTERFACE

  def is_abstract(self) -> bool:
    return self.class_type == LANGEX.CLASS_TYPE.ABSTRACT

  def use_primitive(self) -> type:
    self.class_type = LANGEX.CLASS_TYPE.PRIMITIVE
    methods = extract_methods(self.cls)

    for method_name in methods:
      method = methods[method_name]
      self.methods.add_implemented(method)

    return self.cls

  def use_interfacing(self) -> type:
    self.class_type = LANGEX.CLASS_TYPE.INTERFACE
    methods = extract_methods(self.cls)

    for method_name in methods:
      method = methods[method_name]
      self.methods.add_abstracted(method)

    return self.cls

  def use_abstraction(self) -> type:
    self.class_type = LANGEX.CLASS_TYPE.ABSTRACT
    methods = extract_methods(self.cls)

    for method_name in methods:
      method = methods[method_name]

      if not hasattr(method, LANGEX.FUNC_META):
        method = FunctionMeta(method)

      if method.is_abstract:
        self.methods.add_abstracted(method)
      else:
        self.methods.add_implemented(method)

    return self.cls

  def implement(self, source: type):
    if not hasattr(source, LANGEX.MARKER):
      raise MisapplicationError({
        "target": self.qual,
        "source": source.__qualname__,
        "reason": "Source is not a langex class"
      })

    interface: ClassMeta = getattr(source, LANGEX.CLASS_META)

    if not interface.is_interface():
      raise ValidationError({
        "target": self.qual,
        "source": interface.qual,
        "reason": "Source is not an interface"
      })

    existing_methods = set()
    existing_methods |= set(self.methods.abstracted.keys())
    existing_methods |= set(self.methods.implemented.keys())
    imposing_methods = set(interface.methods.abstracted.keys())
    missing_methods = imposing_methods - existing_methods

    if missing_methods:
      raise UnimplementedError({
        "target": self.qual,
        "source": interface.qual,
        "missing": missing_methods,
        "reason": "Missing source method implementations in target class"
      })

    for method_name in imposing_methods:
      signature = interface.methods.abstracted[method_name]
      self.methods.implemented[method_name] = signature

    self.follows.add(interface.cls)

