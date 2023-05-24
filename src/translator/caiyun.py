from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
import requests,json

LANGUAGE = {
  "en": ["zh-hans","zh","zh-hant"],
  "zh-hans": ["en","ja"],
  "zh": ["en","ja"],
  "zh-hant": ["en","ja"],
  "ja": ["zh-hans","zh","zh-hant"]
}

class Caiyun(BaseTranslator):
  def __init__(self,name,appKey,appId=None,limit=-1,weight=1,proxy=False):
    super().__init__(name,appKey,appId,limit,weight,proxy)
    assert appKey is not None and len(appKey) > 0
    self.type = "caiyun"
    self.apiUrl = 'http://api.interpreter.caiyunai.com/v1/translator'
    self._headers = {
      'content-type': "application/json",
      'x-authorization': "token " + appKey,
    }
  
  def doTranslate(self,text,src,dst) -> dict:
    transType = src + '2' + dst
    if 'zh' in src:
      transType = "zh2" + dst

    if 'zh' in dst:
      transType = src + '2zh'
    
    payload = {
      "source" : [text], 
      "trans_type" : transType,
      "request_id" : "demo",
    }
    response = requests.request(
      "POST", 
      self.apiUrl, 
      data=json.dumps(payload), 
      headers=self._headers
    )

    if not response.ok:
      data = {
        'code': response.status_code,
        'text': response.text,
        'trans_type': f'src -> {src}, dst -> {dst}, trans_type -> {transType}, text -> {text}'
      }
      raise TranslactionException(self.type,ExceptionType.NETWORK,data)

    data = json.loads(response.text)
    if 'target' not in data:
      data['trans_type'] = f'src -> {src}, dst -> {dst}, trans_type -> {transType}'
      raise TranslactionException(self.type,ExceptionType.UNKNOWN,data)

    return {
      "target_text": data['target'][0],
    }

  def maxCharacterAtOnce(self):
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE
  
