from src.context import configuration
from src.translator import usageInfo

def _mapServices(item: dict):
  translator = item.copy()
  if 'app_key' in translator:
    translator['app_key'] = ("*" * 16)

  return translator

_services = [ _mapServices(item) for item in configuration.services ]

def getServerState() -> dict:
  config = configuration.__dict__
  for s in _services:
    info = usageInfo.getUsageInfo(s['name'],s['type'])
    s['usage'] = info.usage
  
  config['services'] = _services

  return config

