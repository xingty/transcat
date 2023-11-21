from src.mode import MODE_DICT
from src.mode.rules import RULES
from src.translator import TRANSLATORS
from src.utils.ratelimiter import RATELIMITERS
from src.translate_engine import TranslateEngine
from flask import Flask
from src.utils.text import buildServiceId
from src.utils.ds import Sqlite3Datasource
from src.translator import usageInfo as usage
from src.configuration import Configuration
from collections import defaultdict
from logging.handlers import RotatingFileHandler
import src.storage.ds_sqlite3 as storage
import logging.config,os,sys

APP_NAME = "transcat"
TRANSCAT_ASSETS_DIR = "TRANSCAT_ASSETS"

applicationContext: Flask = None
translateEngine: TranslateEngine = None
translators = None
translatorGroup = None
datasource: Sqlite3Datasource = None
configuration: Configuration = None

def initLogger(location: str):
  file = location + '/transcat.log'
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s")
  handler = RotatingFileHandler(file, maxBytes=10485760, backupCount=5)
  handler.setFormatter(formatter)
  logger.addHandler(handler)

def initDB(location):
  global datasource
  datasource = Sqlite3Datasource(location + "/data.db")
  datasource.init("assets/schema.sql")

def initTranslators(config: Configuration):
  global translators
  global translatorGroup
  services = []
  serviceMap = {}
  for item in config.services:
    serviceType = item['type'].lower()
    klass = TRANSLATORS.get(serviceType)
    if not klass:
      print(f'Available rate translate type are [ {TRANSLATORS.keys() }]')
      sys.exit(0)
    
    service = klass(
      name=item['name'],
      appId=item.get('app_id') or None,
      appKey=item.get('app_key') or None,
      region=item.get('region') or None,
      limit=item.get('limit') or None,
      weight=item.get('weight') or None,
      proxy=item.get('proxy') or None
    )

    serviceId = buildServiceId(service.name,service.type)
    if serviceMap.get(serviceId):
      print(f'duplicate key {service.name}')
      sys.exit(0)
    serviceMap[serviceId] = service

    if item.get('mode'):
      service.mode = item['mode']

    if serviceType == "tencent":
      region = item.get('region')
      if region:
        service.region = region

    if serviceType == "openai":
      model = item.get('model') or 'gpt-3.5-turbo'
      assert model == 'gpt-3.5-turbo' or model == 'gpt4'
      service.model = model

    rate = item.get('rate')
    if rate:
      limiter = RATELIMITERS.get(rate.type)
      if not limiter:
        print(f'Available rate limiter type are [ {RATELIMITERS.keys() }]')
        sys.exit(0)
      service.rateLimiter = limiter(rate.capacity,rate.window)

    services.append(service)
  
  translators = services
  translatorGroup = defaultdict(list)
  for t in translators:
    translatorGroup[t.type].append(t)

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

def initTranslateEngine(config: Configuration,translators: list):
  mode = config.mode
  rule = config.loadbalanceRule
  chooser = initChooser(translators,mode,rule)

  global translateEngine  
  translateEngine = TranslateEngine(chooser,mode)
  return translateEngine

def createAppContext(config: Configuration):
  global applicationContext
  applicationContext = Flask(APP_NAME)

  from src.web import auth

  return applicationContext

def initAssetsDir(path: str):
  path = path if path else 'transcat'
  if not os.path.exists(path):
    os.makedirs(path, exist_ok=True)

  return path

def initConfiguration(config: dict):
  global configuration
  configuration = Configuration(config)

  return configuration

def initApplicationContext(config: Configuration):
  path = initAssetsDir(config.assetsDir)
  initDB(path)
  initLogger(path)
  translators = initTranslators(config)
  initTranslateEngine(config,translators)
  app = createAppContext(config)

  return app