from langex.core.errors import ValidationError
from langex.core.functions import args_required, returns
from langex.core.testing import discover_test, expects

@args_required(int, int)
@returns(int)
def add(a, b):
  return a + b

@discover_test
def test_runtimes_enforcements():
  (lambda: add(1, 2)    ) @expects (3)
  (lambda: add("1", "2")) @expects (ValidationError)

