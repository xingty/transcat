import threading
from .exception import TranslactionException,ExceptionType

class BaseTranslator():
  def __init__(self,name,appKey,appId,limit=-1,weight=1,proxy=False):
    self.name = name
    self.appId = appId
    self.appKey = appKey
    self.weight = weight
    self.proxy = proxy
    self.limit = limit
    self.ratelimiter = None
    self._languageMap = self.supportedLanguage()
  
  def translate(self,text,src,dst):
    if not self.support(src,dst):
      raise TranslactionException(None,ExceptionType.SERVICE_NOT_FOUND)

    return self.doTranslate(text,src,dst)

  def doTranslate(self,text,src,dst):
    raise Exception("Implement in subclass")  

  def support(self,src,dst):
    lang = self._languageMap.get(src) or self._languageMap.get('any')
    if not lang:
      return False
    
    return dst in lang or 'any' in lang

  def supportedLanguage(self):
    return {}
  
  def tryAcquire(self):
    return self.ratelimiter == None or self.ratelimiter.acquire()
  
  def maxCharacterAtOnce(self):
    return 10000
