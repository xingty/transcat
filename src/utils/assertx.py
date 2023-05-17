from src.web.exception.error import ServiceException,ErrorCode

def isTrue(expression: bool, message: str):
  if not expression:
    raise ServiceException(ErrorCode.FAILED,message)

def notEmpty(value: str, message: str):
  if not value:
    raise ServiceException(ErrorCode.FAILED,message)

def found(value: object, message: str):
  if not value:
    raise ServiceException(ErrorCode.FAILED,message)