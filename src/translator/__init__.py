from src.translator.caiyun import Caiyun
from src.translator.tencent import Tencent
from src.translator.baidu import Baidu
from src.translator.deeplx import DeepLX
from src.translator.googlex import GoogleX
from src.translator.usage_info import UsageInfo
from src.translator.bingx import BingX
from src.translator.openai import OpenAI
from src.translator.azure import Azure

TRANSLATORS = {
  "caiyun": Caiyun,
  "tencent": Tencent,
  "baidu": Baidu,
  "deeplx": DeepLX,
  "googlex": GoogleX,
  "bingx": BingX,
  "openai": OpenAI,
  "azure": Azure,
}

usageInfo: UsageInfo = UsageInfo()