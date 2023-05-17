from enum import Enum

class ErrorCode(Enum):
  SUCCEED = 0
  ACCESS_DENIED = 403
  FAILED = 500

class ServiceException(Exception):
  def __init__(self,code,message, *args: object) -> None:
    super().__init__(*args)
    self.code = code
    self.message = message