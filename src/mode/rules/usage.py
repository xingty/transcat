import sys,random
from src.translator import usageInfo as usage

#用量多优先
class Usage():
  def __init__(self) -> None:
    pass

  def choose(self, text,servers) -> object:
    maxScore = ~sys.maxsize
    candidate = None
    for server in servers:
      info = usage.getUsageInfo(server.name,server.type)
      score = 0
      if server.limit < 0:
        score = sys.maxsize - random.randint(1, 1000)
      else:
        score = server.limit - info.usage

      if score > maxScore:
        maxScore = score
        candidate = server
    return candidate
