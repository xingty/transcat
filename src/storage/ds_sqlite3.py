FIND_BY_SERVICE_ID = 'select * from service_usage where service_id = ?'
INSERT_USAGE = 'insert into service_usage (service_id,name,engine,usage,month_key) values (?,?,?,0,?)'
INCREMENT_USAGE = 'update service_usage set usage = usage + ? where service_id = ?'

INSERT_HISTORY ='insert into translate_history (sid,src,dst,source_text,target_text,hash_id,engine,text_length) values (?,?,?,?,?,?,?,?)'
FIND_BY_HASH_ID = 'select * from translate_history where hash_id = ? order by id desc'


def findUsageByServiceIds(conn,serviceIds):
  query = 'select * from service_usage where service_id in ({})'.format(','.join('?' * len(serviceIds)))
  return conn.execute(query,serviceIds).fetchall()

def insertUsage(conn,columns):
  return conn.execute(INSERT_USAGE,columns)

def incrementUsageByServiceId(conn,serviceId,amount):
  return conn.execute(INCREMENT_USAGE,(amount,serviceId,))

def findUsageByServiceId(conn,serviceId):
  return conn.execute(FIND_BY_SERVICE_ID,(serviceId,)).fetchone()

def findHistoryByHashId(conn,hashId):
  return conn.execute(FIND_BY_HASH_ID,(hashId,)).fetchone()

def addTranslateHistory(conn,columns):
  return conn.execute(INSERT_HISTORY,columns)