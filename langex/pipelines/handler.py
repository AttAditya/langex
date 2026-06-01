class Pipeline:
  def __init__(self):
    self._steps = []

  def run(self, initial_value=None):
    result = initial_value

    for step_func in self._steps:
      result = step_func(result)

    return result

  def __rshift__(self, other):
    instance = self if len(self._steps) else self.__class__()
    instance._steps.append(other)

    return instance

  def __or__(self, value):
    return self.__rshift__(value)

  def __call__(self, initial_value=None):
    return self.run(initial_value)

