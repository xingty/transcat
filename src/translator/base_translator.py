from src.utils.thread_safe_counter import ThreadSafeCounter
import threading

class BaseTranslator():
  def __init__(self,name,appKey,appId,limit=-1,weight=1,proxy=False):
    self.name = name
    self.appId = appId
    self.appKey = appKey
    self.weight = weight
    self.activeConnections = 0
    self.usage = 0
    self.proxy = proxy
    self.limit = limit
    
    self.lock = threading.Lock()
    self.ratelimiter = None
    self._languageMap = self.supportedLanguage()
  
  def translate(self,text,src,dst):
    if not self.support(src,dst):
      raise Exception(f'Language not supported {src} -> {dst} by {self.name}')

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

  def updateState(self,size): 
    """
    Thread safe method
    Update the state of the translator
    """
    with self.lock:
      self.usage += size
      self.activeConnections += 1
  
  def maxCharacterAtOnce(self):
    return 10000
