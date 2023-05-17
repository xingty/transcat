import threading

class ThreadSafeCounter():
  def __init__(self,counter=0):
    self.lock = threading.Lock()
    self.counter = counter

  def get(self):
    return self.counter
  
  def increment(self,num=1):
    with self.lock:
      self.counter += num

  def incrementAndGet(self,num=1):
    with self.lock:
      self.counter += num
      return self.counter

  def decrementAndGet(self,num=1):
    with self.lock:
      self.counter -= num
      return self.counter