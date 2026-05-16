from langex.constants.contents import CONTENTS
from langex.constants.keys import LANGEX
from langex.constants.labels import LABELS
from langex.errors.misapplication import MisapplicationError
from langex.functions.signature import Signature
from langex.functions.signature_parser import SignatureParser
from langex.utils.cloner import clone_function

class FunctionMeta:
  def __init__(self, func):
    if hasattr(func, LANGEX.FUNC_META):
      return

    if type(func) != type(lambda: None):
      arg_type = type(func).__name__

      if arg_type == "type":
        arg_type = LABELS.CLASS_NOUNS.CLASS_TYPE

      raise MisapplicationError({
        LABELS.REF.SELF: func.__qualname__,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.CONTRADICTING_X.format(
          X=LABELS.FUNC_NOUNS.ARGS_TYPE
        ),
        LABELS.CAUSE.EXPECTED: LABELS.FUNC_NOUNS.FUNC_TYPE,
        LABELS.CAUSE.RECEIVED: arg_type,
      })

    self.func = func
    self.name = func.__name__
    self.qual = func.__qualname__
    self.bounded = self.check_class_bound()
    self.signature = Signature(self.qual)
    self.is_abstract = False
    self._inject()

  def _inject(self):
    setattr(self, LANGEX.MARKER, True)
    setattr(self, LANGEX.FUNC_META, self)

  def check_class_bound(self):
    parts = self.qual.split(".")

    if len(parts) < 2:
      return False

    return parts[-2] != "<locals>"

  def clone(self):
    return self.__class__(
      clone_function(self.func)
    )

  def __call__(self, *args, **kwargs):
    if self.is_abstract:
      raise MisapplicationError({
        LABELS.REF.SELF: self.qual,
        LABELS.CAUSE.REASON: CONTENTS.ERRORS.CANNOT_A_X.format(
          A=LABELS.ACTS.CALL,
          X=LABELS.FUNC_NOUNS.ABS_FUNC
        ),
      })

    self.signature.args.validate(args, kwargs)
    result = self.func(*args, **kwargs)
    self.signature.returns.validate(result)

    return result

  def detect_signature(self):
    parser = SignatureParser(self.func, self.qual)
    self.signature = parser.parse()

