from nltk.corpus import stopwords

minwordlen = 3
nltk_stop_words = list(stopwords.words('english')) 


raw_stop_words = """
    user make run app application page new server page set method find add files image used line created 
    item field user column row api
    custom property size variables date parameter test cell statement difference program default
    output call found version string text array type number object variable access inside input update key element loop failed adding    
    project create something getting running like code function list table via 
    trying problem understand please want working 
    how using question thanks however following
    could n't get would great appreci help everyth work
    fine much seem realli anyth ve try much way still someone
    file error ... data use multiple one without change issue another name 
    two specific time example different tried first time value
    need know also 've works see possible thank solution able values anyone got right
    result even wrong case second looks instead currently advance simple 
    show added many think already sure idea locking current appreciated since
    """.split()
raw_stop_words.extend(nltk_stop_words)

stem_stop_words = """    
    fail number ad give correct let say write 0.0 0.0.0 0.0.0.0 1.0.0
    """.split()
stem_stop_words.extend(raw_stop_words)

lem_stop_words = """    
    give unable add fail character return 
    """.split()
stem_stop_words.extend(raw_stop_words)

whitelist = """
    c c++ c# r 
    """.split()

def filterintern(word, stopwordlist):
    lword = word.lower()
    stopword = lword in stopwordlist
    toosmall = len(word) < minwordlen
    toolong = len(word) > 10
    anumber = False
    notspecialchar = False
    whitel = lword in whitelist
    crap = stopword or toosmall or toolong or anumber or notspecialchar
    return whitel or not crap

def filterraw(rawword):    
    return filterintern(rawword, raw_stop_words)

def filterstem(stemword):
    return filterintern(stemword, stem_stop_words)

def filterlemmed(lemword):
    return filterintern(lemword, lem_stop_words)

def featurefilter(tkey):
    return tkey != 'code' and tkey != 'inlinecode'

"""
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
"""