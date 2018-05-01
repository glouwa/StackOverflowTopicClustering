import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams

snow_stemmer = SnowballStemmer("english", ignore_stopwords=True)

stop_words = """
    project create something getting running like
    trying problem understand please want working 
    how using question thanks however following""".split()

nltk_words = list(stopwords.words('english')) 
stop_words.extend(nltk_words)

inputfile = './dist/data/bag-of-sentences/stackoverflow.json'
outputfile = './dist/data/ngrams/stackoverflow-3gram-stem.json'
inputfeature = 'sentences'
outputfeature = 'terms'

def splitone(result, qkey, tkey, sentence):    
    terms = word_tokenize(sentence)           
    if tkey != 'code' and tkey != 'inlinecode':        
        fterms = [snow_stemmer.stem(w).lower() for w in terms if not w.lower() in stop_words and len(w) > 2]
    else:
        fterms = terms
    fterms = ngrams(fterms, 3)
    fterms = [' '.join(str(i) for i in tupl) for tupl in fterms]        
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
