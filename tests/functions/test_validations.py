from langex.core.errors import ValidationError
from langex.core.functions import args_required, returns
from langex.core.testing import discover_test, expects

@args_required(int)
def func(arg):
  return 0

@args_required(str)
def func2(arg):
  return 0

@args_required(float)
def func3(arg):
  return 0

@args_required(bool)
def func4(arg):
  return 0

@args_required(callable)
def func5(arg):
  return 0

@returns(int)
def func6():
  return 0

@returns(str)
def func7():
  return "0"

@returns(float)
def func8():
  return 0.0

@returns(bool)
def func9():
  return False

@returns(callable)
def func10():
  return lambda: None

@returns(int)
def func11():
  return "0"

@returns(str)
def func12():
  return 0

@returns(float)
def func13():
  return "0"

@returns(bool)
def func14():
  return "0"

@returns(callable)
def func15():
  return "0"

@discover_test
def test_arg_validations():
  (lambda: func(1)            ) @expects (0)
  (lambda: func2("1")         ) @expects (0)
  (lambda: func3(0.0)         ) @expects (0)
  (lambda: func4(True)        ) @expects (0)
  (lambda: func5(lambda: None)) @expects (0)
  (lambda: func("1")          ) @expects (ValidationError)
  (lambda: func2(1)           ) @expects (ValidationError)
  (lambda: func3(0)           ) @expects (ValidationError)
  (lambda: func4(1)           ) @expects (ValidationError)
  (lambda: func5(1)           ) @expects (ValidationError)

@discover_test
def test_return_validations():
  (lambda: func6()           ) @expects (0)
  (lambda: func7()           ) @expects ("0")
  (lambda: func8()           ) @expects (0.0)
  (lambda: func9()           ) @expects (False)
  (lambda: callable(func10())) @expects (True)
  (lambda: func11()          ) @expects (ValidationError)
  (lambda: func12()          ) @expects (ValidationError)
  (lambda: func13()          ) @expects (ValidationError)
  (lambda: func14()          ) @expects (ValidationError)
  (lambda: func15()          ) @expects (ValidationError)

