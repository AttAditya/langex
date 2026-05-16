def clone_function(f):
  FunctionType = type(f)
  res = FunctionType(
    f.__code__,
    f.__globals__,
    f.__name__,
    f.__defaults__,
    f.__closure__
  )

  res.__dict__.update(f.__dict__.copy())
  res.__kwdefaults__ = f.__kwdefaults__
  res.__doc__ = f.__doc__
  res.__module__ = f.__module__
  res.__annotations__ = f.__annotations__

  return res

