from langex.classes.methods_meta import MethodsMeta
from langex.constants.contents import CONTENTS
from langex.constants.keys import LANGEX
from langex.constants.labels import LABELS
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
    self.instanciate = getattr(cls, LANGEX.ATTACKED_ATTRS.NEW)
    self.class_type = LANGEX.CLASS_TYPE.UNSET
    self.follows: set[ClassMeta] = set()
    self.methods = MethodsMeta(self)
    self._inject()

  def _create_class_instance(self, *args, **kwargs):
    if self.is_interface():
      raise InstantiationError({
        LABELS.REF.SELF: self.qual,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.CANNOT_A_X.format(
          A=LABELS.ACTS.INSTANTIATE,
          X=LABELS.CLASS_NOUNS.INTERFACE_CLASS
        )
      })

    if self.is_abstract():
      raise InstantiationError({
        LABELS.REF.SELF: self.qual,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.CANNOT_A_X.format(
          A=LABELS.ACTS.INSTANTIATE,
          X=LABELS.CLASS_NOUNS.ABSTRACT_CLASS
        )
      })

    args = args[1:]
    instance = object.__new__(self.cls)
    instance.__init__(*args, **kwargs)
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
      method.func = func_ref.__get__(instance, self.cls)
      setattr(instance, method_name, method)

    return instance

  def _inject(self):
    setattr(self.cls, LANGEX.MARKER, True)
    setattr(self.cls, LANGEX.CLASS_META, self)
    setattr(
      self.cls,
      LANGEX.ATTACKED_ATTRS.NEW,
      self._create_class_instance
    )

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
        LABELS.REF.SELF: self.qual,
        LABELS.REF.PEER: source.__qualname__,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_IS_NOT_Y.format(
          X=LABELS.REF.PEER,
          Y=LABELS.CLASS_NOUNS.LANGEX_CLASS
        )
      })

    interface: ClassMeta = getattr(source, LANGEX.CLASS_META)

    if not interface.is_interface():
      raise ValidationError({
        LABELS.REF.SELF: self.qual,
        LABELS.REF.PEER: interface.qual,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_IS_NOT_Y.format(
          X=LABELS.REF.PEER,
          Y=LABELS.CLASS_NOUNS.INTERFACE_CLASS
        )
      })

    existing_methods = set()
    existing_methods |= set(self.methods.abstracted.keys())
    existing_methods |= set(self.methods.implemented.keys())
    imposing_methods = set(interface.methods.abstracted.keys())
    missing_methods = imposing_methods - existing_methods

    if missing_methods:
      raise UnimplementedError({
        LABELS.REF.SELF: self.qual,
        LABELS.REF.PEER: interface.qual,
        LABELS.CAUSE.MISSING: missing_methods,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.MISSING_X.format(
          X=LABELS.FUNC_NOUNS.PEER_METHON_IMPL
        )
      })

    for method_name in imposing_methods:
      signature = interface.methods.abstracted[method_name]
      self.methods.implemented[method_name] = signature

    self.follows.add(interface.cls)

