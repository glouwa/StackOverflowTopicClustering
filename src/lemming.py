import nltk
import json
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag
#nltk.download() to download further packages/modules for nltk
'''Extract words from each sentence, tokenize and pos_tag it. Afterwards stemming happens'''

def convert_tagset(tag):
    '''Convert Universal tagset to wordnet tagset, default is 'NOUN' '''
    if tag == "ADJ":
        return wordnet.ADJ
    elif tag == "VERB":
        return wordnet.VERB
    elif tag == "ADV":
        return wordnet.ADV
    else:
        return wordnet.NOUN

lemmatizer = WordNetLemmatizer()
title_sentences = []
body_sentences = []
lem_map = {}
data = json.load(open('htmlcleaned.json'))

for question, values in data.items():
    tmp_dict = {}
    for entry in values:
        words = []
        lemmas = []
        for title_sentence in values[entry]:
            tokens = nltk.word_tokenize(title_sentence)
            tagged = nltk.pos_tag(tokens,tagset='universal')
            tmp_words = list(title_sentence.lower().split(" "))
            words += (tmp_words)
            for i in range(len(tmp_words)):
                lemmas.append(lemmatizer.lemmatize(tmp_words[i],convert_tagset(tagged[i][1])))
        tmp_dict[entry] = lemmas
    lem_map.update({question: tmp_dict})

with open('lemmatized.json', 'w') as outfile:
    json.dump(lem_map, outfile,sort_keys=True, indent=4)
