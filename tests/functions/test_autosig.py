from langex.core.classes import langex_class
from langex.core.functions import autosig
from langex.core.testing import discover_test, expects
from langex.errors.validation import ValidationError

@autosig
def mul(a: int, b: int) -> int:
  return a * b

@autosig
def mul_optional(a: int = 1, b: int = 1) -> int:
  return a * b

@langex_class
class Test:
  @autosig
  def add(self, a: int, b: int) -> int:
    return a + b

  @autosig
  def sum_all(self, *args: int) -> int:
    return sum(args)

@discover_test
def test_runtimes_enforcements():
  inst = Test()
  (lambda: mul(2, 3)              ) @expects (6)
  (lambda: mul("2", "3")          ) @expects (ValidationError)
  (lambda: inst.add(1, 2)         ) @expects (3)
  (lambda: inst.add("1", "2")     ) @expects (ValidationError)
  (lambda: mul_optional()         ) @expects (1)
  (lambda: mul_optional(2)        ) @expects (2)
  (lambda: mul_optional(2, 3)     ) @expects (6)
  (lambda: mul_optional("2")      ) @expects (ValidationError)
  (lambda: mul_optional(2, "3")   ) @expects (ValidationError)
  (lambda: mul_optional("2", 3)   ) @expects (ValidationError)
  (lambda: mul_optional("2", "3") ) @expects (ValidationError)
  (lambda: inst.sum_all(1, 2, 3)  ) @expects (6)
  (lambda: inst.sum_all(1, 2, "3")) @expects (ValidationError)

