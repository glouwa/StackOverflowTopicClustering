import numpy as np
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib
from sklearn import model_selection
from ipywidgets import FloatProgress
from IPython.display import display
from src.algo import frames

def featuretranform(srcpath, destpath, algo, X, Y, k):
    if algo == 'chi2':
        fs = feature_selection.SelectKBest(feature_selection.chi2, k=k).fit(X, Y)    
    elif algo == 'f_classif':
        fs = feature_selection.SelectKBest(feature_selection.f_classif, k=k).fit(X, Y)    
    elif algo == 'mutual_info_classif':
        fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=k).fit(X, Y)
    else:
        assert(False)

    frames.save(destpath, 'X',      fs.transform(X))
    frames.save(destpath, 'Mask',   fs.get_support())
    frames.save(destpath, 'Indices',fs.get_support(indices=True))    
    frames.save(destpath, 'Scores', fs.scores_)
    frames.save(destpath, 'Pvalue', fs.pvalues_)    

def savefeatures(srcpath, destpath, tag, algo, nsamples, k):       
    #X, Y, F = joblib.load(srcpath, 'X', 'Y','F') 
    X = joblib.load(srcpath+'X.pkl')
    F = joblib.load(srcpath+'F.pkl')
    Y = joblib.load(srcpath+'Y.pkl')
    C = joblib.load(srcpath+'C.pkl')

    tagidx = list(C).index(tag)    
    Yc = Y[:, tagidx]

    frames.save(destpath, 'assertF', F)
    frames.save(destpath, 'assertY', Yc)

    X_train, _, Y_train, _ = model_selection.train_test_split(X, Yc, test_size=0, random_state=0)            
    fselsamples = nsamples
    X_ = X_train[:fselsamples]
    Y_ = Y_train[:fselsamples]
    assert(len(X_) > 500)
    
    featuretranform(srcpath, destpath, algo, X_, Y_, k)

def FeatureFrame():
    return frames.FeatureFrame()

def run(frame, nsamples, k):    
    f = FloatProgress(min=0, max=frame.shape[0])
    display(f) 
    
    for task in frame.index.values:
        f.value += 1
        destpath = './dist/data/'+'/'.join(task)+'/'        
        srcpath = './dist/data/'+'/'.join(task[:5])+'/'
        
        tag = task[5]        
        algo = task[6]        
        savefeatures(srcpath, destpath, tag, algo, nsamples, k)        

    return frames.cell2string.file2shape(frame)    
    