from src.mode import MODE_DICT
from src.mode.rules import RULES
from src.translator import TRANSLATORS
from src.utils.ratelimiter import RATELIMITERS
from src.translate_engine import TranslateEngine
from flask import Flask
from src.utils import hash
from src.utils.ds import Sqlite3Datasource
import src.storage.ds_sqlite3 as storage
import logging,logging.config,os,time

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
  month = time.strftime('%Y-%m')
  for item in config["services"]:
    serviceType = item['type'].lower()
    klass = TRANSLATORS.get(serviceType)
    if not klass:
      raise Exception(f'Available services type are [ {TRANSLATORS.keys() }]')
    
    service = klass(
      name=item['name'],
      appId=item.get('app_id') or None,
      appKey=item.get('app_key') or None,
      limit=item.get('limit') or None,
      weight=item.get('weight') or None,
      proxy=item.get('proxy') or None
    )

    serviceId = hash.md5(service.name + '_' + service.type + '_' + month)
    if serviceMap.get(serviceId):
      raise Exception(f'duplicate key {service.name}')
    serviceMap[serviceId] = service

    if serviceType == "tencent":
      region = item.get('region')
      if region:
        service.region = region

    rate = item.get('rate')
    if rate:
      limiter = RATELIMITERS.get(rate.type)
      if not limiter:
        raise Exception(f'Available rate limiter type are [ {RATELIMITERS.keys() }]')
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
      service = serviceMap.get(row['service_id']) or None
      if service:
        service.usage = row['usage']

def initChooser(translators,mode,rule):
  klass = MODE_DICT.get(mode)
  if not klass:
    raise Exception(f'Available rate limiter type are [ {MODE_DICT.keys() }]')

  chooser = None
  if mode == 'select':
    chooser = klass(translators)
  elif mode == 'load-balance':
    if not rule:
      raise Exception(f'Missing key [ load-balance-rule ]')
    
    rule_klass = RULES.get(rule) or None
    if not rule_klass:
      raise Exception(f'Available rule type are [ {RULES.keys() }]')
    
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