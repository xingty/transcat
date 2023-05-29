from flask import (Blueprint, request)
import src.web.translate_service as service

bp = Blueprint('translate', __name__, url_prefix='/api')

@bp.route('/translate/deeplx/adapter',methods=['POST'])
def deeplxAdapter():
  showEngine = request.args.get('show_engine') or None
  useCache = not (request.args.get('disable_cache') == '1')
  data = service.translate(request.json,showEngine,useCache)

  return {
    "code": 200,
    "id": 123321,
    "data": data['target_text'],
    "alternatives": []
  }

@bp.route('/translate/<engine>',methods=['POST'])
def translate(engine):
  useCache = not (request.args.get('disable_cache') == '1')
  data = service.translateByService(engine,request.json,useCache)

  return data


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
