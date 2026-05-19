from types import UnionType, GenericAlias

from langex.constants.keys import LANGEX

class _MatchResult:
  def __init__(self):
    self._evaluated = False
    self._value = None

  def evaluate(self, result: bool) -> None:
    self._evaluated = True
    self._value = result

  def evaluated(self) -> bool:
    return self._evaluated

  def get_value(self) -> bool:
    if not self._evaluated:
      raise Exception("Result has not been evaluated yet")

    return self._value

class _MatchArgs:
  def __init__(
    self,
    received_arg: object,
    arg_type: object
  ):
    self.received_arg = received_arg
    self.arg_type = arg_type

def handle_none(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if args.arg_type is not None: return
  result.evaluate(args.received_arg is None)

def handle_callable(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if args.arg_type != callable: return
  result.evaluate(callable(args.received_arg))

def handle_langex_class(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if not hasattr(args.received_arg, LANGEX.MARKER): return
  class_meta = getattr(args.received_arg, LANGEX.CLASS_META)

  if args.arg_type in class_meta.follows:
    result.evaluate(True)

def handle_union_type(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if not isinstance(args.arg_type, UnionType): return
  for union_arg_type in args.arg_type.__args__:
    if matches_type(args.received_arg, union_arg_type):
      result.evaluate(True)
      return

  result.evaluate(False)

def handle_type(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if not isinstance(args.arg_type, type): return
  if type(args.received_arg) == bool:
    result.evaluate(args.arg_type == bool)
    return

  result.evaluate(isinstance(args.received_arg, args.arg_type))

def match_typed_list(recv: list, meta) -> bool:
  arg = meta[0]

  for item in recv:
    if not matches_type(item, arg):
      return False

  return True

def match_typed_set(recv: set, meta) -> bool:
  arg = meta[0]

  for item in recv:
    if not matches_type(item, arg):
      return False

  return True

def match_typed_dict(recv: dict, meta) -> bool:
  key_type = meta[0]
  val_type = meta[1]

  for key, val in recv.items():
    if not matches_type(key, key_type):
      return False

    if not matches_type(val, val_type):
      return False

  return True

def match_typed_tuple(recv: tuple, meta) -> bool:
  if len(recv) != len(meta):
    return False

  for item, arg in zip(recv, meta):
    if not matches_type(item, arg):
      return False

  return True

def handle_type_with_meta(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  if not isinstance(args.arg_type, GenericAlias): return
  origin = args.arg_type.__origin__
  meta = args.arg_type.__args__

  if not isinstance(args.received_arg, origin):
    result.evaluate(False)
    return

  match_func = {
    "list": match_typed_list,
    "set": match_typed_set,
    "dict": match_typed_dict,
    "tuple": match_typed_tuple,
    "fallback": lambda recv, meta: True
  }.get(origin.__name__, "fallback")

  result.evaluate(match_func(args.received_arg, meta))

def handle_default(
  result: _MatchResult, args: _MatchArgs
) -> None:
  if result.evaluated(): return
  result.evaluate(False)

def matches_type(
  received_arg: object,
  arg_type: object
) -> bool:
  result = _MatchResult()
  args = _MatchArgs(received_arg, arg_type)
  handle_none(result, args)
  handle_callable(result, args)
  handle_langex_class(result, args)
  handle_union_type(result, args)
  handle_type(result, args)
  handle_type_with_meta(result, args)
  handle_default(result, args)

  return result.get_value()

def matches_any_type(
  received_arg: object,
  arg_types: set[object]
) -> bool:
  for arg_type in arg_types:
    if matches_type(received_arg, arg_type):
      return True

  return False

def match_arrays(
  arr1: list[object],
  arr2: list[object]
) -> bool:
  if len(arr1) != len(arr2):
    return False

  for obj1, obj2 in zip(arr1, arr2):
    if obj1 != obj2:
      return False

  return True

def match_dicts(
  dict1: dict[str, object],
  dict2: dict[str, object]
) -> bool:
  if dict1.keys() != dict2.keys():
    return False

  for key in dict1.keys():
    if dict1[key] != dict2[key]:
      return False

  return True

def match_sets(
  set1: set[object],
  set2: set[object]
) -> bool:
  return set1 == set2

def match_nullable_sets(
  set1: set[object] | None,
  set2: set[object] | None
) -> bool:
  if set1 is None and set2 is None:
    return True

  if set1 is None or set2 is None:
    return False

  return match_sets(set1, set2)

