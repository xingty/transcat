from src.mode import MODE_DICT
from src.mode.rules import RULES
from src.translator import TRANSLATORS
from src.utils.ratelimiter import RATELIMITERS
from src.translate_engine import TranslateEngine
from flask import Flask
from src.utils.text import buildServiceId
from src.utils.ds import Sqlite3Datasource
from src.translator import usageInfo as usage
import src.storage.ds_sqlite3 as storage
import logging,logging.config,os,sys

APP_NAME = "transcat"

applicationContext: Flask = None
translateEngine: TranslateEngine = None
translators = None
datasource: Sqlite3Datasource = None

def initLogger():
  if not os.path.exists('logs'):
    os.mkdir('logs')
  
  logging.config.fileConfig('assets/logging.conf')

def initDB():
  global datasource
  datasource = Sqlite3Datasource("assets/data.db")
  datasource.init("assets/schema.sql")

def initTranslators(config):
  global translators
  services = []
  serviceMap = {}
  for item in config["services"]:
    serviceType = item['type'].lower()
    klass = TRANSLATORS.get(serviceType)
    if not klass:
      print(f'Available rate translate type are [ {TRANSLATORS.keys() }]')
      sys.exit(0)
    
    service = klass(
      name=item['name'],
      appId=item.get('app_id') or None,
      appKey=item.get('app_key') or None,
      limit=item.get('limit') or None,
      weight=item.get('weight') or None,
      proxy=item.get('proxy') or None
    )

    serviceId = buildServiceId(service.name,service.type)
    if serviceMap.get(serviceId):
      print(f'duplicate key {service.name}')
      sys.exit(0)
    serviceMap[serviceId] = service

    if serviceType == "tencent":
      region = item.get('region')
      if region:
        service.region = region

    rate = item.get('rate')
    if rate:
      limiter = RATELIMITERS.get(rate.type)
      if not limiter:
        print(f'Available rate limiter type are [ {RATELIMITERS.keys() }]')
        sys.exit(0)
      service.rateLimiter = limiter(rate.capacity,rate.window)

    services.append(service)
  
  translators = services
  initServiceUsage(serviceMap)
  return translators


def initServiceUsage(serviceMap):
  serviceIds = list(serviceMap.keys())
  with datasource.getConnection() as conn:
    rows = storage.findUsageByServiceIds(conn,serviceIds)
    for item in rows:
      row = dict(item)
      sid = row['service_id']
      info = usage.getUsageInfoBySid(sid)
      info.updateUsage(row['usage'])

def initChooser(translators,mode,rule):
  klass = MODE_DICT.get(mode)
  if not klass:
    print(f'unknown mode: {mode}')
    sys.exit(0)

  chooser = None
  if mode == 'select':
    chooser = klass(translators)
  elif mode == 'load-balance':
    if not rule:
      print(f'Missing key [ load-balance-rule ]')
      sys.exit(0)
    
    rule_klass = RULES.get(rule) or None
    if not rule_klass:
      print(f'Available rule type are [ {RULES.keys() }]')
      sys.exit(0)
    
    chooser = klass(translators,rule_klass())

  return chooser

def initTranslateEngine(config,translators):
  mode = config['mode']
  rule = config.get('load-balance-rule') or None
  chooser = initChooser(translators,mode,rule)

  global translateEngine  
  translateEngine = TranslateEngine(chooser,mode)
  return translateEngine

def createAppContext(config):
  global applicationContext
  applicationContext = Flask(APP_NAME)
  return applicationContext

def initApplicationContext(config):
  initDB()
  initLogger()
  translators = initTranslators(config)
  initTranslateEngine(config,translators)
  app = createAppContext(config)

  return app