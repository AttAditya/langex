from langex.core.handlers import catch, safe_call
from langex.core.testing import discover_test, expects

@safe_call
def f1():
  print("f1: This will be printed")

  raise ValueError("This is an error")

@catch(Exception, lambda: 1)
def f2():
  print("f2: This will be printed")

  raise ValueError("This is an error")

@discover_test
def test_handlers():
  (lambda: f1()) @expects (None)
  (lambda: f2()) @expects (1)

