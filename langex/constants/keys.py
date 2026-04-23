class LANGEX:
  MARKER = "__langex__"
  CLASS_META = "__langex_class_meta__"
  FUNC_META = "__langex_function_meta__"

  class CLASS_TYPE:
    UNSET = "unset"
    PRIMITIVE = "primitive"
    INTERFACE = "interface"
    ABSTRACT = "abstract"

  class METHOD_TYPE:
    UNSET = "unset"
    IMPLEMENTED = "implemented"
    ABSTRACTED = "abstracted"

  class ATTACKED_ATTRS:
    NEW = "__new__"
    RETURN = "return"

