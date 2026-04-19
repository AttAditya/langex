from typing import Self

from langex.functions.args_meta import Args
from langex.functions.returns_meta import Returns

class Signature:
  def __init__(self):
    self.args = Args()
    self.returns = Returns()

  def match_signature(self, signature: Self) -> bool:
    if not self.returns.match_returns(signature.returns):
      return False

    return True

