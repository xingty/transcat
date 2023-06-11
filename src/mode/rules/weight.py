import sys
from src.translator import usageInfo as usage

class Weight():
  def __init__(self) -> None:
    pass
  
  def choose(self, text,servers) -> object:
    """
    Choose the server with the lowest score.

    :param text: A string representing the text to be processed.
    :param servers: A list of server objects to choose from.
    :return: The server object with the lowest score.
    """
    minScore = sys.maxsize
    candidate = None
    for server in servers:
      info = usage.getUsageInfo(server.name,server.type)
      score = info.activeConnections * (10000 / server.weight)
      if score < minScore:
        minScore = score
        candidate = server
    return candidate