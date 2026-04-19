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

  def __call__(self, *args, **kwargs):
    if self.owner:
      args = (self.owner,) + args

    self.signature.args.validate(args, kwargs)
    result = self.func(*args, **kwargs)
    self.signature.returns.validate(result)

    return result

