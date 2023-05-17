from src.translator.caiyun import Caiyun
from src.translator.tencent import Tencent
from src.translator.baidu import Baidu
from src.translator.deeplx import DeepLX
from src.translator.google import Google

TRANSLATORS = {
  "caiyun": Caiyun,
  "tencent": Tencent,
  "baidu": Baidu,
  "deeplx": DeepLX,
  "google": Google
}