from src.translator.exception import TranslactionException,ExceptionType

class LoadBalancer():
  def __init__(self,services,rule):
    self._services = [ t for t in services if t.mode is None or 'load-balance' in t.mode ]
    self._rule = rule

  def choose(self,text,src,dst):
    services = list(self.getAvailable(text,src,dst))
    if not services or len(services) <= 0:
      raise TranslactionException(None,ExceptionType.SERVICE_NOT_FOUND,{'text': text, 'src': src, 'dst': dst})

    return self._rule.choose(text,services)

  def getAvailable(self,text,src,dst):
    return filter(lambda s: s.support(src,dst),self._services)
  
  def allServes(self):
    return self._services
