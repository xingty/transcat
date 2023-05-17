import hashlib

def md5(val:str):
  return hashlib.md5(val.encode('utf-8')).hexdigest()