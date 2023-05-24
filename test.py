import logging

# result = caiyun.translate('有时候我也想去旅游', 'auto', 'en
# result = baidu.translate('你好', 'zh', 'en')
# print(result)

# google = Google('google1',7,3)
# result = google.translate('Gives administrators the ability to assign different weights to each server', 'en', 'zh')
# print(result)

# deeplx = DeepLX('deeplx1')
# result = deeplx.translate('hey, i need some translators', 'en', 'zh')
# print(result)
# print(result)
# caiyun.doTranslate('The world’s oldest ultramarathon runner is racing against death','auto','zh')

# testEngine()
# from pl import translate
# print(translate('hey, i need a translator'))

# for i in range(100):
#   service = lb.choose('hello world','en','zh')
#   print('--' * 30)
#   print(f'before name: {service.getName()} usage: {service.getUsage()}, conn: {service.getActiveConnections()}')
#   service.updateState(len('hello world'))
#   print(f'after name: {service.getName()} usage: {service.getUsage()}, conn: {service.getActiveConnections()}')
#   print('--' * 30 + "\n")
from src.utils.ds.datasource import Sqlite3Datasource
import src.storage.ds_sqlite3 as storage
def testFindServiceIds():
  # ds = Sqlite3Datasource("assets/data.db")
  rows = storage.findUsageByServiceIds([
    '3715311b47edfa56dfb48f758ac3ce28',
    'f314efffb523de9cff81c40c728943d9'
  ])
  rows = [dict(row) for row in rows]

  print(rows)

def testFindServiceId():
  # ds = Sqlite3Datasource("assets/data.db")
  row = storage.findUsageByServiceId('3715311b47edfa56dfb48f758ac3ce28')

  print(dict(row))


def testAutocloseableConnection():
  ds = Sqlite3Datasource("assets/data.db")

  with ds.getConnection() as conn:
    rows = conn.execute("select * from service_usage").fetchall()
    print([dict(row) for row in rows])


class User():
  def __init__(self,name,age) -> None:
    self.name = name
    self.age = age

  def __str__(self) -> str:
    return f'name: {self.name}, age: {self.age}'

def testObject():
  user = User('zhangsan',18)
  user.phone = '138001380000'

  print(user.phone)

def testDict():
  data = {"a": 1, "b": 2}
  data2 = data.copy()
  data2['a'] = 3

  print(data)
  print(data2)

# testDict()
# testObject()

import threading,time

def testRatelimiter():
  def testBucket():
    limiter = TokenBucket(2,1)
    while True:
      token = limiter.acquire()
      if token:
        print('acquire a token from the bucket')
      else:
        print('the bucket is empty now,waiting')
      time.sleep(0.4)

  thread = threading.Thread(target=testBucket)
  thread.start()

from src.utils.text import splitByMark
def testSplit():
  text = "The docker build command uses the Dockerfile to build a new container image hsldfhkajlsdfhakljshdfjkashdflkjashdfklhasdfasjdfhlajsdhfklahsdjfkahsdfkljhasdjfhasdfasdfasdfasdfasdfasdfasdf. You might have noticed that Docker downloaded a lot of “layers” hsldfhkajlsdfhakljshdfjkashdflkjashdfklhasdfasjdfhlajsdhfklahsdjfkahsdfkljhasdjfhasdfasdfasdfasdfasdfasdfasdf. This is because you instructed the builder that you wanted to start from the node:18-alpine image. But, since you didn’t have that on your machine, Docker needed to download the image."
  mark = {'!',"\uff01",".","。","?","\uff1f"}
  mark2 = {'\n'}
  res = splitByMark(text,len(text),100,mark)
  # for item in res:
  #   print(item.strip())
  print(len(res))
  print(res)


def testDeeplX():
  res = deeplx.translate('hey, i need some translators','en','zh')
  print(res)

# testDeeplX()
# testSplit()

# trans = Google(name="hello",appId="world")
# print(trans)
# import os,logging.config
# if not os.path.exists('logs'):
#   os.mkdir('logs')

# logging.config.fileConfig('logging.conf')
# logger = logging.getLogger('translate')


# arr = [1,2,3]
# my_dict = {
#   'id': 123,
#   'name': 'bigcat'
# }

# testEngineRatelimiter()

# testRatelimiter()

def testMD5():
  import hashlib

  # 定义一个字符串
  string = "123456"

  # 计算字符串的 MD5 摘要
  md5_hash = hashlib.md5()
  md5_hash.update(string.encode('utf-8'))
  digest = md5_hash.hexdigest()

  print(digest)  # 输出 MD5 摘要

# testMD5()

from queue import Queue
def testQueue():
  q = Queue()
  
  def schedule():
    counter = 0
    while True:
      q.put(f'counter: {counter}')
      counter += 1
      time.sleep(10)

  t = threading.Thread(target=schedule)
  t.start()

  while True:
    print(q.get())

def testDict():
  d = {
    'a':1,
    'b':2,
    'c':3
  }
  e = {
    'd':4,
    'e':5
  }
  d.update(e)
  print(d)


def testBingx():
  from src.translator.bingx import BingX
  bingx = BingX('bing1',proxy='http://127.0.0.1:7890')
  data = bingx.translate('hello,world','en','zh-hant')
  print(data)

  data = bingx.translate('hello,python','en','zh-hans')
  print(data)

testBingx()