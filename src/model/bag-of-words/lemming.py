import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag

from wordfilter import filterraw
from wordfilter import filterlemmed 
from wordfilter import featurefilter 

lemmatizer = WordNetLemmatizer()

inputfile = './dist/data/bag-of-sentences/stackoverflow.json'
outputfile = './dist/data/bag-of-words/stackoverflow-lemma.json'
inputfeature = 'sentences'
outputfeature = 'terms'

u = {}

def splitone(result, qkey, tkey, sentence):    
    terms = nltk.word_tokenize(sentence)
    if len(terms) > 0:
        if featurefilter(tkey):   
            fterms = []
            for pair in nltk.pos_tag(terms, tagset='universal'):                
                if filterraw(pair[0]):
                    """
                    postag = convert_tagset3(pair[1])                    
                        if postag.startswith('n'):
                        fterms.append(pair[0])
                    """
                    u[pair[1]] = True
                    postag = convert_tagset3(pair[1])                    
                    if pair[1] == 'NOUN':
                        lemterm = lemmatizer.lemmatize(pair[0], postag).lower()
                        if filterlemmed(lemterm):
                            fterms.append(lemterm)                    
        else:
            fterms = terms
        result[qkey][outputfeature][tkey].append(fterms)

def convert_tagset3(tag):    
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN    
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

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

    print(u)
splitterms()
