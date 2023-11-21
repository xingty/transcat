import hashlib, hmac, json, time
from datetime import datetime
from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
from src.utils import http

LANGUAGE = {
  "auto": ["any"],
  "zh": ["en", "ja", "ko", "fr", "es", "it", "de", "tr", "ru", "pt", "vi", "id", "th", "ms"],
  "zh-hans": ["en", "ja", "ko", "fr", "es", "it", "de", "tr", "ru", "pt", "vi", "id", "th", "ms"],
  "zh-hant": ["en", "ja", "ko", "fr", "es", "it", "de", "tr", "ru", "pt", "vi", "id", "th", "ms"],
  "en": ["zh", "zh-hant","ja", "ko", "fr", "es", "it", "de", "tr", "ru", "pt", "vi", "id", "th", "ms", "ar", "hi"],
  "ja": ["zh", "zh-hant","en", "ko"],
  "ko": ["zh", "zh-hant","en", "ja"],
  "fr": ["zh", "zh-hant","en", "es", "it", "de", "tr", "ru", "pt"],
  "es": ["zh", "zh-hant","en", "fr", "it", "de", "tr", "ru", "pt"],
  "it": ["zh", "zh-hant","en", "fr", "es", "de", "tr", "ru", "pt"],
  "de": ["zh", "zh-hant","en", "fr", "es", "it", "tr", "ru", "pt"],
  "tr": ["zh", "zh-hant","en", "fr", "es", "it", "de", "ru", "pt"],
  "ru": ["zh", "zh-hant","en", "fr", "es", "it", "de", "tr", "pt"],
  "pt": ["zh", "zh-hant","en", "fr", "es", "it", "de", "tr", "ru"],
  "vi": ["zh", "zh-hant","en"],
  "id": ["zh", "zh-hant","en"],
  "th": ["zh", "zh-hant","en"],
  "ms": ["zh", "zh-hant","en"],
  "ar": ["en"],
  "hi": ["en"]
}

class Tencent(BaseTranslator):
  def __init__(self, name,appKey,appId,limit=-1, weight=1, proxy=False):
    super().__init__(name, appKey,appId,limit, weight, proxy)
    assert appId is not None and len(appId) > 0
    assert appKey is not None and len(appKey) > 0
    self.region = 'ap-guangzhou'
    self.type = 'tencent'
    self.apiUrl = 'https://tmt.tencentcloudapi.com'

  def doTranslate(self, text, src, dst) -> dict:
    _src = src
    _dst = dst
    if 'zh-' in src:
      _src = 'zh' if src == 'zh-hans' else 'zh-TW'

    if 'zh-' in dst:
      _dst = 'zh' if dst == 'zh-hans' else 'zh-TW'

    payload = {
      "SourceText": text,
      "Source": _src,
      "Target": _dst,
      "ProjectId": 0
    }

    timestamp = int(time.time())
    authorization = self.getAuthorization(timestamp,payload)
    headers = {
      'Authorization': authorization,
      'Content-Type': 'application/json; charset=utf-8',
      'Host': 'tmt.tencentcloudapi.com',
      'X-TC-Action': 'TextTranslate',
      'X-TC-Timestamp': str(timestamp),
      'X-TC-Version': '2018-03-21',
      'X-TC-Region': self.region,
    }

    try:
      response = http.post(
        url=self.apiUrl,
        headers=headers,
        data=json.dumps(payload),
        proxy=self.proxy
      )

      data = response.json()
      if 'Response' in data and 'Error' in data['Response']:
        err = data['Response']['Error']
        eType = ExceptionType.REQUEST_LIMIT if err['Code'] == 'RequestLimitExceeded' else ExceptionType.UNKNOWN
        raise TranslactionException(self.type,eType,data)
      
      return {
        "target_text": data['Response']['TargetText']
      }
      
    except http.NetworkException as e:
      raise TranslactionException(self.type,ExceptionType.NETWORK,e.message)

  def getAuthorization(self,timestamp,params) -> str:
    signed_headers = "content-type;host"
    service = "tmt"
    host = "tmt.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    def getCanonicalRequest() -> str:
      http_request_method = "POST"
      canonical_uri = "/"
      canonical_querystring = ""
      ct = "application/json; charset=utf-8"
      payload = json.dumps(params)
      canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
      hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
      return (http_request_method + "\n" +
                     canonical_uri + "\n" +
                     canonical_querystring + "\n" +
                     canonical_headers + "\n" +
                     signed_headers + "\n" +
                     hashed_request_payload)

    canonicalRequeset = getCanonicalRequest()
    
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonicalRequeset.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                  str(timestamp) + "\n" +
                  credential_scope + "\n" +
                  hashed_canonical_request)

    def sign(key, msg):
      return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + self.appKey).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    return (algorithm + " " +
                 "Credential=" + self.appId + "/" + credential_scope + ", " +
                 "SignedHeaders=" + signed_headers + ", " +
                 "Signature=" + signature)
  
  def maxCharacterAtOnce(self):
    # https://cloud.tencent.com/document/product/551/32572
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE