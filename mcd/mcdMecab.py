# -*- coding: utf-8 -*-


import re, string

kanji = u''.join([unichr(c) for c in range(0x4E00, 0x9FBF)])
hiragana = u''.join([unichr(c) for c in range(0x3040, 0x309F)])
 
ex = re.compile('([%s]+\[.*?\])' % kanji, re.UNICODE)
ex2 = re.compile('\[[%s]+\]' % hiragana, re.UNICODE)

def parse(s, clozeText):

  cards = []

  for word in ex.findall(s):
    for c in word:
      if c in kanji:
        cloze = word.replace(c, clozeText)
        cards.append(
            (
              ex2.sub('', s.replace(word, cloze)).replace(' ', ''),
              c,
              word.split('[')[0],
              word
            )
        )

  return cards

if __name__ == '__main__':
  for card in parse( u'この 語[ご]は 使用[しよう] 頻度[ひんど]が 高[たか]い 語[ご]は', '[...]'):
    print '%s, %s, %s' % card
