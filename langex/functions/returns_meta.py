from typing import Self

from langex.validation.returns_validator import ReturnsValidator

class Returns:
  def __init__(self):
    self.has_return = False
    self.return_type = None

  def set_return_type(self, return_type: object):
    self.has_return = True
    self.return_type = return_type

  def clone(self):
    new_returns = Returns()
    new_returns.has_return = self.has_return
    new_returns.return_type = self.return_type

    return new_returns

  def validate(self, returned_value: object):
    ReturnsValidator(self, returned_value).validate()

  def match_returns(self, returns: Self) -> bool:
    if self.has_return != returns.has_return:
      return False

    if self.return_type != returns.return_type:
      return False

    return True

