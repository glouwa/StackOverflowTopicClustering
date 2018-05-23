import numpy as np
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib
from sklearn import model_selection
import os

def save(name, M, D):
        if not os.path.exists(D):
            os.makedirs(D)       
            print("makedir", D)        
        filename = D+'{}-{}.pkl'.format(M.shape, name)
        joblib.dump(M, filename)    
        print(filename)
    
def writetopfeatureblock(wordtype, topfeature, tfidfcfg, mindf, mintf):    
    implname = 'stackoverflow/nltk/lemmatized'
    topfeatureSTR = '_'.join(topfeature)     
    tfidfcfgSTR = '{}{}_{}'.format(tfidfcfg[0], tfidfcfg[1], topfeatureSTR)
    corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, 
        topfeature, tfidfcfg[0], tfidfcfg[1], mindf, mintf)
    
    X = np.matrix(corpus.w.T)
    XR = np.matrix(corpus.doctermRaw.T)
    F = corpus.termssorted    
    Y = []
    tags = ['python', 'php', 'html', 'android', 'javascript', 'sql'] 
    for tag in tags:         
        Y.append(corpus.labels_(tag))

    directory = './dist/data/{}/{}/'.format(implname, tfidfcfgSTR)        
    save("X",  X,  directory)
    save("XR", XR, directory)
    save("F",  F,  directory)
    save('Y', np.array(Y).T, directory)
    save('T', np.array(tags), directory)
    return X, Y

def runTfidf(wordtype, htmlfeatuercombo, htmlfeatuercomboDfTf, tfidfs):    
    htmlfeatuercomboDfTf = [ (3,15),    
                         (5,15),
                         (5,25),
                         (5,25),
                         (7,50) ] 
    assert(len(htmlfeatuercomboDfTf) == len(htmlfeatuercombo))
    for wt in wordtype:        
        for hfidx, hfeature in enumerate(htmlfeatuercombo):
            for  tfidf in tfidfs:
                writetopfeatureblock(wt, hfeature, tfidf, htmlfeatuercomboDfTf[hfidx][0], htmlfeatuercomboDfTf[hfidx][1])
 
if __name__ == "__main__":  
    wordtype =             [ 'lemma' ]
    htmlfeatuercombo =     [ ['title'], ['title', 'inlinecode'], ['title', 'body'], ['title', 'code'], ['title', 'inlinecode', 'code', 'body']] 
    htmlfeatuercomboDfTf = [ (3,10),    (4,15),                  (5,25),            (5,25),            (7,50) ] 
    tfidfs =               [ [3, 2], [1, 1], [1, 0], [0, 1], [0, 0] ]       
    
    runTfidf(wordtype, htmlfeatuercombo, htmlfeatuercomboDfTf, tfidfs)
