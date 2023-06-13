import requests
import logging

class NetworkException(Exception):
  def __init__(self,code,message, *args: object) -> None:
    super().__init__(*args)
    self.statusCode = code
    self.message = message

  def __str__(self) -> str:
    return f'code => {self.statusCode}, message => {self.message}'

def post(url,data,headers=None,proxy=None):
  return _sendRequest(
    url=url,
    method='POST',
    data=data,
    params=None,
    headers=headers,
    proxy=proxy
  )

def get(url,params=None,headers=None,proxy=None):
  return _sendRequest(
    url=url,
    method='GET',
    data=None,
    params=params,
    headers=headers,
    proxy=proxy
  )

def _sendRequest(url,method,data,params=None,headers=None,proxy=None):
  proxies = None
  if proxy:
      proxies = { "http": proxy, "https": proxy }
  
  res = requests.request(
    method,url,
    data=data,
    params=params,
    headers=headers,
    proxies=proxies
  )

  if not res.ok:
    logging.debug("NetworkException: url=%s,status_code=%s, text=%s",url,res.status_code,res.text)
    raise NetworkException(res.status_code,res.text)
  
  return res
  