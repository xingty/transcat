from random import choice
from src.web.exception.error import ServiceException,ErrorCode
from src.utils import assertx,hash
from src.mode import MODE_DICT
from src.context import initChooser,translatorGroup,configuration,translators
from .translate_history import history
from src.context import translateEngine as engine
from src.translator import usageInfo as usage


def translate(params,showEngine,useCache=False) -> dict:
  assertx.isTrue('source_lang' in params,'Missing parameter: [ source_lang ]')
  assertx.isTrue('target_lang' in params,'Missing parameter: [ target_lang ]')
  text = params['text']
  assertx.notEmpty(text,'[ text ] must not be empty')

  try:
    showEngine = int(showEngine)
  except Exception:
    showEngine = 0

  src = params['source_lang'].lower()
  dst = params['target_lang'].lower()

  try:
    data = None
    if useCache:
      data = _getFromCache(text,dst)

    if not data:
      data = engine.translate(text,src,dst)
      history.push(data.copy())

    content = data['target_text']
    if showEngine != 0:
      data['target_text'] = f'{content} - (by {data["engine"]})'
    return data
  except Exception as e:
    raise ServiceException(ErrorCode.FAILED,'server internal error')

def _getFromCache(text,dst):
  hashId = hash.md5(text + '_' + dst)
  return history.getByHashId(hashId)

def translateByService(serviceName,params,useCache=False) -> dict:
  assertx.isTrue('source_lang' in params,'Missing parameter: [ source_lang ]')
  assertx.isTrue('target_lang' in params,'Missing parameter: [ target_lang ]')
  text = params['text']
  assertx.notEmpty(text,'[ text ] must not be empty')

  src = params['source_lang'].lower()
  dst = params['target_lang'].lower()

  data = None
  if useCache:
    data = _getFromCache(text,dst)
  
  if data is not None:
    return data

  translators = translatorGroup[serviceName.lower()]
  if translators is None or len(translators) < 1:
    raise ServiceException(ErrorCode.SERVICE_NOT_FOUND,'service not found')

  translator = choice(translators)
  data = translator.translate(text,src,dst)
  if data is not None:
    cache = data.copy()
    cache.update({
      'sid': translator.name,
      'src': src,
      'dst': dst,
      'source_text': text,
      'engine': translator.type
    })
    history.push(cache)

  usage.updateUsageInfo(translator.name,translator.type,len(text))

  return {
    'src': src,
    'dst': dst,
    'target_text': data['target_text'],
    'engine': serviceName
  }


def switchMode(mode,rule): 
  if mode not in MODE_DICT:
    raise ServiceException(ErrorCode.FAILED,f'Invalid mode [ {mode} ], available modes: {MODE_DICT.keys()}')
  
  if (mode == engine.getMode()):
    return
  
  chooser = initChooser(translators,mode,rule)
  engine.switchMode(chooser,mode)
  configuration.mode = mode
  configuration.loadbalanceRule = rule
  

def selectServer(index):
  return engine.selectServer(index)
