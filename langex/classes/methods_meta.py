from langex.errors.unimplemented import UnimplementedError
from langex.functions.function_meta import FunctionMeta
from langex.functions.signature import Signature

class MethodsMeta:
  def __init__(self, class_meta):
    self.class_meta = class_meta
    self.abstract_methods: dict[str, Signature] = {}
    self.methods: dict[str, Signature] = {}

  def add_abstract_method(self, method):
    if not isinstance(method, FunctionMeta):
      method = FunctionMeta(method)

    self.abstract_methods[method.name] = method.signature

  def add_method(self, method):
    if not isinstance(method, FunctionMeta):
      method = FunctionMeta(method)

    self.methods[method.name] = method.signature

  def clone(self):
    new_methods_meta = MethodsMeta(self.class_meta)
    new_methods_meta.abstract_methods = {}
    new_methods_meta.methods = {}

    for method_name in self.abstract_methods:
      cloned_signature = self.abstract_methods[method_name].clone()
      new_methods_meta.abstract_methods[method_name] = cloned_signature

    for method_name in self.methods:
      cloned_signature = self.methods[method_name].clone()
      new_methods_meta.methods[method_name] = cloned_signature

    return new_methods_meta

  def impose(self, cls):
    missing_methods = set()

    for required_method_name in self.abstract_methods:
      if not hasattr(cls, required_method_name):
        missing_methods.add(required_method_name)
        continue

      method = getattr(cls, required_method_name)
      method = FunctionMeta(method)
      expected_signature = self.abstract_methods[required_method_name]
      method.signature = expected_signature
      setattr(cls, required_method_name, method)

    if missing_methods:
      raise UnimplementedError({
        "target": cls.__name__,
        "source": self.class_meta.name,
        "missing": missing_methods,
        "reason": "Missing source method implementations in target class"
      })

