import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag

lemmatizer = WordNetLemmatizer()

stop_words = """
    project create something getting running like
    trying problem understand please want working 
    how using question thanks however following""".split()

nltk_words = list(stopwords.words('english')) 
stop_words.extend(nltk_words)

inputfile = './dist/data/bag-of-sentences/stackoverflow.json'
outputfile = './dist/data/bag-of-words/stackoverflow-lemma.json'
inputfeature = 'sentences'
outputfeature = 'terms'

def splitone(result, qkey, tkey, sentence):    
    terms = nltk.word_tokenize(sentence)
    if len(terms) > 0:
        if tkey != 'code' and tkey != 'inlinecode':   
            fterms = []        
            for pair in nltk.pos_tag(terms, tagset='universal'):
                if not pair[0].lower() in stop_words and len(pair[0]) > 2:
                    postag = convert_tagset3(pair[1])
                    lemterm = lemmatizer.lemmatize(pair[0], postag).lower()
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
        return wordnet.NOUN

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
