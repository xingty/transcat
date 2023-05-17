import threading,time

class TokenBucket():
  def __init__(self,capacity,windowTimeInSeconds) -> None:
    self.capacity = capacity
    self.fillTokenPerSecond = int(capacity / windowTimeInSeconds)
    assert self.fillTokenPerSecond > 0
    self.lastRefillTime = 0
    self.availableTokens = 0
    self.lock = threading.Lock()

  def acquire(self):
    with self.lock:
      now = int(time.time())
      elapsed = now - self.lastRefillTime
      tokens = elapsed * self.fillTokenPerSecond + self.availableTokens
      if tokens > 0:
        self.lastRefillTime = now
        self.availableTokens = tokens if tokens < self.capacity else self.capacity
      
      if self.availableTokens <= 0:
        return False

      self.availableTokens -= 1
      return True