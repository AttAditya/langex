class LangexError(Exception):
  def __init__(
    self,
    type: str,
    message: str,
    additional_info: dict[str, object]
  ):
    self.type = type
    self.additional_info = additional_info
    super().__init__(f"Langex Error: {message}")

  def __str__(self):
    err_text = f"Langex Error ({self.type})\n"
    err_text += "Additional Information:\n"

    for key, value in self.additional_info.items():
      err_text += f"  {key}: {value}\n"

    return err_text

