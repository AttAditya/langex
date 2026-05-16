from langex.core.classes import singleton
from langex.core.testing import discover_test, expects

@singleton
class IdGenerator:
  def __init__(self, initial = 0):
    self.value = initial

  def next_id(self):
    self.value += 1

    return self.value

@discover_test
def test_singleton():
  id_gen1 = IdGenerator()
  id_gen2 = IdGenerator()
  (id_gen1.next_id           ) @expects (1)
  (id_gen1.next_id           ) @expects (2)
  (id_gen2.next_id           ) @expects (3)
  (lambda: id_gen1 is id_gen2) @expects (True)

