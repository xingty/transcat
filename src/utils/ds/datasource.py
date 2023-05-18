import sqlite3,os

class AutocloseableConnection:
  def __init__(self,conn):
    self._conn = conn

  def __enter__(self):
    return self._conn
  
  def __exit__(self,exc_type,exc_val,exc_tb):
    if not self._conn:
      return
    
    if exc_type is not None:
      self._conn.rollback()
    else:
      self._conn.commit()
      
    self._conn.close()

class Sqlite3Datasource:
  def __init__(self,dbName) -> None:
    super().__init__()
    self.dbName = dbName

  def init(self,schema):
    if not os.path.exists(self.dbName):
      conn = sqlite3.connect(self.dbName)
      with open(schema) as f:
        schema = f.read()
        conn.executescript(schema)
      conn.close()

  def getConnection(self,autoclose=True):
    conn = sqlite3.connect(self.dbName)
    conn.row_factory = sqlite3.Row
    return AutocloseableConnection(conn) if autoclose else conn