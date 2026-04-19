from langex.functions.signature import Signature

class FunctionMeta:
  def __init__(self, func):
    self.func = func
    self.signature = Signature()

  def __call__(self, *args, **kwargs):
    self.signature.args.validate(args, kwargs)
    result = self.func(*args, **kwargs)
    self.signature.returns.validate(result)

    return result

