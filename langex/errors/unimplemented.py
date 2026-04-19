from langex.errors.langex import LangexError

class UnimplementedError(LangexError):
  def __init__(self, additional_info):
    super().__init__(
      "Unimplemented",
      "Implementation missing",
      additional_info
    )

