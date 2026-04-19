from typing import Self

from langex.validation.kw_args_validator import KeywordArgsValidator
from langex.validation.pos_args_validator import PositionalArgsValidator

from langex.utils.matcher import (
  match_arrays,
  match_dicts,
  match_nullable_sets
)

class Args:
  def __init__(self):
    self.has_args = False
    self.positional: list[object] = []
    self.keyword: dict[str, object] = {}
    self.optional_positional: list[object] = []
    self.optional_keyword: dict[str, object] = {}
    self.dynamic_positional: set[object] | None = None
    self.dynamic_keyword: set[object] | None = None

  def add_positional(self, arg_type: object):
    self.has_args = True
    self.positional.append(arg_type)

  def add_keyword(self, name: str, arg_type: object):
    self.has_args = True
    self.keyword[name] = arg_type

  def add_optional_positional(self, arg_type: object):
    self.has_args = True
    self.optional_positional.append(arg_type)

  def add_optional_keyword(self, name: str, arg_type: object):
    self.has_args = True
    self.optional_keyword[name] = arg_type

  def add_dynamic_positional(self, arg_type: object):
    self.has_args = True

    if self.dynamic_positional is None:
      self.dynamic_positional = set()

    self.dynamic_positional.add(arg_type)

  def add_dynamic_keyword(self, arg_type: object):
    self.has_args = True

    if self.dynamic_keyword is None:
      self.dynamic_keyword = set()

    self.dynamic_keyword.add(arg_type)

  def validate(
    self,
    pos_args: list[object],
    kw_args: dict[str, object]
  ):
    if not self.has_args:
      return

    PositionalArgsValidator(self, pos_args).validate()
    KeywordArgsValidator(self, kw_args).validate()

  def match_args(self, args: Self) -> bool:
    failing_conditions = [
      self.has_args != args.has_args,
      not match_arrays(
        self.positional,
        args.positional
      ),
      not match_dicts(
        self.keyword,
        args.keyword
      ),
      not match_arrays(
        self.optional_positional,
        args.optional_positional
      ),
      not match_dicts(
        self.optional_keyword,
        args.optional_keyword
      ),
      not match_nullable_sets(
        self.dynamic_positional,
        args.dynamic_positional
      ),
      not match_nullable_sets(
        self.dynamic_keyword,
        args.dynamic_keyword
      )
    ]

    return not any(failing_conditions)

