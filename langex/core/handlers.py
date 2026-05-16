from typing import Callable, TypeVar

from langex.handlers.err_handlers import error_handler

__all__ = [
  "catch",
  "safe_call",
]

FuncType = TypeVar("FuncType", bound=Callable)

def catch(exception_type, fallback) -> Callable[[FuncType], FuncType]:
  return error_handler(exception_type, fallback)

def safe_call(func: FuncType) -> FuncType:
  return error_handler(Exception, lambda: None)(func)

