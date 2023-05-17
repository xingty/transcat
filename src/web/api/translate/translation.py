from flask import (Blueprint, request)
from src.context import translateEngine
from src.web.api.translate.service import TranslateService

bp = Blueprint('translate', __name__, url_prefix='/api')
service = TranslateService(translateEngine)

@bp.route('/translate/deeplx/adapter',methods=['POST'])
def deeplxAdapter():
  showEngine = request.args.get('show_engine') or None
  useCache = not (request.args.get('disable_cache') == '1')
  print(useCache)
  data = service.translate(request.json,showEngine,useCache)

  return {
    "code": 200,
    "id": 123321,
    "data": data['target_text'],
    "alternatives": []
  }

@bp.route('/translate/mode/switch',methods=['PUT'])
def switchMode():
  mode = request.form.get('mode')
  rule = request.form.get('rule')

  service.switchMode(mode,rule)
  return { "message": 'successful' }

@bp.route('/translate/select',methods=['PUT'])
def selectServer():
  index = request.form.get('index') or 0
  service.selectServer(int(index))

  return { "message": 'successful' }
