from langex.core import access_langex

def _get_typehints(func):
  lnx = access_langex(func)
  typehints = lnx.callable_meta.typehints
  typehints.has_typehints = True

  return typehints

def _match_type(instance, type_class):
  if type_class is callable:
    return callable(instance)

  return isinstance(instance, type_class)

def _validate_pos_args(func, *args):
  typehints = _get_typehints(func)

  if not typehints.has_pos_args:
    return []

  failing_checks = []

  if len(args) < len(typehints.pos_args):
    failing_checks.append("positional arguments minimum count")

  for i, arg in enumerate(args):
    received_type = type(arg)
    expected_type = typehints.pos_args[i]

    if not _match_type(arg, expected_type):
      failing_checks.append(" ".join([
        f"positional argument {i}",
        f"(expected {expected_type.__name__},",
        f"got {received_type.__name__})",
      ]))

  return failing_checks

def _validate_kw_args(func, **kwargs):
  typehints = _get_typehints(func)

  if not typehints.has_kw_args:
    return []

  failing_checks = []

  for kwarg_name, expected_type in typehints.kw_args.items():
    if kwarg_name not in kwargs:
      failing_checks.append(f"keyword argument missing ({kwarg_name})")
      continue

    received_type = type(kwargs[kwarg_name])

    if not _match_type(kwargs[kwarg_name], expected_type):
      failing_checks.append(" ".join([
        f"keyword argument {kwarg_name}",
        f"(expected {expected_type.__name__},",
        f"got {received_type.__name__})",
      ]))

  return failing_checks

def _validate_extra_pos_args(func, *args):
  typehints = _get_typehints(func)

  if not typehints.has_pos_args_list:
    return []

  failing_checks = []
  eligible_types = typehints.pos_args_list
  extra_pos_args = []

  for i in range(len(typehints.pos_args), len(args)):
    extra_pos_args.append(args[i])

  for i in range(len(typehints.pos_args), len(args)):
    for eligible_type in eligible_types:
      if _match_type(args[i], eligible_type):
        break

    else:
      failing_checks.append(" ".join([
        f"extra positional argument {i}",
        f"(expected one of {' '.join([
          t.__name__ for t in eligible_types
        ])},",

        f"got {type(args[i]).__name__})",
      ]))

  return failing_checks

def _validate_extra_kw_args(func, **kwargs):
  typehints = _get_typehints(func)

  if not typehints.has_kw_args_dict:
    return []

  failing_checks = []
  eligible_types = typehints.kw_args_dict
  extra_kw_args = {}

  for kwarg_name, kwarg_value in kwargs.items():
    if kwarg_name not in typehints.kw_args:
      extra_kw_args[kwarg_name] = kwarg_value

  for kwarg_name, kwarg_value in extra_kw_args.items():
    for eligible_type in eligible_types.values():
      if _match_type(kwarg_value, eligible_type):
        break

    else:
      failing_checks.append(" ".join([
        f"extra keyword argument {kwarg_name}",
        f"(expected one of {' '.join([
          t.__name__ for t in eligible_types.values()
        ])},",

        f"got {type(kwarg_value).__name__})",
      ]))

  return failing_checks

def _validate_args(func, *args, **kwargs):
  typehints = _get_typehints(func)

  if not typehints.has_typehints:
    return []

  failing_checks = []
  failing_checks.extend(_validate_pos_args(func, *args))
  failing_checks.extend(_validate_kw_args(func, **kwargs))
  failing_checks.extend(_validate_extra_pos_args(func, *args))
  failing_checks.extend(_validate_extra_kw_args(func, **kwargs))

  return failing_checks

def _validate_return(func, result):
  typehints = _get_typehints(func)

  if not typehints.has_return_type:
    return []

  if not _match_type(result, typehints.return_type):
    return ["return type"]

  return []

def _raise_validation_error(func, failed_checks):
  raise TypeError(" ".join([
    f"Function {func.__name__} failed type checks for:",
    ", ".join(failed_checks),
  ]))

def enforce_types(func):
  def decorator(*args, **kwargs):
    failed_checks = _validate_args(func, *args, **kwargs)

    if failed_checks:
      _raise_validation_error(func, failed_checks)

    result = func(*args, **kwargs)
    failed_checks = _validate_return(func, result)

    if failed_checks:
      _raise_validation_error(func, failed_checks)

    return result

  return decorator

__all__ = [
  "enforce_types",
]

