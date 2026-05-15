from langex.core.classes import implements, interface
from langex.core.functions import args_required, returns
from langex.core.testing import expects, discover_test
from langex.errors.validation import ValidationError

@interface
class InterfaceClass:
  @args_required(int)
  @returns(int)
  def method1(self, a: int) -> int:
    ...

  @args_required(str)
  @returns(str)
  def method2(self, b: str) -> str:
    ...

@implements(InterfaceClass)
class ImplementationClass:
  def __init__(self, factor):
    self.factor = factor

  def method1(self, a: int) -> int:
    return a * self.factor

  def method2(self, b: str) -> str:
    return b.upper() * self.factor

@discover_test
def test_interface():
  inst = ImplementationClass(3)

  def test_instance():
    return 0

  test_instance @expects (0)
  test_instance @expects (0)
  # test_instance @expects_like (lambda x: x in [0, 1, 2])
  (lambda: inst.method1(5)   ) @expects (15)
  (lambda: inst.method2("hi")) @expects ("HIHIHI")
  (lambda: inst.method1("5") ) @expects (ValidationError)
  (lambda: inst.method2(5)   ) @expects (ValidationError)

