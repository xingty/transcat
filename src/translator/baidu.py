import hashlib, json, time,requests
from src.translator.exception import TranslactionException,ExceptionType
from .base_translator import BaseTranslator

LANGUAGE = {
  "en": ["zh", "ja", "ko", "fr", "es", "it", "de", "ru", "pt", "vi", "ar"],
  "zh": ["en","ja","ko"],
  "zh-hans": ["en","ja","ko"],
  "zh-hant": ["en","ja","ko"],
  "ja": ["zh", "zh-hant","en", "ko"],
  "ko": ["zh", "zh-hant","en", "ja"],
  "fr": ["zh", "zh-hant","en", "es", "it", "de", "ru", "pt"],
  "es": ["zh", "zh-hant","en", "fr", "it", "de", "ru", "pt"],
  "it": ["zh", "zh-hant","en", "fr", "es", "de", "ru", "pt"],
  "de": ["zh", "zh-hant","en", "fr", "es", "it", "ru", "pt"]
}

class Baidu(BaseTranslator):
  def __init__(self, name,appKey,appId=None,limit=-1, weight=1, proxy=False):
    super().__init__(name,appKey,appId,limit, weight, proxy)
    assert appId is not None and len(appId) > 0
    assert appKey is not None and len(appKey) > 0
    self.type = 'baidu'
    self.apiUrl = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    self.mapping = {
      "ja": "jp",
      "ko": "kor",
      "fr": "fra",
      "es": "spa",
      "vi": "vie",
      "ar": "ara",
      "zh-hant": "cht",
      "zh-hans": "zh",
    }
  
  def doTranslate(self, text, src, dst) -> dict:
    _src = src
    _dst = dst
    if self.mapping.get(src):
      _src = self.mapping.get(src)

    if self.mapping.get(dst):
      _dst = self.mapping.get(dst)

    salt = str(round(time.time() * 1000))
    raw = self.appid + text + salt + self.appKey
    sign = hashlib.md5(raw.encode('utf8')).hexdigest()
    params = {
        'q': text,
        'from': _src,
        'to': _dst,
        'appid': self.appId,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(self.apiUrl, params=params)
    if not response.ok:
      data = { 'code': response.status_code,'text': response.text }
      raise TranslactionException(self.type,ExceptionType.NETWORK,data)

    data = json.loads(response.text)
    if 'error_code' in data:
      etype = ExceptionType.REQUEST_LIMIT if '54003' == data['error_code'] else ExceptionType.UNKNOWN
      raise TranslactionException(self.type,etype,data)

    return {
      "target_text": data['trans_result'][0]['dst']
    }
  
  def maxCharacterAtOnce(self):
    # http://api.fanyi.baidu.com/doc/21
    # 2000是一个比较保险的值
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE