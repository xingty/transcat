from src.translator.caiyun import Caiyun
from src.translator.tencent import Tencent
from src.translator.baidu import Baidu
from src.translator.deeplx import DeepLX
from src.translator.googlex import GoogleX
from src.translator.usage_info import UsageInfo
from src.translator.bingx import BingX

TRANSLATORS = {
  "caiyun": Caiyun,
  "tencent": Tencent,
  "baidu": Baidu,
  "deeplx": DeepLX,
  "googlex": GoogleX,
  "bingx": BingX
}

usageInfo: UsageInfo = UsageInfo()