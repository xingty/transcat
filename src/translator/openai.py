from .base_translator import BaseTranslator
from src.utils import http
import json

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


API_URL = 'https://api.openai.com/v1/chat/completions'

class OpenAI(BaseTranslator):
  def __init__(self, name, appKey, appId=None, region=None,  limit=-1, weight=1, proxy=False):
    super().__init__(name, appKey, appId, limit, weight, proxy)
    self.model = 'gpt-3.5-turbo'
    self.type = 'openai'
    #thanks for @yetone's openai-translator
    self.systemPrompt = 'You are a translation engine that can only translate text and cannot interpret it.'
    self.prompt = self.initDefaultPrompt()
    self.temperature = 0.3
    self.headers = {
      "Content-Type": "application/json; charset=utf-8",
      "Authorization": "Bearer {}".format(self.appKey)
    }

  def initDefaultPrompt(self):
    with open('assets/prompt.txt') as f:
      return f.read()
  
  def doTranslate(self,text,src,dst) -> dict:
    userPrompt = self.prompt.format(src,dst,text)

    payload = {
      'model': self.model,
      'temperature': self.temperature,
      'frequency_penalty': 1,
      'messages': [
        {
          "role": "system",
          "content": self.systemPrompt
        },
        {
          "role": "user",
          "content": userPrompt
        }
      ]
    }

    response = http.post(API_URL, data=json.dumps(payload), headers=self.headers,proxy=self.proxy)
    data = response.json()

    return {
      "model": data['model'],
      "target_text": data['choices'][0]['message']['content']
    }

  def maxCharacterAtOnce(self):
    return 2000

  def supportedLanguage(self) -> dict:
    return LANGUAGE

