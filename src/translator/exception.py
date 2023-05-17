from enum import Enum

class ExceptionType(Enum):
  UNKNOWN = 0
  NETWORK = 1
  REQUEST_LIMIT = 2
  SERVICE_NOT_FOUND = 3


class TranslactionException(Exception):
  def __init__(self,engine,etype,data=None, *args: object) -> None:
    super().__init__(*args)
    self.engine = engine
    self.data = data
    self.etype = etype