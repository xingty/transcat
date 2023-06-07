
class Select():
  def __init__(self,services) -> None:
    self._services = [ t for t in services if t.mode is None or 'select' in t.mode ]
    self._index = 0

  def choose(self,text,src,dst):
    return self._services[self._index]
  
  def select(self,index):
    length = len(self._services)
    if index >= length or index < 0:
      raise Exception("Index out of range")
    
    self._index = index

  def allServices(self):
    return self._services