from langex.core.classes import abstract, extends
from langex.core.functions import args_required, autosig, returns
from langex.core.testing import discover_test, expects

@abstract
class Parent:
  def get_name(self) -> str:
    return self.name

  @args_required(int)
  @returns(str)
  def manual_args(self, a: int) -> str:
    return self.name

  @autosig
  def auto_args(self, a: int) -> str:
    return self.name

@extends
class Child1(Parent):
  def __init__(self):
    self.name = "Child 1"

@extends
class Child2(Parent):
  def __init__(self):
    self.name = "Child 2"

@discover_test
def test_persistent_attributes():
  (lambda: Child1().get_name()    ) @expects ("Child 1")
  (lambda: Child2().get_name()    ) @expects ("Child 2")
  (lambda: Child1().manual_args(1)) @expects ("Child 1")
  (lambda: Child2().manual_args(2)) @expects ("Child 2")
  (lambda: Child1().auto_args(1)  ) @expects ("Child 1")
  (lambda: Child2().auto_args(2)  ) @expects ("Child 2")

