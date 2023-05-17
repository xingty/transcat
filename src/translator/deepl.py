from .base_translator import BaseTranslator

class DeepL(BaseTranslator):
  def __init__(self,secretKey):
    super().__init__('id',secretKey)
    self.type = "DEEPL"