from typing import Callable, TypeVar

from langex.testing.helpers import TestHelpers

__all__ = [
  "expects",
  "discover_test",
  "run_tests",
]

FuncType = TypeVar("FuncType", bound=Callable)
_test_helpers = TestHelpers()
expects = _test_helpers.Expects

def discover_test(func: FuncType) -> FuncType:
  return _test_helpers.discover_test(func)

def run_tests(initial_file: str, module_name: str):
  _test_helpers.run_tests(initial_file, module_name)

