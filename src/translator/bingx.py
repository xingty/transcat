from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
from src.utils.thread_safe_counter import ThreadSafeCounter
import requests,time,re,threading

LANGUAGE = {
  "auto": ["any"],
  "zh": ["any"],
  "zh-hans": ["any"],
  "zh-hant": ["any"],
  "af": ["any"],
	"sq": ["any"],
	"am": ["any"],
	"ar": ["any"],
	"hy": ["any"],
	"as": ["any"],
	"az": ["any"],
	"bn": ["any"],
	"ba": ["any"],
	"eu": ["any"],
	"bs": ["any"],
	"bg": ["any"],
	"yue": ["any"],
	"ca": ["any"],
	"lzh": ["any"],
	"hr": ["any"],
	"cs": ["any"],
	"da": ["any"],
	"prs": ["any"],
	"dv": ["any"],
	"nl": ["any"],
	"en": ["any"],
	"et": ["any"],
	"fo": ["any"],
	"fj": ["any"],
	"fil": ["any"],
	"fi": ["any"],
	"fr": ["any"],
	"gl": ["any"],
	"lug": ["any"],
	"ka": ["any"],
	"de": ["any"],
	"el": ["any"],
	"gu": ["any"],
	"ht": ["any"],
	"ha": ["any"],
	"he": ["any"],
	"hi": ["any"],
	"mww": ["any"],
	"hu": ["any"],
	"is": ["any"],
	"ig": ["any"],
	"id": ["any"],
	"ikt": ["any"],
	"iu": ["any"],
	"ga": ["any"],
	"it": ["any"],
	"ja": ["any"],
	"kn": ["any"],
	"kk": ["any"],
	"km": ["any"],
	"rw": ["any"],
	"gom": ["any"],
	"ko": ["any"],
	"ku": ["any"],
	"kmr": ["any"],
	"ky": ["any"],
	"lo": ["any"],
	"lv": ["any"],
	"ln": ["any"],
	"lt": ["any"],
	"dsb": ["any"],
	"mk": ["any"],
	"mai": ["any"],
	"mg": ["any"],
	"ms": ["any"],
	"ml": ["any"],
	"mt": ["any"],
	"mr": ["any"],
	"my": ["any"],
	"mi": ["any"],
	"ne": ["any"],
	"nb": ["any"],
	"nya": ["any"],
	"or": ["any"],
	"ps": ["any"],
	"fa": ["any"],
	"pl": ["any"],
	"pt": ["any"],
	"pa": ["any"],
	"otq": ["any"],
	"ro": ["any"],
	"run": ["any"],
	"ru": ["any"],
	"sm": ["any"],
	"st": ["any"],
	"nso": ["any"],
	"tn": ["any"],
	"sn": ["any"],
	"sd": ["any"],
	"si": ["any"],
	"sk": ["any"],
	"sl": ["any"],
	"so": ["any"],
	"es": ["any"],
	"sw": ["any"],
	"sv": ["any"],
	"ty": ["any"],
	"ta": ["any"],
	"tt": ["any"],
	"te": ["any"],
	"th": ["any"],
	"bo": ["any"],
	"ti": ["any"],
	"to": ["any"],
	"tr": ["any"],
	"tk": ["any"],
	"uk": ["any"],
	"hsb": ["any"],
	"ur": ["any"],
	"ug": ["any"],
	"uz": ["any"],
	"vi": ["any"],
	"cy": ["any"],
	"xh": ["any"],
	"yo": ["any"],
	"yua": ["any"],
	"zu": ["any"]
}

URL_BING = 'https://www.bing.com/translator?mkt=en-US'
HEADERS_BING = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Language": "en-US,en;q=0.9",
  "Accept-Encoding": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
  "Connection": "keep-alive",
  "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

class BingAbuseHelper:
  def __init__(self,key,token,timeout) -> None:
    self.key = key
    self.token = token
    self.timeout = timeout
    self.expired = self._calcExpiredTime(key,timeout)
    #absue count
    self.counter = ThreadSafeCounter(0)

  def _calcExpiredTime(self,key,timeout) -> int:
    start = int(key[:-3])
    timeout = int(int(timeout) / 1000)

    return start + timeout - 600

  def isValid(self,now) -> bool:
    return now >= self.expired or self.counter.get() >= 10

class BingX(BaseTranslator):
  def __init__(self,name,appKey=None,appId=None, limit=-1,weight=1,proxy=False):
    super().__init__(name,appKey,appId,limit,weight,proxy)
    self.type = 'bingx'
    self.apiUrl = 'https://www.bing.com/ttranslatev3?isVertical=1&&IG=A4C997CC519A48C29AE92C20F2E5247E&IID=translator.5027'
    self.headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "*/*",
      "Accept-Language": "en-US,en;q=0.9",
      "Accept-Encoding": "gzip",
      "Connection": "keep-alive",
      "Origin": "https://www.bing.com",
      "Referer": "https://www.bing.com/translator?mkt=en-US",
      "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    self.mapping = {
      "auto": "auto-detect",
      "zh": 'zh-hans'
    }

    self.lock = threading.Lock()
    self.abuseHelper = None

  def doTranslate(self,text,src,dst) -> dict:
    _src = src
    _dst = dst
    if src in self.mapping:
      _src = self.mapping[src]

    if dst in self.mapping:
      _dst = self.mapping[dst]

    proxies = None
    if self.proxy:
      proxies = { "http": self.proxy, "https": self.proxy }

    if self.abuseHelper is None or self.abuseHelper.isValid(time.time()):
      with self.lock:
        if self.abuseHelper is None or self.abuseHelper.isValid(time.time()):
          self.abuseHelper = self.newBingAbuseHelper()

    params = {
      'fromLang': _src,
      'text': text,
      'to': _dst,
      'token': self.abuseHelper.token,
      'key': self.abuseHelper.key,
      'tryFetchingGenderDebiasedTranslations': 'true'
    }
    res = requests.post(
      self.apiUrl,
      headers=self.headers,
      data=params,
      proxies=proxies
    )

    if not res.ok:
      data = { 
        'code': res.status_code,
        'text': 'Token has been expired' if res.status_code == 205 else res.text 
      }
      raise TranslactionException(self.type,ExceptionType.NETWORK,data)
    
    result = res.json()
    if 'statusCode' in result:
      etype = ExceptionType.UNKNOWN
      if result['statusCode'] == 429:
        self.abuseHelper.counter.increment()
        etype = ExceptionType.REQUEST_LIMIT
      raise TranslactionException(self.type,etype,result)

    translations = result[0].get('translations')
    if translations is None:
      raise TranslactionException(self.type,ExceptionType.UNKNOWN,{text: 'translations is None'})

    return {
      "target_text": translations[0].get('text')
    }
  
  def newBingAbuseHelper(self) -> BingAbuseHelper:
    res = requests.get(URL_BING,headers=HEADERS_BING)
    if res.ok:
      html = res.text
      m = re.search(r'params_AbusePreventionHelper[ ]?=[ ]?\[([^]]+)\]',html)
      if m:
        items = m.group(1).split(',')
        return BingAbuseHelper(items[0],items[1].replace('"',''),items[2])
    else:
      data = { 'code': res.status_code,'text': res.text }
      raise TranslactionException(self.type,ExceptionType.NETWORK,data)

  def maxCharacterAtOnce(self):
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE