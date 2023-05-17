import sys

class Weight():
  def __init__(self) -> None:
    pass
  
  def choose(self, text,servers) -> object:
    minScore = sys.maxsize
    candidate = None
    for server in servers:
      score = server.activeConnections * (10000 / server.weight)
      if score < minScore:
        minScore = score
        candidate = server
    return candidate