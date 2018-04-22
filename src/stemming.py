import nltk
import json
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk.tag import pos_tag
#nltk.download() to download further packages/modules for nltk
'''Extract words from each sentence, tokenize and pos_tag it. Afterwards stemming happens'''

#'''ignore_stopwords: If set to True, stopwords are not stemmed and returned unchanged. Set to False by default.'''
snow_stemmer = SnowballStemmer("english", ignore_stopwords=True)
title_sentences = []
body_sentences = []
data = json.load(open('htmlcleaned.json'))

stem_map = {}
for question, values in data.items():
    tmp_dict = {}
    for entry in values:
        words = []
        stems = []
        for title_sentence in values[entry]:
            tokens = nltk.word_tokenize(title_sentence)
            tagged = nltk.pos_tag(tokens,tagset='universal')
            tmp_words = list(title_sentence.lower().split(" "))
            words += (tmp_words)
            for word in tmp_words:
                stems.append(snow_stemmer.stem(word))
        tmp_dict[entry] = stems
    stem_map.update({question: tmp_dict})

with open('stemmed.json', 'w') as outfile:
    json.dump(stem_map, outfile, sort_keys=True, indent=4)