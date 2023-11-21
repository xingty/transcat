from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
from src.utils import http
import json

LANGUAGE = {
  "en": ["zh-hans","zh","zh-hant"],
  "zh-hans": ["en","ja"],
  "zh": ["en","ja"],
  "zh-hant": ["en","ja"],
  "ja": ["zh-hans","zh","zh-hant"]
}

class Caiyun(BaseTranslator):
  def __init__(self,name,appKey,appId=None, limit=-1,weight=1,proxy=False):
    super().__init__(name,appKey,appId,limit,weight,proxy)
    assert appKey is not None and len(appKey) > 0
    self.type = "caiyun"
    self.apiUrl = 'http://api.interpreter.caiyunai.com/v1/translator'
    self.headers = {
      'content-type': "application/json",
      'x-authorization': "token " + appKey,
    }
  
  def doTranslate(self,text,src,dst) -> dict:
    transType = src + '2' + dst
    if 'zh' in src:
      transType = "zh2" + dst

    if 'zh' in dst:
      transType = src + '2zh'
    
    paragraphs = text.split('\n')
    payload = {
      "source" : paragraphs, 
      "trans_type" : transType,
      "request_id" : "demo",
    }

    try:
      response = http.post(
        url=self.apiUrl, 
        data=json.dumps(payload), 
        headers=self.headers,
        proxy=self.proxy
      )

      data = response.json()
      if 'target' not in data:
        data['trans_type'] = f'src -> {src}, dst -> {dst}, trans_type -> {transType}'
        raise TranslactionException(self.type,ExceptionType.UNKNOWN,data)

      return {
        "target_text": "\n".join(data['target']),
      }
    except http.NetworkException as e:
      raise TranslactionException(self.type,ExceptionType.NETWORK,e.message)


  def maxCharacterAtOnce(self):
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE
  
