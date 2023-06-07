import unittest,os
from src.translator import TRANSLATORS

class TestTranslator(unittest.TestCase):
  def test_google(self):
    GoogleX = TRANSLATORS.get('googlex')
    google = GoogleX('google1')
    result = google.translate('hello','en','zh')

    self.assertTrue('target_text' in result and len(result['target_text']) > 0)

  def test_bing(self):
    BingX = TRANSLATORS.get('bingx')
    bing = BingX('bing1')
    result = bing.translate('hello','en','zh')

    self.assertTrue('target_text' in result and len(result['target_text']) > 0)

  def test_tencent(self):
    appid = os.getenv('TENCENT_APPID')
    key = os.getenv('TENCENT_KEY')

    Tencent = TRANSLATORS.get('tencent')
    tencent = Tencent('tencent1',key,appid)
    result = tencent.translate('hello','en','zh')

    self.assertTrue('target_text' in result and len(result['target_text']) > 0)

  def test_caiyun(self):
    key = os.getenv('CAIYUN')
    Caiyun = TRANSLATORS.get('caiyun')
    caiyun = Caiyun('caiyun1',key)
    result = caiyun.translate('hello','en','zh')

    self.assertTrue('target_text' in result and len(result['target_text']) > 0)

  def test_baidu(self):
    appid = os.getenv('BAIDU_APPID')
    key = os.getenv('BAIDU_KEY')

    Baidu = TRANSLATORS.get('baidu')
    baidu = Baidu('baidu1',key,appid)
    result = baidu.translate('hello','en','zh')

    self.assertTrue('target_text' in result and len(result['target_text']) > 0)

if __name__ == '__main__':
  unittest.main()