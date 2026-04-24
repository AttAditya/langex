from langex.constants.contents import CONTENTS
from langex.constants.labels import LABELS
from langex.errors.validation import ValidationError
from langex.utils.matcher import matches_any_type, matches_type
from langex.validation.validator import Validator

class KeywordArgsValidator(Validator):
  def __init__(self, args, received_args: dict[str, object]):
    self.args = args
    self.received_args = received_args
    self.required = self.args.keyword
    self.optional = self.args.optional_keyword
    self.dynamic = self.args.dynamic_keyword

  def _partition(self) -> tuple[dict[str, object], ...]:
    required_args = {}
    optional_args = {}
    dynamic_args = {}

    for keyword in self.received_args:
      if keyword in self.required:
        required_args[keyword] = self.received_args[keyword]
      elif keyword in self.optional:
        optional_args[keyword] = self.received_args[keyword]
      else:
        dynamic_args[keyword] = self.received_args[keyword]

    return required_args, optional_args, dynamic_args

  def _validate_required(self, required_args: dict[str, object]):
    missing_args = set()

    for keyword, arg_type in self.required.items():
      if keyword not in required_args:
        missing_args.add(keyword)
        continue

      received_arg = required_args[keyword]

      if not matches_type(received_arg, arg_type):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.FUNC_NOUNS.ARGS_TYPE: arg_type.__name__,
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: keyword
        })

    if len(missing_args) > 0:
      raise ValidationError({
        LABELS.REF.SELF: self.args.func_name,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.MISSING_X.format(
          X=LABELS.FUNC_NOUNS.KWARGS
        ),
        LABELS.CAUSE.MISSING: missing_args
      })

  def _validate_optional(self, optional_args: dict[str, object]):
    if len(optional_args) == 0:
      return

    for keyword, received_arg in optional_args.items():
      arg_type = self.optional[keyword]

      if not matches_type(received_arg, arg_type):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.FUNC_NOUNS.ARGS_TYPE: arg_type.__name__,
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: keyword
        })

  def _validate_dynamic(self, dynamic_args: dict[str, object]):
    if len(dynamic_args) == 0:
      return

    if self.dynamic is None:
      raise ValidationError({
        LABELS.REF.SELF: self.args.func_name,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_NOT_ALLOWED.format(
          X=LABELS.FUNC_NOUNS.DKWARGS
        ),
        LABELS.CAUSE.RECEIVED: dynamic_args
      })

    for keyword, received_arg in dynamic_args.items():
      if not matches_any_type(received_arg, self.dynamic):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.CAUSE.EXPECTED: {cls.__name__ for cls in self.dynamic},
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: keyword
        })

  def validate(self):
    required_args, optional_args, dynamic_args = self._partition()
    self._validate_required(required_args)
    self._validate_optional(optional_args)
    self._validate_dynamic(dynamic_args)

