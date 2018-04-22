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
data = json.load(open('./dist/htmlcleaned.json'))
print(len(data))

for question, values in data.items():
    tmp_dict = {}
    for entry in values:
        words = []
        lemmas = []
        for title_sentence in values[entry]:
            tokens = nltk.word_tokenize(title_sentence)
            tagged = nltk.pos_tag(tokens,tagset='universal')
            tmp_words = list(title_sentence.lower().split(" "))
            termset = tokens
            words += (termset)
            for i in range(len(termset)):
                interm = termset[i]        
                postag = convert_tagset(tagged[i][1])                
                lemterm = lemmatizer.lemmatize(interm, postag)
                lemmas.append(lemterm)
        tmp_dict[entry] = lemmas
    lem_map.update({question: tmp_dict})
    done = len(lem_map)
    if done % 500 == 0:
        print(done)

with open('./dist/lemmatized.json', 'w') as outfile:
    json.dump(lem_map, outfile,sort_keys=True, indent=4)

lem_ttf = {}
lem_ttf['body_terms'] = {}
lem_ttf['title_terms'] = {}
for qid, question in lem_map.items():
    for body_term in question['body']:
        lem_ttf['body_terms'][body_term] = lem_ttf['body_terms'].get(body_term, 0)+1

    for title_term in question['title']:
        lem_ttf['title_terms'][title_term] = lem_ttf['title_terms'].get(title_term, 0)+1

with open('./dist/lemmatized-meta.json', 'w') as outfile:
    json.dump(lem_ttf, outfile, sort_keys=True, indent=4)