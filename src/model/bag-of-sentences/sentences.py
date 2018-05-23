import nltk
import json
from nltk.tokenize import sent_tokenize

inputfile = './dist/data/bag-of-texts/stackoverflow.json'
outputfile = './dist/data/bag-of-sentences/stackoverflow.json'
inputfeature = 'text'
outputfeature = 'sentences'

def splitone(result, qkey, tkey, block):
    if tkey != 'code' and tkey != 'inlinecode':
        tockens = sent_tokenize(block)
        if len(tockens) > 0:
            for sentence in tockens:
                tmp = sentence.replace('c#', 'csharp')
                tmp2 = tmp.replace('C#', 'csharp')
                result[qkey][outputfeature][tkey].append(tmp2)
    else: 
        result[qkey][outputfeature][tkey].append(block)

def splitsentences():
    result = json.load(open(inputfile))
    for qkey, qvalue in result.items():
        result[qkey][outputfeature] = result[qkey].get(outputfeature, {})
        for tkey, tvalue in result[qkey][inputfeature].items():
            result[qkey][outputfeature][tkey] = []
            for block in result[qkey][inputfeature][tkey]:                
                splitone(result, qkey, tkey, block)

        del result[qkey][inputfeature]

    with open(outputfile, 'w') as outfile:
        json.dump(result, outfile, indent=4)

splitsentences()