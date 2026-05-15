from langex.core.classes import implements, interface
from langex.core.functions import args_required, returns

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

instance = ImplementationClass(3)
assert instance.method1(5) == 15
assert instance.method2("hi") == "HIHIHI"

try:
  instance.method1("5")
  assert False

except:
  pass

try:
  instance.method2(5)
  assert False

except:
  pass

