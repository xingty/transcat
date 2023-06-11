import threading,time

class TokenBucket():
  def __init__(self,capacity,windowTimeInSeconds) -> None:
    """
    Initializes an instance of the Token Bucket algorithm.
    
    Args:
        capacity (int): The maximum number of tokens that the bucket can hold.
        windowTimeInSeconds (int): The time window in seconds for refilling the bucket.
    
    Returns:
        None
    """
    self.capacity = capacity
    self.fillTokenPerSecond = int(capacity / windowTimeInSeconds)
    assert self.fillTokenPerSecond > 0
    self.lastRefillTime = 0
    self.availableTokens = 0
    self.lock = threading.Lock()

  def acquire(self):
    """
    Acquires a token from the bucket if available. Returns True if a token was successfully acquired,
    False otherwise.
    """
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