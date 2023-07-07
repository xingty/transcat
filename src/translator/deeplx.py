from .base_translator import BaseTranslator
import random,time,json,requests
from src.translator.exception import TranslactionException,ExceptionType

class DeepLX(BaseTranslator):
  def __init__(self, name,appKey=None,appId=None,limit=-1, weight=1, proxy=False):
    super().__init__(name, appKey,appId,limit,weight,proxy)
    self.apiUrl = 'https://www2.deepl.com/jsonrpc'
    self.type = 'deeplx'
    self.headers = {
      "Content-Type": "application/json; charset=utf-8",
      "Accept-Language": "en-US,en;q=0.9",
      "Accept-Encoding": "gzip",
      "Connection": "keep-alive",
      "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

  def doTranslate(self, text, src, dst):
    iCount = self.getICount(text)
    id = self.getRandomNumber()
    timestamp = self.getTimestamp(iCount)
    
    _src = src
    _dst = dst
    if "zh-" in src:
      _src = 'zh'

    if "zh-" in dst:
      _dst = 'zh'

    body = {
      "jsonrpc": "2.0",
      "method":"LMT_handle_texts",
      "params": {
        "splitting": "newlines",
        "lang": {
            "source_lang_user_selected": _src,
            "target_lang": _dst,
        },
        "texts": [{
          "text": text,
          "requestAlternatives": 3
        }],
        "timestamp": timestamp,
      },
      "id": id,
    }
    payload = json.dumps(body, ensure_ascii=False,separators=(',', ':'))
    if (id+5) % 29 == 0 or (id+3) % 13 == 0:
      payload = payload.replace("\"method\":\"", "\"method\" : \"", -1)
    else:
      payload = payload.replace("\"method\":\"", "\"method\": \"", -1)

    payload = payload.encode('utf-8')
    response = requests.post(self.apiUrl,data=payload,headers=self.headers)
    if not response.ok:
      data = {
        'code': response.status_code,
        'text': response.text
      }
      raise TranslactionException(self.type,ExceptionType.UNKNOWN,data)

    data = json.loads(response.text)
    targetText = data["result"]["texts"][0]["text"]

    return {
      "target_text": targetText,
      "alternatives": data["result"]["texts"][0].get("alternatives")
    }
  
  def getRandomNumber(self) -> int:
    random.seed(time.time())
    num = random.randint(100000, 109999)
    return num * 1000
  
  def getTimestamp(self,iCount: int) -> int:
    ts = int(time.time() * 1000)
    if iCount != 0:
      iCount += 1
      return ts - ts % iCount + iCount

    return ts
  
  def getICount(self,text) -> int:
    return text.count('i')
  
  def supportedLanguage(self) -> dict:
    return {
      "auto": ["any"],
      "zh": ["any"],
      "zh-hans": ["any"],
      "zh-hant": ["any"],
      "bg": ["any"],
      "cs": ["any"],
      "da": ["any"],
      "de": ["any"],
      "el": ["any"],
      "en": ["any"],
      "es": ["any"],
      "et": ["any"],
      "fi": ["any"],
      "fr": ["any"],
      "hu": ["any"],
      "id": ["any"],
      "it": ["any"],
      "ja": ["any"],
      "ko": ["any"],
      "lt": ["any"],
      "lv": ["any"],
      "nb": ["any"],
      "nl": ["any"],
      "pl": ["any"],
      "pt": ["any"],
      "ro": ["any"],
      "ru": ["any"],
      "sk": ["any"],
      "sl": ["any"],
      "sv": ["any"],
      "tr": ["any"],
      "uk": ["any"],
      "zh": ["any"]
    }