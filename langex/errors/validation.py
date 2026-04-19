from langex.errors.langex import LangexError

class ValidationError(LangexError):
  def __init__(self, additional_info: dict[str, str]):
    super().__init__("Validation", "Validation failed", additional_info)

