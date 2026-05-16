def error_handler(exception_type, fallback):
  def wrapper(func):
    def inner(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except exception_type:
        return fallback()

    return inner

  return wrapper

