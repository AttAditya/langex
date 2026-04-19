from langex.errors.validation import ValidationError
from langex.utils.matcher import matches_type
from langex.validation.validator import Validator

class ReturnsValidator(Validator):
  def __init__(self, returns, returned_value: object):
    self.returns = returns
    self.returned_value = returned_value

  def validate(self):
    if not self.returns.has_return:
      return

    if matches_type(
      self.returned_value,
      self.returns.return_type
    ):
      return

    raise ValidationError({
      "message": "Return type mismatch",
      "expected type": self.returns.return_type.__name__,
      "received type": type(self.returned_value).__name__
    })

