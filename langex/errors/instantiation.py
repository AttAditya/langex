from langex.errors.langex import LangexError

class InstantiationError(LangexError):
  def __init__(self, additional_info):
    super().__init__(
      "Instantiation",
      "Instantiation failed",
      additional_info
    )

