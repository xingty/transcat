import threading
from src.utils.text import buildServiceId

class Usage:
  def __init__(self,serviceId,usage=0,activeConnections=0) -> None:
    self.serviceId = serviceId
    self.usage = usage
    self.activeConnections = activeConnections
    self.lock = threading.Lock()
  
  def updateUsage(self,size):
    with self.lock:
      self.usage += size
      self.activeConnections += 1

class UsageInfo:
  def __init__(self) -> None:
    self.usageMap = {}
    self.lock = threading.Lock()
  
  def getUsageInfo(self,name,tType) -> Usage:
    sid = buildServiceId(name,tType)
    return self.getUsageInfoBySid(sid)
  
  def getUsageInfoBySid(self,sid) -> Usage:
    info = self.usageMap.get(sid) or None
    if info is None:
      with self.lock:
        info = self.usageMap.get(sid) or None
        # double check
        if info is None:
          info = Usage(sid,0,0)
          self.usageMap[sid] = info
    
    return info

  def updateUsageInfo(self,name,tType,textSize):
    info = self.getUsageInfo(name,tType)
    info.updateUsage(textSize)


