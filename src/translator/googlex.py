from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException,ExceptionType
import requests
from src.utils import http

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
	"ay": ["any"],
	"az": ["any"],
	"bm": ["any"],
	"eu": ["any"],
	"be": ["any"],
	"bn": ["any"],
	"bho": ["any"],
	"bs": ["any"],
	"bg": ["any"],
	"ca": ["any"],
	"ceb": ["any"],
	"ny": ["any"],
	"co": ["any"],
	"hr": ["any"],
	"cs": ["any"],
	"da": ["any"],
	"dv": ["any"],
	"doi": ["any"],
	"nl": ["any"],
	"en": ["any"],
	"eo": ["any"],
	"et": ["any"],
	"ee": ["any"],
	"tl": ["any"],
	"fi": ["any"],
	"fr": ["any"],
	"fy": ["any"],
	"gl": ["any"],
	"ka": ["any"],
	"de": ["any"],
	"el": ["any"],
	"gn": ["any"],
	"gu": ["any"],
	"ht": ["any"],
	"ha": ["any"],
	"haw": ["any"],
	"iw": ["any"],
	"hi": ["any"],
	"hmn": ["any"],
	"hu": ["any"],
	"is": ["any"],
	"ig": ["any"],
	"ilo": ["any"],
	"id": ["any"],
	"ga": ["any"],
	"it": ["any"],
	"ja": ["any"],
	"jw": ["any"],
	"kn": ["any"],
	"kk": ["any"],
	"km": ["any"],
	"rw": ["any"],
	"gom": ["any"],
	"ko": ["any"],
	"kri": ["any"],
	"ku": ["any"],
	"ckb": ["any"],
	"ky": ["any"],
	"lo": ["any"],
	"la": ["any"],
	"lv": ["any"],
	"ln": ["any"],
	"lt": ["any"],
	"lg": ["any"],
	"lb": ["any"],
	"mk": ["any"],
	"mai": ["any"],
	"mg": ["any"],
	"ms": ["any"],
	"ml": ["any"],
	"mt": ["any"],
	"mi": ["any"],
	"mr": ["any"],
	"lus": ["any"],
	"mn": ["any"],
	"my": ["any"],
	"ne": ["any"],
	"no": ["any"],
	"or": ["any"],
	"om": ["any"],
	"ps": ["any"],
	"fa": ["any"],
	"pl": ["any"],
	"pt": ["any"],
	"pa": ["any"],
	"qu": ["any"],
	"ro": ["any"],
	"ru": ["any"],
	"sm": ["any"],
	"sa": ["any"],
	"gd": ["any"],
	"nso": ["any"],
	"sr": ["any"],
	"st": ["any"],
	"sn": ["any"],
	"sd": ["any"],
	"si": ["any"],
	"sk": ["any"],
	"sl": ["any"],
	"so": ["any"],
	"es": ["any"],
	"su": ["any"],
	"sw": ["any"],
	"sv": ["any"],
	"tg": ["any"],
	"ta": ["any"],
	"tt": ["any"],
	"te": ["any"],
	"th": ["any"],
	"ti": ["any"],
	"ts": ["any"],
	"tr": ["any"],
	"tk": ["any"],
	"ak": ["any"],
	"uk": ["any"],
	"ur": ["any"],
	"ug": ["any"],
	"uz": ["any"],
	"vi": ["any"],
	"cy": ["any"],
	"xh": ["any"],
	"yi": ["any"],
	"yo": ["any"],
	"zu": ["any"]
}

class GoogleX(BaseTranslator):
  def __init__(self,name,appKey=None,appId=None, limit=-1,weight=1,proxy=False):
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