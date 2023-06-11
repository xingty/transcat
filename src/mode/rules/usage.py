import sys,random
from src.translator import usageInfo as usage

#用量多优先
class Usage():
  def __init__(self) -> None:
    pass

  def choose(self, text,servers) -> object:
    """
    Choose the best server to handle the given text from a list of servers.
    
    Args:
        text (str): The text to be processed.
        servers (list): A list of available servers to choose from.
        
    Returns:
        object: The server object with the highest score based on its usage info and limit.
    """
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
