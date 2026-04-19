from langex.classes.class_meta import ClassMeta
from langex.errors.validation import ValidationError
from langex.utils.extracter import extract_methods

def interface(cls):
  cls_meta = ClassMeta(cls)
  cls_meta.is_interface = True
  methods = extract_methods(cls_meta.cls)

  for method_name in methods:
    method = methods[method_name]
    cls_meta.methods_meta.add_abstract_method(method)

  return cls_meta

def abstract(cls):
  cls_meta = ClassMeta(cls)
  cls_meta.is_abstract = True
  methods = extract_methods(cls_meta.cls)

  for method_name in methods:
    method = methods[method_name]

    if method.is_abstract:
      cls_meta.methods_meta.add_abstract_method(method)
    else:
      cls_meta.methods_meta.add_method(method)

  return cls_meta

def implements(*interfaces):
  def decorator(cls):
    class_meta = ClassMeta(cls)

    for interface in interfaces:
      interface = ClassMeta(interface)

      if not interface.is_interface:
        raise ValidationError({
          "target": cls.__name__,
          "source": interface.__name__,
          "reason": "Source is not an interface"
        })

      interface.methods_meta.impose(class_meta.cls)

    return class_meta

  return decorator

