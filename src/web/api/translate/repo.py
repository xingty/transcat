import sqlite3,threading,time
from queue import Queue
from src.utils import hash

class TranslateHistory():
  def __init__(self):
    self.queue = Queue()
    self.usageSet = set()
    t = threading.Thread(target=self.run)
    t.daemon = True
    t.start()

  def getByHashId(self,hashId):
    conn = sqlite3.connect('data/data.db')
    conn.row_factory = sqlite3.Row
    result = conn.execute('select * from translate_history where hash_id = ? order by id desc',(hashId,)).fetchone()
    if not result:
      return None
    
    conn.close()
    return dict(result)

  def push(self,data):
    self.queue.put(data)

  def save(self,conn,data):
    length = len(data['source_text'])
    hashId = hash.md5(data['source_text'] + '_' + data['dst'])
    columns = [
      data['sid'],data['src'],data['dst'],data['source_text'],data['target_text'],hashId,data['engine'],length
    ]
    conn.execute('insert into translate_history (sid,src,dst,source_text,target_text,hash_id,engine,text_length)' 
                 + 'values (?,?,?,?,?,?,?,?)',columns)
    
    self.updateUsage(conn,data)

    conn.commit()
  
  def updateUsage(self,conn,data):
    month = time.strftime('%Y-%m')
    key = f'{data["sid"]}_{data["engine"]}_{month}'
    serviceId = hash.md5(key)

    def getUsageByServiceId():
      record = conn.execute('select * from service_usage where service_id = ?',(serviceId,)).fetchone()
      if not record:
        conn.execute(
          'insert into service_usage (service_id,name,engine,usage,month_key) values (?,?,?,0,?)',
          (serviceId,data['sid'],data['engine'],month)
        )
        record = conn.execute('select * from service_usage where service_id = ?',(serviceId,)).fetchone()

      return dict(record)

    if serviceId not in self.usageSet:
      usage = getUsageByServiceId()
      if usage:
        self.usageSet.add(serviceId)

    count = len(data['source_text'])
    conn.execute('update service_usage set usage = usage + ? where service_id = ?',(count,serviceId,))


  def run(self):
    conn = sqlite3.connect('data/data.db')
    conn.row_factory = sqlite3.Row
    while True:
      data = self.queue.get()
      self.save(conn,data)
      time.sleep(0.1)
