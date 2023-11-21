import uuid

from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException, ExceptionType
from src.utils import http
import json

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


class Azure(BaseTranslator):
    def __init__(self, name, appKey, region, appId=None, limit=-1, weight=1, proxy=False):
        super().__init__(name, appKey, appId, limit, weight, proxy)
        assert appKey is not None and len(appKey) > 0
        self.type = "azure"
        self.apiUrl = 'https://api.cognitive.microsofttranslator.com/translate'
        self.region = region
        self.headers = {
            'Ocp-Apim-Subscription-Key': appKey,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def doTranslate(self, text, src, dst) -> dict:
        _src = src
        _dst = dst
        if 'zh-' in src:
            _src = 'zh' if src == 'zh-hans' else 'zh-TW'

        if 'zh-' in dst:
            _dst = 'zh' if dst == 'zh-hans' else 'zh-TW'
        params = {
            'api-version': '3.0',
            'from': _src,
            'to': _dst
        }
        body = [{
            'text': text
        }]

        try:
            request = http.post(
                url=self.apiUrl,
                params=params,
                data=json.dumps(body),
                headers=self.headers,
                proxy=self.proxy,
            )
            response = request.json()
            data = response[0]
            if 'translations' not in data:
                data = f'src -> {src}, dst -> {dst}'
                raise TranslactionException(self.type, ExceptionType.UNKNOWN, data)
            return {
                "target_text": "\n".join(data['translations'][0]['text']),
            }
        except http.NetworkException as e:
            raise TranslactionException(self.type, ExceptionType.NETWORK, e.message)

    def maxCharacterAtOnce(self):
        return 50000

    def supportedLanguage(self) -> dict:
        return LANGUAGE
