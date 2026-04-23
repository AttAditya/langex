from langex.errors.misapplication import MisapplicationError
from langex.functions.signature import Signature
from langex.registry import LANGEX

class FunctionMeta:
  def __init__(self, func):
    if hasattr(func, LANGEX.MARKER):
      return

    self.func = func
    self.name = func.__name__
    self.qual = func.__qualname__
    self.signature = Signature(self.qual)
    self.is_abstract = False
    self._inject()

  def _inject(self):
    setattr(self, LANGEX.MARKER, True)
    setattr(self, LANGEX.FUNC_META, self)

  def _is_class_function(self):
    parts = self.qual.split(".")

    if len(parts) == 1:
      return False

    return parts[-2] != "<locals>"

  def __call__(self, *args, **kwargs):
    self.signature.args.validate(args, kwargs)
    result = self.func(*args, **kwargs)
    self.signature.returns.validate(result)

    return result

