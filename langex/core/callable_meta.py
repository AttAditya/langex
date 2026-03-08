class _LangexCallableTypehints:
  def __init__(self):
    self.has_typehints = False
    self.has_return_type = False
    self.has_pos_args = False
    self.has_kw_args = False
    self.has_pos_args_list = False
    self.has_kw_args_dict = False
    self.return_type = None
    self.pos_args = []
    self.kw_args = {}
    self.pos_args_list = []
    self.kw_args_dict = {
      "keys": [],
      "values": [],
    }

  def matches_signature(self, other):
    has_match = [
      self.has_typehints == other.has_typehints,
      self.has_return_type == other.has_return_type,
      self.has_pos_args == other.has_pos_args,
      self.has_kw_args == other.has_kw_args,
      self.has_pos_args_list == other.has_pos_args_list,
      self.has_kw_args_dict == other.has_kw_args_dict,
    ]

    value_match = [
      self.return_type == other.return_type,
      self.pos_args == other.pos_args,
      self.kw_args == other.kw_args,
      self.pos_args_list == other.pos_args_list,
      self.kw_args_dict == other.kw_args_dict,
    ]

    return all(has_match) and all(value_match)

class LangexCallableMeta:
  def __init__(self):
    self.typehints = _LangexCallableTypehints()

__all__ = [
  "LangexCallableMeta",
]

