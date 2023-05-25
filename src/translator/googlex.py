from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
import requests
from src.utils import http

LANGUAGE = {
  "auto": ["any"],
  "zh": ["any"],
  "zh-hans": ["any"],
  "zh-hant": ["any"],
  "en": ["any"],
  "ja": ["any"],
  "ko": ["any"],
  "fr": ["any"],
  "es": ["any"],
  "it": ["any"],
  "de": ["any"],
  "tr": ["any"],
  "ru": ["any"],
  "pt": ["any"],
  "vi": ["any"],
  "id": ["any"],
  "th": ["any"],
  "ms": ["any"],
  "ar": ["any"],
  "hi": ["any"]
}

class GoogleX(BaseTranslator):
  def __init__(self,name,appKey=None,appId=None,limit=-1,weight=1,proxy=False):
    super().__init__(name,appId,appKey,limit,weight,proxy)
    self.type = "googlex"
    # sl: source language
    # tl: target language
    # q: query word / text
    # client: 客户端类型
    # dt=t: 仅回复翻译结果
    self.apiUrl = "https://translate.google.com/translate_a/single?client=it&dt=qca&dt=t&dt=rmt&dt=bd&dt=rms&dt=sos&dt=md&dt=gt&dt=ld&dt=ss&dt=ex&otf=2&dj=1&hl=en&ie=UTF-8&oe=UTF-8"
    self.headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "User-Agent": "GoogleTranslate/6.29.59279 (iPhone; iOS 15.4; en; iPhone14,2)",
    }
    self.mapping = {
      "zh-hans": "zh-CN",
      "zh-hant": "zh-TW",
    }
  
  def doTranslate(self,text,src,dst) -> dict:
    _src = src
    _dst = dst
    if src in self.mapping:
      _src = self.mapping[src]

    if dst in self.mapping:
      _dst = self.mapping[dst]

    url = f'{self.apiUrl}&sl={_src}&tl={_dst}'
    try:
      data=f"q={requests.utils.quote(text)}"
      res = http.post(url,data,self.headers,self.proxy)

      trans = "".join(
        [sentence.get("trans", "") for sentence in res.json()["sentences"]],
      )

      return {
        "target_text": trans
      }
    except http.NetworkException as e:
      raise TranslactionException(self.type,ExceptionType.NETWORK,None)

  def maxCharacterAtOnce(self):
    return 3000

  def supportedLanguage(self) -> dict:
    return LANGUAGE