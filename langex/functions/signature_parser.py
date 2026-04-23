from langex.constants.keys import LANGEX
from langex.functions.signature import Signature

class SignatureParser:
  def __init__(self, func, qual: str):
    self.func = func
    self.signature = Signature(qual)
    self.returns = self.signature.returns
    self.args = self.signature.args

  def _parse_returns(self):
    annots = self.func.__annotations__
    attacked = LANGEX.ATTACKED_ATTRS.RETURN

    if attacked in annots:
      self.returns.set_return_type(annots[attacked])

  def _parse_pos_static(self):
    annots = self.func.__annotations__
    code = self.func.__code__
    varnames = code.co_varnames
    count = code.co_argcount
    found = varnames[:count]
    defaults = len(self.func.__defaults__ or ())
    optional = {*varnames[-defaults:]}

    for arg in found:
      arg_type = annots.get(arg, object)

      if arg in optional:
        self.args.add_optional_positional(arg_type)
      else:
        self.args.add_positional(arg_type)

  def _parse_pos_dynamic(self):
    code = self.func.__code__
    has_pos_dynamic = (code.co_flags >> 2) & 1
    has_kw_dynamic = (code.co_flags >> 3) & 1

    if not has_pos_dynamic:
      return

    varname = code.co_varnames[-1]

    if has_kw_dynamic:
      varname = code.co_varnames[-2]

    annots = self.func.__annotations__
    arg_type = annots.get(varname, object)
    self.args.add_dynamic_positional(arg_type)

  def _parse_positional(self):
    self._parse_pos_static()
    self._parse_pos_dynamic()

  def _parse_kw_static(self):
    annots = self.func.__annotations__
    code = self.func.__code__
    pos_count = code.co_argcount
    count = code.co_kwonlyargcount
    total = pos_count + count
    found = code.co_varnames[pos_count:total]
    defaults = self.func.__kwdefaults__ or {}

    for arg in found:
      arg_type = annots.get(arg, object)

      if arg in defaults:
        self.args.add_optional_keyword(arg, arg_type)
      else:
        self.args.add_keyword(arg, arg_type)

  def _parse_kw_dynamic(self):
    code = self.func.__code__
    has_dynamic = (code.co_flags >> 3) & 1

    if not has_dynamic:
      return

    varname = code.co_varnames[-1]
    annots = self.func.__annotations__
    arg_type = annots.get(varname, object)
    self.args.add_dynamic_keyword(arg_type)

  def _parse_keyword(self):
    self._parse_kw_static()
    self._parse_kw_dynamic()

  def _parse_args(self):
    self._parse_positional()
    self._parse_keyword()

  def parse(self) -> Signature:
    self._parse_args()
    self._parse_returns()

    return self.signature

