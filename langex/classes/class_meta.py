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
    if type(cls) != type:
      raise MisapplicationError({
        LABELS.REF.SELF: cls.__qualname__,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
          X=LABELS.REF.SELF
        ),
        LABELS.CAUSE.EXPECTED: LABELS.CLASS_NOUNS.CLASS_TYPE,
        LABELS.CAUSE.RECEIVED: type(cls).__name__,
      })

    self.cls = cls
    self.name = cls.__name__
    self.qual = cls.__qualname__
    self.instanciate = getattr(cls, LANGEX.ATTACKED_ATTRS.NEW)
    self.class_type = LANGEX.CLASS_TYPE.UNSET
    self.follows: set[ClassMeta] = set()
    self.methods = MethodsMeta(self)
    self.instanciated = False
    self._inject()

  def _bound_class(self):
    for method_name in self.methods.implemented:
      method = self.methods.implemented[method_name]
      method.args.set_class_bounded()

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

    self._bound_class()
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

  def _validate_source(self, source: type):
    if hasattr(source, LANGEX.MARKER):
      return

    raise MisapplicationError({
      LABELS.REF.SELF: self.qual,
      LABELS.REF.PEER: source.__qualname__,
      LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_IS_NOT_Y.format(
        X=LABELS.REF.PEER,
        Y=LABELS.CLASS_NOUNS.LANGEX_CLASS
      )
    })

  def _validate_interface(self, source: type):
    self._validate_source(source)
    interface: ClassMeta = getattr(source, LANGEX.CLASS_META)

    if interface.is_interface():
      return

    raise ValidationError({
      LABELS.REF.SELF: self.qual,
      LABELS.REF.PEER: interface.qual,
      LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_IS_NOT_Y.format(
        X=LABELS.REF.PEER,
        Y=LABELS.CLASS_NOUNS.INTERFACE_CLASS
      )
    })

  def _get_missing_methods(
    self,
    source: type,
    method_type: str
  ) -> set[str]:
    meta: ClassMeta = getattr(source, LANGEX.CLASS_META)
    target_methods: set[str] = set()

    if method_type == LANGEX.METHOD_TYPE.ABSTRACTED:
      target_methods = set(meta.methods.abstracted.keys())

    if method_type == LANGEX.METHOD_TYPE.IMPLEMENTED:
      target_methods = set(meta.methods.implemented.keys())

    existing_methods: set[str] = set()
    existing_methods |= set(self.methods.abstracted.keys())
    existing_methods |= set(self.methods.implemented.keys())
    missing_methods = target_methods - existing_methods

    return missing_methods

  def _abstraction_check(self, source: type):
    class_meta: ClassMeta = getattr(source, LANGEX.CLASS_META)
    missing_methods = self._get_missing_methods(
      source, LANGEX.METHOD_TYPE.ABSTRACTED
    )

    if missing_methods:
      raise UnimplementedError({
        LABELS.REF.SELF: self.qual,
        LABELS.REF.PEER: class_meta.qual,
        LABELS.CAUSE.MISSING: missing_methods,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.MISSING_X.format(
          X=LABELS.FUNC_NOUNS.PEER_METHON_IMPL
        )
      })

  def implement(self, source: type):
    self._validate_interface(source)
    self._abstraction_check(source)
    interface: ClassMeta = getattr(source, LANGEX.CLASS_META)
    imposing_methods = set(interface.methods.abstracted.keys())

    for method_name in imposing_methods:
      signature = interface.methods.abstracted[method_name]
      self.methods.implemented[method_name] = signature

    self.follows.add(interface.cls)

  def extend(self, source: type):
    self._validate_source(source)
    parent: ClassMeta = getattr(source, LANGEX.CLASS_META)
    extending_methods = self._get_missing_methods(
      source, LANGEX.METHOD_TYPE.IMPLEMENTED
    )

    for method_name in extending_methods:
      method = getattr(source, method_name)
      signature = parent.methods.implemented[method_name]
      self.methods.implemented[method_name] = signature
      setattr(self.cls, method_name, method)

    imposing_abs_methods = set(parent.methods.abstracted.keys())
    imposing_imp_methods = set(parent.methods.implemented.keys())

    for method_name in imposing_abs_methods:
      signature = parent.methods.abstracted[method_name]
      self.methods.implemented[method_name] = signature

    for method_name in imposing_imp_methods:
      signature = parent.methods.implemented[method_name]
      self.methods.implemented[method_name] = signature

    if not self.is_abstract():
      self._abstraction_check(source)

    self.follows.add(parent.cls)

