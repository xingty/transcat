import time
from . import hash
def splitByMark(text,textSize,maxLenOfCharacters,mark={'\n'}):
  left = 0
  right = 0
  texts = []
  for i in range(textSize):
    if text[i] in mark:
      segLen = i - left + 1
      if segLen == 0:
        texts.append(text[left:i])
        left = i + 1
        right = left
      elif segLen > maxLenOfCharacters:
        content = None
        if left == right:
          content = text[left:i]
          left = i + 1
          right = left
        else:
          content = text[left:right]
          left = right + 1
          right = i
        texts.append(content)
      else:
        right = i
        
  if left != right:
    texts.append(text[left:right])
  
  if right < textSize:
    content = text[right:textSize]
    if content != '' and content not in mark:   
      texts.append(content)

  return texts


def buildServiceId(name,type):
  query = f'{name}_{type}_{time.strftime("%Y-%m")}'
  return hash.md5(query)