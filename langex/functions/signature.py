from typing import Self

from langex.functions.args_meta import Args
from langex.functions.returns_meta import Returns

class Signature:
  def __init__(self, func_name: str):
    self.func_name = func_name
    self.args = Args(self.func_name)
    self.returns = Returns(self.func_name)

  def clone(self):
    new_signature = Signature(self.func_name)
    new_signature.args = self.args.clone()
    new_signature.returns = self.returns.clone()

    return new_signature

  def match_signature(self, signature: Self) -> bool:
    if not self.returns.match_returns(signature.returns):
      return False

    return True

