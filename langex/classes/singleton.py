from langex.classes.class_meta import ClassMeta

def Singleton(cls):
  instance = ClassMeta(cls).use_primitive()()

  class Wrapper():
    def __call__(self):
      return instance

    def __getattr__(self, name):
      return getattr(instance, name)

    def __setattr__(self, name, value):
      return setattr(instance, name, value)

  return Wrapper()

