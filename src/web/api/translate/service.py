from src.web.exception.error import ServiceException,ErrorCode
from src.utils import assertx,hash
from src.mode import MODE_DICT
from src.context import initChooser,translators
from src.web.api.translate.repo import TranslateHistory

history = TranslateHistory() 

class TranslateService():
  def __init__(self,engine) -> None:
    self.engine = engine

  def translate(self,params,showEngine,useCache=False) -> dict:
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
      if useCache:
        data = self._getFromCache(text,dst)
        if data:
          return data

      data = self.engine.translate(text,src,dst)
      history.push(data)
      content = data['target_text']
      if showEngine != 0:
        data['target_text'] = f'{content} - (by {data["engine"]})'
      return data
    except Exception as e:
      raise ServiceException(ErrorCode.FAILED,e.data)

  def _getFromCache(self,text,dst):
    hashId = hash.md5(text + '_' + dst)
    record = history.getByHashId(hashId)
    if not record:
      return None

    return {
      'src': record['src'],
      'dst': record['dst'],
      'target_text': record['target_text'],
      'engine': record['engine'],
    }

  def switchMode(self,mode,rule): 
    if mode not in MODE_DICT:
      raise ServiceException(ErrorCode.FAILED,f'Invalid mode [ {mode} ], available modes: {MODE_DICT.keys()}')
    
    if (mode == self.engine.getMode()):
      return
    
    chooser = initChooser(translators,mode,rule)
    self.engine.switchMode(chooser,mode)

  def selectServer(self,index):
    return self.engine.selectServer(index)