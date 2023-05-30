from enum import Enum
from flask import Response
import json

class ErrorCode(Enum):
  SUCCEED = 0
  ACCESS_DENIED = 403
  FAILED = 500

class ServiceException(Exception):
  def __init__(self,code,message, *args: object) -> None:
    super().__init__(*args)
    self.code = code
    self.message = message


def restExceptionHandler(e):
  ec: ErrorCode = e.code
  response = {
    'code': ec.value,
    'message': e.message
  }

  headers = {'Content-Type': 'application/json'}
  return Response(json.dumps(response), status=500, headers=headers)