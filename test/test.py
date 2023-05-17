from translator.caiyun import Caiyun
from translator.tencent import Tencent
from translator.baidu import Baidu
from translator.deeplx import DeepLX
from translator.google import Google

from mode.loadbalancer import LoadBalancer
from src.translate_engine import TranslateEngine

from translator.exception import TranslactionException,ExceptionType

import logging

# result = caiyun.translate('有时候我也想去旅游', 'auto', 'en
# result = baidu.translate('你好', 'zh', 'en')
# print(result)

google = Google('google1',7,3)
# result = google.translate('Gives administrators the ability to assign different weights to each server', 'en', 'zh')
# print(result)

deeplx = DeepLX('deeplx1')
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

from utils.ratelimiter.token_bucket import TokenBucket
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

from utils.text import splitByMark
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
import os,logging.config
if not os.path.exists('logs'):
  os.mkdir('logs')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('translate')


arr = [1,2,3]
my_dict = {
  'id': 123,
  'name': 'bigcat'
}
def testLogger():
  logger.info("hello %s world %s, len=%s, dict=%s",'test','hh',len(arr),my_dict)

testLogger()
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

testDict()