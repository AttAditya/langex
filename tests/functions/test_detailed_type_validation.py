from langex.core.errors import ValidationError
from langex.core.functions import autosig
from langex.core.testing import discover_test, expects

@autosig
def list1(a: list[int], b: list[str]) -> list[bool]:
  return [True, False]

@autosig
def list2() -> list[float]:
  return ["a", "b", "c"]

@autosig
def list3(a: list, b: list) -> list:
  return [True, False]

@autosig
def list4() -> list:
  return ["a", "b", "c"]

@autosig
def list5(a: list[int | str]) -> list[int | str]:
  return a

@autosig
def list6(a: list[int | str]) -> list[int | str]:
  return a + [True]

@autosig
def set1(a: set[int], b: set[str]) -> set[bool]:
  return {True, False}

@autosig
def set2() -> set[float]:
  return {"a", "b", "c"}

@autosig
def set3(a: set, b: set) -> set:
  return {True, False}

@autosig
def dict1(a: dict[str, int], b: dict[int, str]) -> dict[str, bool]:
  return {"a": True, "b": False}

@autosig
def dict2() -> dict[float, str]:
  return {"a": "1", "b": "2", "c": "3"}

@autosig
def dict3(a: dict, b: dict) -> dict:
  return {"a": True, "b": False}

@autosig
def tuple1(a: tuple[int, str], b: tuple[str, int]) -> tuple[bool, bool]:
  return (True, False)

@autosig
def tuple2() -> tuple[float, str]:
  return ("a", "1")

@autosig
def tuple3(a: tuple, b: tuple) -> tuple:
  return (True, False)

@discover_test
def test_detailed_list_validation():
  (lambda: list1([1, 2, 3], ["a", "b", "c"])) @expects ([True, False])
  (lambda: list2()                          ) @expects (ValidationError)
  (lambda: list3([1, 2, 3], ["a", "b", "c"])) @expects ([True, False])
  (lambda: list4()                          ) @expects (["a", "b", "c"])
  (lambda: list5([1, "a", 2, "b"])          ) @expects ([1, "a", 2, "b"])
  (lambda: list6([1, "a", 2, "b", 3, "c"])  ) @expects (ValidationError)

@discover_test
def test_detailed_set_validation():
  (lambda: set1({1, 2, 3}, {"a", "b", "c"})) @expects ({True, False})
  (lambda: set2()                          ) @expects (ValidationError)
  (lambda: set3({1, 2, 3}, {"a", "b", "c"})) @expects ({True, False})

@discover_test
def test_detailed_dict_validation():
  ex_dict1 = {"a": 1, "b": 2}
  ex_dict2 = {1: "a", 2: "b"}
  (lambda: dict1(ex_dict1, ex_dict2)) @expects ({"a": True, "b": False})
  (lambda: dict2()                  ) @expects (ValidationError)
  (lambda: dict3(ex_dict1, ex_dict2)) @expects ({"a": True, "b": False})

@discover_test
def test_detailed_tuple_validation():
  (lambda: tuple1((1, "a"), ("b", 2))) @expects ((True, False))
  (lambda: tuple2()                  ) @expects (ValidationError)
  (lambda: tuple3((1, "a"), ("b", 2))) @expects ((True, False))

