import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

from wordfilter import whitelist
from wordfilter import filterraw
from wordfilter import featurefilter 

inputfile = './dist/data/bag-of-sentences/stackoverflow.json'
outputfile = './dist/data/bag-of-words/stackoverflow-raw.json'
inputfeature = 'sentences'
outputfeature = 'terms'

def splitone(result, qkey, tkey, sentence):
    terms = word_tokenize(sentence)           
    if len(terms) > 0:
        if featurefilter(tkey):
            fterms = []
            for pair in nltk.pos_tag(terms, tagset='universal'):  
                if pair[0].lower() in whitelist:
                    fterms.append(pair[0].lower())              
                elif filterraw(pair[0].lower()):                                     
                    if pair[1] == 'NOUN':                        
                        fterms.append(pair[0].lower())
        else:
            fterms = terms
        result[qkey][outputfeature][tkey].append(fterms)

def splitterms():
    result = json.load(open(inputfile))
    for qkey, qvalue in result.items():
        result[qkey][outputfeature] = result[qkey].get(outputfeature, {})
        for tkey, tvalue in result[qkey][inputfeature].items():
            result[qkey][outputfeature][tkey] = []            
            for sentence in result[qkey][inputfeature][tkey]:     
                splitone(result, qkey, tkey, sentence)

        del result[qkey][inputfeature]

    with open(outputfile, 'w') as outfile:
        json.dump(result, outfile, indent=4)

splitterms()

