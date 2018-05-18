import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet

from wordfilter import whitelist
from wordfilter import filterraw
from wordfilter import filterstem
from wordfilter import featurefilter 

snow_stemmer = SnowballStemmer("english", ignore_stopwords=True)

inputfile = './dist/data/bag-of-sentences/stackoverflow.json'
outputfile = './dist/data/bag-of-words/stackoverflow-stem.json'
inputfeature = 'sentences'
outputfeature = 'terms'

def splitone(result, qkey, tkey, sentence):    
    terms = word_tokenize(sentence)           
    if len(terms) > 0:
        if featurefilter(tkey):   
            fterms = []
            for pair in nltk.pos_tag(terms, tagset='universal'):                
                if pair[0] in whitelist:
                    fterms.append(pair[0])
                elif filterraw(pair[0]):                                 
                    if pair[1] == 'NOUN':
                        stemmed = snow_stemmer.stem(pair[0]).lower()
                        if filterstem(stemmed):
                            fterms.append(stemmed)
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
