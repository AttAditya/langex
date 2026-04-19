from langex.functions.function_meta import FunctionMeta

def _prepare_function(func):
  if not isinstance(func, FunctionMeta):
    return FunctionMeta(func)

  return func

def args_required(*arg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for arg in arg_types:
      func.signature.args.add_positional(arg)

    return func

  return decorator

def args_optional(*arg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for arg in arg_types:
      func.signature.args.add_optional_positional(arg)

    return func

  return decorator

def args_dynamic(*arg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for arg in arg_types:
      func.signature.args.add_dynamic_positional(arg)

    return func

  return decorator

def kwargs_required(**kwarg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for name, arg in kwarg_types.items():
      func.signature.args.add_keyword(name, arg)

    return func

  return decorator

def kwargs_optional(**kwarg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for name, arg in kwarg_types.items():
      func.signature.args.add_optional_keyword(name, arg)

    return func

  return decorator

def kwargs_dynamic(*kwarg_types: object):
  def decorator(func):
    func = _prepare_function(func)

    for arg in kwarg_types:
      func.signature.args.add_dynamic_keyword(arg)

    return func

  return decorator

def returns(return_type: object):
  def decorator(func):
    func = _prepare_function(func)
    func.signature.returns.set_return_type(return_type)

    return func

  return decorator

