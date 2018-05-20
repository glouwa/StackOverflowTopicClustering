import sys
import nltk
import json
import copy
from nltk.util import ngrams

n = int(sys.argv[1])

inputfile = './dist/data/bag-of-words/stackoverflow-lemma.json'
outputfile = './dist/data/ngrams/stackoverflow-'+str(n)+'gram-stem.json'
inputfeature = 'terms'
outputfeature = 'terms'

def splitone(result, qkey, tkey, sentence):        
    fterms = ngrams(sentence, n)    
    fterms = [' '.join(str(i) for i in tupl) for tupl in fterms if tupl[0] != tupl[1]]        
    result[qkey][outputfeature][tkey].append(fterms)

def splitterms():
    datain = json.load(open(inputfile))
    result = {}
    for qkey, qvalue in datain.items():
        result[qkey] = {}
        result[qkey][outputfeature] = {}
        for tkey, tvalue in datain[qkey][inputfeature].items():
            result[qkey][outputfeature][tkey] = []            
            for sentence in datain[qkey][inputfeature][tkey]:
                splitone(result, qkey, tkey, sentence)

    with open(outputfile, 'w') as outfile:
        json.dump(result, outfile, indent=4)

splitterms()