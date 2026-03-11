from langex.core.use import access_langex

def get_typehints(func):
  lnx = access_langex(func)
  typehints = lnx.callable_meta.typehints
  typehints.has_typehints = True

  return typehints

def return_type(rtype):
  def decorator(func):
    typehints = get_typehints(func)
    typehints.has_return_type = True
    typehints.return_type = rtype

    return func

  return decorator

def pos_args(*args):
  def decorator(func):
    typehints = get_typehints(func)
    typehints.has_pos_args = True
    typehints.pos_args = args

    return func

  return decorator

def kw_args(**kwargs):
  def decorator(func):
    typehints = get_typehints(func)
    typehints.has_kw_args = True
    typehints.kw_args = kwargs

    return func

  return decorator

def extra_pos_args(*arg_types):
  def decorator(func):
    typehints = get_typehints(func)
    typehints.has_pos_args_list = True
    typehints.pos_args_list = list(arg_types)

    return func

  return decorator

def extra_kw_args(**kwargs):
  def decorator(func):
    typehints = get_typehints(func)
    typehints.has_kw_args_dict = True
    typehints.kw_args_dict = kwargs

    return func

  return decorator

__all__ = [
  "return_type",
  "pos_args",
  "kw_args",
  "extra_pos_args",
  "extra_kw_args",
]

