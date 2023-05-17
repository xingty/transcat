import sqlite3

class Datasource():
  
  def getConnection(self):
    raise NotImplementedError

class Sqlite3Datasource(Datasource):
  def __init__(self,dbName) -> None:
    super().__init__()
    self.dbName = dbName

  def getConnection(self):
    return sqlite3.connect(self.dbName)