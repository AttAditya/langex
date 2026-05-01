class Singleton:
  def __init__(self, cls):
    self.cls = cls
    self.instance = None

  def __call__(self, *args, **kwargs):
    if self.instance is None:
      self.instance = self.cls(*args, **kwargs)

    return self.instance

  def __getattr__(self, name):
    if self.instance is None:
      self.instance = self.cls()

    return getattr(self.instance, name)

