from flask import (Blueprint, request)
from src.context import configuration
from src.translator import usageInfo

bp = Blueprint('server', __name__, url_prefix='/api')

def mapServices(item: dict):
  translator = item.copy()
  if 'app_key' in translator:
    translator['app_key'] = ("*" * 16)

  return translator

services = [ mapServices(item) for item in configuration.services ]

@bp.route('/server/status',methods=['GET'])
def serverState():
  config = configuration.__dict__
  for s in services:
    info = usageInfo.getUsageInfo(s['name'],s['type'])
    s['usage'] = info.usage
  
  config['services'] = services

  return config
