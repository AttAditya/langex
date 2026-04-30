from traceback import extract_tb

class LangexError(Exception):
  def __init__(
    self,
    type: str,
    message: str,
    additional_info: dict[str, object]
  ):
    super().__init__(f"Langex Error: {message}")
    self.type = type
    self.additional_info = additional_info

  def get_traceback(self):
    result = []
    tb_list = extract_tb(self.__traceback__)

    for tb in tb_list:
      result.append(f"  {tb.filename} {tb.lineno}")

    initial_count = result[-1].count("langex") if result else 0

    while result and result[-1].count("langex") >= initial_count:
      result.pop()

    return "\n".join(result)

  def __str__(self):
    err_text = f"Langex Error ({self.type})\n"
    err_text += "Traceback:\n"
    err_text += self.get_traceback() + "\n\n"
    err_text += "Additional Information:\n"

    for key, value in self.additional_info.items():
      err_text += f"  {key}: {value}\n"

    return err_text

