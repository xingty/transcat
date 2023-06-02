from enum import Enum
from flask import Response
import json

class ErrorCode(Enum):
  SUCCEED = 200
  ACCESS_DENIED = 403
  SERVICE_NOT_FOUND = 410
  FAILED = 500

class ServiceException(Exception):
  def __init__(self,code: ErrorCode,message: str, *args: object) -> None:
    super().__init__(*args)
    self.code = code
    self.message = message


def restExceptionHandler(e: ServiceException):
  response = {
    'code': e.code.value,
    'message': e.message
  }

  headers = {'Content-Type': 'application/json'}
  return Response(json.dumps(response), status=500, headers=headers)