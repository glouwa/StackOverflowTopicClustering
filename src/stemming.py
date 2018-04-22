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
data = json.load(open('./dist/htmlcleaned.json'))

print(len(data))

stem_map = {}
for question, values in data.items():
    tmp_dict = {}
    for entry in values:
        words = []
        stems = []
        for title_sentence in values[entry]:            
            tmp_words = list(title_sentence.lower().split(" "))
            words += (tmp_words)
            for word in tmp_words:
                stems.append(snow_stemmer.stem(word))
        tmp_dict[entry] = stems
    stem_map.update({question: tmp_dict})
    done = len(stem_map)
    if done % 1000 == 0:
        print(done)

with open('./dist/stemmed.json', 'w') as outfile:
    json.dump(stem_map, outfile, sort_keys=True, indent=4)

stem_ttf = {}
stem_ttf['body_terms'] = {}
stem_ttf['title_terms'] = {}
for qid, question in stem_map.items():
    for body_term in question['body']:
        stem_ttf['body_terms'][body_term] = stem_ttf['body_terms'].get(body_term, 0)+1

    for title_term in question['title']:
        stem_ttf['title_terms'][title_term] = stem_ttf['title_terms'].get(title_term, 0)+1

with open('./dist/stemmed-meta.json', 'w') as outfile:
    json.dump(stem_ttf, outfile, sort_keys=True, indent=4)