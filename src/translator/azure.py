import uuid

from .base_translator import BaseTranslator
from src.translator.exception import TranslactionException, ExceptionType
from src.utils import http
import json

LANGUAGE = {
    "en": ["zh-hans", "zh", "zh-hant"],
    "zh-hans": ["en", "ja"],
    "zh": ["en", "ja"],
    "zh-hant": ["en", "ja"],
    "ja": ["zh-hans", "zh", "zh-hant"]
}


class Azure(BaseTranslator):
    def __init__(self, name, appKey, region, limit=-1, weight=1, proxy=False):
        super().__init__(name, appKey, region, limit, weight, proxy)
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
                data['trans_type'] = f'src -> {src}, dst -> {dst}'
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
