import unittest,os

class TestAPP(unittest.TestCase):
  def test_split_paragraph(self):
    from src.utils.text import splitByMark

    text = 'hello\nworld\n'

    paragraphs = splitByMark(text,len(text),6,{'\n'})
    self.assertEqual(len(paragraphs),2)

    paragraphs = splitByMark(text,len(text),20,{'\n'})
    self.assertEqual(len(paragraphs),1)

    text = 'hello.world'
    paragraphs = splitByMark(text,len(text),6,{'.'})
    self.assertEqual(len(paragraphs),2)
    
    text = 'hello!world'
    paragraphs = splitByMark(text,len(text),6,{'!'})
    self.assertEqual(len(paragraphs),2)

    text = 'hello,world'
    paragraphs = splitByMark(text,len(text),5,{'\n'})
    self.assertEqual(len(paragraphs),1)

if __name__ == '__main__':
  unittest.main()