from typing import Callable, TypeVar

from langex.constants.keys import LANGEX
from langex.functions.function_meta import FunctionMeta

__all__ = [
  "langex_function",
  "abstracted",
  "no_args",
  "args_required",
  "args_optional",
  "args_dynamic",
  "kwargs_required",
  "kwargs_optional",
  "kwargs_dynamic",
  "returns",
  "autosig",
]

FuncType = TypeVar("FuncType", bound=Callable)

def _prepare_function(func) -> FunctionMeta:
  if not hasattr(func, LANGEX.MARKER):
    return FunctionMeta(func)

  return func

def langex_function(func: FuncType) -> FuncType:
  return _prepare_function(func)

def abstracted(func):
  func = _prepare_function(func)
  func.is_abstract = True

  return func

def no_args(func):
  func = _prepare_function(func)
  func.signature.args.set_no_args()

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

def autosig(func: FuncType) -> FuncType:
  func = _prepare_function(func)
  func.detect_signature()

  return func

