from langex.errors.langex import LangexError

class MisapplicationError(LangexError):
  def __init__(self, additional_info):
    super().__init__(
      "Misapplication",
      "Implementation error",
      additional_info
    )

