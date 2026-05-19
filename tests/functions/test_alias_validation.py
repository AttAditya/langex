from langex.core.errors import ValidationError
from langex.core.functions import autosig
from langex.core.testing import discover_test, expects

@autosig
def func1(a: list[str], b: list[int]) -> list[bool]:
  return [True, False]

@autosig
def func2() -> list[float]:
  return ["a", "b", "c"]

@discover_test
def test_alias_validation():
  (lambda: func1([1, 2, 3], ["a", "b", "c"])) @expects ([True, False])
  (lambda: func2()                          ) @expects (ValidationError)

