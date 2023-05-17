from src.utils.thread_safe_counter import ThreadSafeCounter

class RoundRobin():
  def __init__(self):
    self.counter = ThreadSafeCounter(0)

  def choose(self,text,servers) -> object:
    mod = len(servers)
    index = self.counter.incrementAndGet() % mod
    
    return servers[index]