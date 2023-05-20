import sqlite3,threading,time
from queue import Queue
from src.utils import hash
from src.context import datasource
import src.storage.ds_sqlite3 as storage

class TranslateHistory():
  def __init__(self):
    self.queue = Queue()
    self.usageSet = set()
    t = threading.Thread(target=self.run)
    t.daemon = True
    t.start()

  def getByHashId(self,hashId):
    with datasource.getConnection() as conn:
      row = storage.findHistoryByHashId(conn,hashId)
      if not row:
        return None
      
      return dict(row)

  def push(self,data):
    self.queue.put(data)

  def save(self,conn,data):
    length = len(data['source_text'])
    hashId = hash.md5(data['source_text'] + '_' + data['dst'])
    columns = [
      data['sid'],data['src'],data['dst'],
      data['source_text'],data['target_text'],
      hashId,data['engine'],length
    ]

    try:
      storage.addTranslateHistory(conn,columns)
      self.updateUsage(conn,data)
      conn.commit()
    except Exception as e:
      conn.rollback()
  
  def updateUsage(self,conn,data):
    month = time.strftime('%Y-%m')
    key = f'{data["sid"]}_{data["engine"]}_{month}'
    serviceId = hash.md5(key)

    def getUsageByServiceId():
      record = storage.findUsageByServiceId(conn,serviceId)
      if not record:
        cloumns = (serviceId,data['sid'],data['engine'],month)
        storage.insertUsage(conn,cloumns)
        record = storage.findUsageByServiceId(conn,serviceId)

      return dict(record)

    if serviceId not in self.usageSet:
      usage = getUsageByServiceId()
      if usage:
        self.usageSet.add(serviceId)

    count = len(data['source_text'])
    storage.incrementUsageByServiceId(conn,serviceId,count)


  def run(self):
    conn = datasource.getConnection(autoclose=False)
    while True:
      data = self.queue.get()
      self.save(conn,data)
      time.sleep(0.1)

history = TranslateHistory()