from langex.errors.misapplication import MisapplicationError
from langex.functions.signature import Signature

class FunctionMeta:
  def __init__(self, func):
    if isinstance(func, FunctionMeta):
      self.name = func.name
      self.func = func.func
      self.signature = func.signature.clone()
      self.is_abstract = func.is_abstract
      self.owner = func.owner
    else:
      self.func = func
      self.name = func.__name__
      self.signature = Signature()
      self.is_abstract = False
      self.owner = None

  def _is_class_function(self):
    parts = self.func.__qualname__.split(".")

    if len(parts) == 1:
      return False

    return parts[-2] != "<locals>"

  def __call__(self, *args, **kwargs):
    self.signature.args.validate(args, kwargs)

    if self.owner:
      args = (self.owner,) + args
    else:
      if self._is_class_function():
        raise MisapplicationError({
          "target": self.func.__qualname__,
          "reason": "Called langex class function without langex class instance"
        })

    result = self.func(*args, **kwargs)
    self.signature.returns.validate(result)

    return result

