from langex.core.classes import singleton
from langex.core.errors import ValidationError
from langex.core.functions import autosig
from langex.core.testing import discover_test, expects

@singleton
class IdGenerator:
  def __init__(self, initial = 0):
    self.value = initial

  def next_id(self):
    self.value += 1

    return self.value

  @autosig
  def next_id_with_prefix(self, prefix: str) -> str:
    return f"{prefix}_{self.next_id()}"

@discover_test
def test_singleton():
  id_gen1 = IdGenerator()
  id_gen2 = IdGenerator()
  (id_gen1.next_id                          ) @expects (1)
  (id_gen1.next_id                          ) @expects (2)
  (id_gen2.next_id                          ) @expects (3)
  (lambda: id_gen1 is id_gen2               ) @expects (True)
  (lambda: id_gen1.next_id_with_prefix(0)   ) @expects (ValidationError)
  (lambda: id_gen1.next_id_with_prefix("ID")) @expects ("ID_4")

