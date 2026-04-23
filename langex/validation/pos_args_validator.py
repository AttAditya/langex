from langex.constants.contents import CONTENTS
from langex.constants.labels import LABELS
from langex.errors.validation import ValidationError
from langex.utils.matcher import matches_any_type, matches_type
from langex.validation.validator import Validator

class PositionalArgsValidator(Validator):
  def __init__(self, args, received_args: list[object]):
    self.args = args
    self.received_args = received_args
    self.required = self.args.positional
    self.optional = self.args.optional_positional
    self.dynamic = self.args.dynamic_positional

  def _partition(self) -> tuple[list[object], ...]:
    required_args = []
    optional_args = []
    dynamic_args = []

    for idx, arg in enumerate(self.received_args):
      if idx < len(self.required):
        required_args.append(arg)
      elif idx < len(self.required) + len(self.optional):
        optional_args.append(arg)
      else:
        dynamic_args.append(arg)

    return required_args, optional_args, dynamic_args

  def _validate_required(self, required_args: list[object]):
    if len(required_args) < len(self.required):
      raise ValidationError({
        LABELS.REF.SELF: self.args.func_name,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.MISSING_X.format(
          X=LABELS.FUNC_NOUNS.ARGS
        ),
        LABELS.CAUSE.EXPECTED: len(self.required),
        LABELS.CAUSE.RECEIVED: len(required_args)
      })

    for idx, arg_type in enumerate(self.required):
      received_arg = required_args[idx]

      if not matches_type(received_arg, arg_type):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.FUNC_NOUNS.ARGS_TYPE: arg_type.__name__,
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: idx
        })

  def _validate_optional(self, optional_args: list[object]):
    if len(optional_args) == 0:
      return

    offset_idx = len(self.required)

    for idx, received_arg in enumerate(optional_args):
      arg_type = self.optional[idx]

      if not matches_type(received_arg, arg_type):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.FUNC_NOUNS.ARGS_TYPE: arg_type.__name__,
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: idx + offset_idx
        })

  def _validate_dynamic(self, dynamic_args: list[object]):
    if len(dynamic_args) == 0:
      return

    offset_idx = len(self.required) + len(self.optional)

    if self.dynamic is None:
      raise ValidationError({
        LABELS.REF.SELF: self.args.func_name,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.X_NOT_ALLOWED.format(
          X=LABELS.FUNC_NOUNS.DARGS
        ),
        LABELS.CAUSE.RECEIVED: len(self.received_args)
      })

    for idx, received_arg in enumerate(dynamic_args):
      if not matches_any_type(received_arg, self.dynamic):
        raise ValidationError({
          LABELS.REF.SELF: self.args.func_name,
          LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
            X=LABELS.FUNC_NOUNS.ARGS_TYPE
          ),
          LABELS.CAUSE.EXPECTED: {cls.__name__ for cls in self.dynamic},
          LABELS.FUNC_NOUNS.RECV_TYPE: type(received_arg).__name__,
          LABELS.FUNC_NOUNS.ARGS_IDX: idx + offset_idx
        })

  def validate(self):
    required_args, optional_args, dynamic_args = self._partition()
    self._validate_required(required_args)
    self._validate_optional(optional_args)
    self._validate_dynamic(dynamic_args)

