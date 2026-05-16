from langex.core.classes import langex_class
from langex.core.errors import ValidationError
from langex.core.functions import args_dynamic, args_optional, args_required, returns
from langex.core.testing import discover_test, expects

@langex_class
class Test:
  @args_required(int, int)
  @returns(int)
  def add(self, a, b):
    return a + b

  @args_optional(int, int)
  @returns(int)
  def mul(self, a=1, b=1):
    return a * b

  @args_dynamic(int)
  @returns(int)
  def sum_all(self, *args):
    return sum(args)

@discover_test
def test_runtimes_enforcements():
  inst = Test()
  (lambda: inst.add(1, 2)         ) @expects (3)
  (lambda: inst.add("1", "2")     ) @expects (ValidationError)
  (lambda: inst.mul()             ) @expects (1)
  (lambda: inst.mul(2)            ) @expects (2)
  (lambda: inst.mul(2, 3)         ) @expects (6)
  (lambda: inst.mul("2")          ) @expects (ValidationError)
  (lambda: inst.mul(2, "3")       ) @expects (ValidationError)
  (lambda: inst.mul("2", 3)       ) @expects (ValidationError)
  (lambda: inst.mul("2", "3")     ) @expects (ValidationError)
  (lambda: inst.sum_all(1, 2, 3)  ) @expects (6)
  (lambda: inst.sum_all(1, 2, "3")) @expects (ValidationError)

