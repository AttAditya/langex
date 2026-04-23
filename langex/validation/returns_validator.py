from langex.constants.contents import CONTENTS
from langex.constants.labels import LABELS
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
      LABELS.REF.SELF: self.returns.func_name,
      LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
        X=LABELS.FUNC_NOUNS.RTYPE
      ),
      LABELS.CAUSE.EXPECTED: self.returns.return_type.__name__,
      LABELS.CAUSE.RECEIVED: type(self.returned_value).__name__
    })

