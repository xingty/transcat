
class Select():
  def __init__(self,services) -> None:
    self._services = services
    self._index = 0

  def choose(self,text,src,dst):
    print('index:' + str(self._index))
    return self._services[self._index]
  
  def select(self,index):
    length = len(self._services)
    if index >= length or index < 0:
      raise Exception("Index out of range")
    
    self._index = index

  def allServes(self):
    return self._services