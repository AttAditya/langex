from types import UnionType

def matches_type(
  received_arg: object,
  arg_type: object
) -> bool:
  if arg_type is None:
    return received_arg is None

  if arg_type == callable:
    return callable(received_arg)

  if isinstance(arg_type, type) or isinstance(arg_type, UnionType):
    return isinstance(received_arg, arg_type)

  if hasattr(received_arg, "ancestors"):
    if arg_type in received_arg.ancestors:
      return True
    
    for ancestor in received_arg.ancestors:
      if isinstance(received_arg, ancestor.cls):
        return True

  if hasattr(arg_type, "cls"):
    return isinstance(received_arg, arg_type.cls)
  
  return False

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

