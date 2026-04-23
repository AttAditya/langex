from langex.functions.function_meta import FunctionMeta
from langex.functions.signature import Signature

class MethodsMeta:
  def __init__(self, class_meta):
    self.class_meta = class_meta
    self.abstracted: dict[str, Signature] = {}
    self.implemented: dict[str, Signature] = {}

  def add_abstracted(self, method: FunctionMeta):
    self.abstracted[method.name] = method.signature

  def add_implemented(self, method: FunctionMeta):
    self.implemented[method.name] = method.signature

  def clone(self):
    new_methods_meta = MethodsMeta(self.class_meta)
    new_methods_meta.abstracted = {}
    new_methods_meta.implemented = {}

    for method_name in self.abstracted:
      cloned_signature = self.abstracted[method_name].clone()
      new_methods_meta.abstracted[method_name] = cloned_signature

    for method_name in self.implemented:
      cloned_signature = self.implemented[method_name].clone()
      new_methods_meta.implemented[method_name] = cloned_signature

    return new_methods_meta

