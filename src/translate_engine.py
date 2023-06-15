import time,logging,threading
from src.utils.text import splitByMark
from src.translator.exception import TranslactionException,ExceptionType
from src.translator import usageInfo as usage
import langdetect,threading

logger = logging.getLogger()

class TranslateEngine():
  def __init__(self,service,mode) -> None:
    self.mode = mode
    self.service = service
    self.lock = threading.Lock()

  def translate(self,text,src,dst) -> dict:
    """
    Translates text from one language to another using a translation service.
    :param text: The text to be translated.
    :param src: The source language code of the text.
    :param dst: The destination language code to translate the text to.
    :return: A dictionary containing the translated text and additional information.
    """
    count = 0
    translator = None
    detectLang = None
    try:
      while (translator == None and count < 5):
        try:
          count += 1
          translator = self.service.choose(text,src,dst)
          if not translator:
            time.sleep(0.05)
        except TranslactionException as te:
          if te.etype == ExceptionType.SERVICE_NOT_FOUND:
            if detectLang is None:
              try:
                detectLang = langdetect.detect(text)
              except Exception:
                pass
            
            logger.warn(
              "No service found for %s => %s, detectLang => %s text => %s",
              src,dst,detectLang,text
            )

            if detectLang is None:
              break

            if detectLang != src:
              src = detectLang
              continue
            
            raise te
          raise te  
            
    except Exception as e:
      logger.error('Unknown exception',exc_info=True)
      raise e

    if not translator:
      logger.warn('Could not find a translator for: src: %s, dst: %s, text: %s',text,src,dst)
      raise TranslactionException(None,ExceptionType.SERVICE_NOT_FOUND,{'text': text, 'src': src, 'dst': dst})

    size = len(text)
    max = translator.maxCharacterAtOnce()
    texts = [text]
    if size > max:
      texts = self.splitText(text,size,max)
      logger.warn('Split text to multiple paragraphs: textSize: %s, max: %s',size,max)

    return self._doTranslate(translator,text,texts,src,dst)

  def _doTranslate(self,translator,sourceText,texts,src,dst) -> dict:
    ex = None
    result = None
    index = 0
    count = 0
    size = len(texts)
    while index < size and count < 1:
      # 每个翻译服务会有不同的限流策略,用之前需要确定当前还有限额
      if not translator.tryAcquire():
        time.sleep(0.05)
        continue

      paragraph = texts[index].strip()
      try:
        data = translator.translate(paragraph,src,dst)
        if not result:
          result = data
        else:
          trans = data.get('target_text')
          if not trans:
            print(f'name: {translator.name}, error: {data}')
            count += 1
            time.sleep(0.1)
            continue

          result['target_text'] += trans + '\n'
        
        index += 1

      except TranslactionException as e:
        if e.etype == ExceptionType.REQUEST_LIMIT:
          logger.warn('Request limit, translator: %s, src: %s, dst: %s',translator.name,src,dst)
          time.sleep(0.3)
        else:
          count += 1
        print(f'name: {e.engine}, message: {e.data}')
      except Exception as e:
        logger.error('Unknown error: count: %s, cause: %s,',count,e,exc_info=True)
        ex = e
        count += 1
        time.sleep(0.1)
      finally:
        usage.updateUsageInfo(translator.name,translator.type,len(paragraph))

    if result:
      result.update({
        'sid': translator.name,
        'src': src,
        'dst': dst,
        'source_text': sourceText,
        'engine': translator.type
      })

      return result
    
    raise ex if ex else Exception(f"Unknown error for translator {translator.name}")

  def splitText(self,text,textSize,maxLenOfCharacters) -> list:
    texts = splitByMark(text,textSize,maxLenOfCharacters,{'\n'})
    if len(texts) == 1:
      mark = {'!',"\uff01",".","。","?","\uff1f"}
      texts = splitByMark(text,textSize,maxLenOfCharacters,mark)
      last = texts[-1]
      if len(last) > maxLenOfCharacters:
        texts[-1] = last[0:maxLenOfCharacters]
  
    return texts

  def switchMode(self,service,mode) -> None:
    self.service = service
    self.mode = mode

  def selectServer(self,index) -> None:
    if self.mode == 'select':
      self.service.select(index)  

  def getMode(self):
    return self.mode