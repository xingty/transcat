import hashlib, json, time

def verify(params,secret):
  """
  Verify if the request signature is valid.
  
  Args:
  - params (dict): A dictionary containing the request parameters.
  - secret (str): A secret key to be used in the signature verification.
  
  Raises:
  - Exception: If the request is staled or the signature verification failed.
  """
  timestamp = params['timestamp']
  now = int(time.time())
  if now - timestamp > 300:
    raise Exception('The request is staled.')
  
  def truncate(text):
    l = len(text)
    if (l <= 20):
      return text
    
    return text[0:10] + str(l) + text[-10:]

  text = truncate(params['text'])
  salt = params['salt']
  str = text + salt + timestamp + secret
  sign = hashlib.sha1(str.encode('utf-8')).hexdigest()

  if (sign != params['sign']):
    raise Exception('Signature verification failed.')




