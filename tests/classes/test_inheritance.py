from langex.core.classes import abstract, extends
from langex.core.functions import abstracted, autosig
from langex.core.testing import discover_test, expects
from langex.errors.instantiation import InstantiationError

@abstract
class ParentClass:
  @abstracted
  @autosig
  def method1(self, a: int) -> int:
    ...

  @autosig
  def method2(self, b: str) -> str:
    return b.upper()

@extends
class ChildClass(ParentClass):
  def method1(self, a: int) -> int:
    return a * 2
  
@extends
class AnotherChildClass(ParentClass):
  def method1(self, a: int) -> int:
    return a * 3
  
  def method2(self, b: str) -> str:
    return b.lower()

@discover_test
def test_inheritance():
  child1 = ChildClass()
  child2 = AnotherChildClass()
  (lambda: ParentClass()      ) @expects (InstantiationError)
  (lambda: child1.method1(5)   ) @expects (10)
  (lambda: child2.method1(5)   ) @expects (15)
  (lambda: child1.method2("Hi")) @expects ("HI")
  (lambda: child2.method2("Hi")) @expects ("hi")

