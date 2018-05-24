import numpy as np
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib
from sklearn import model_selection

def savefeatures(X, Yf, F, name):            
    X, Yf, F, =load (X, Yf, F,)
    for tag in tags: 
        Y = Yf(tag)
        joblib.dump(Y,                        './dist/data/tf-idf/{}/{}-Y-{}.pkl'.format(tfidfcfgSTR, name, tag))

        X_train, _, Y_train, _ = model_selection.train_test_split(X, Y, test_size=0, random_state=0)            
        fselsamples = 10000
        X_ = X_train[:fselsamples]
        Y_ = Y_train[:fselsamples]
        assert(len(X_) > 500)
        
        fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=1000).fit(X_, Y_)
        joblib.dump(fs.transform(X),          './dist/data/tf-idf/{}/{}-X-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
        joblib.dump(F[fs.get_support()],      './dist/data/tf-idf/{}/{}-F-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
        joblib.dump(fs.scores_,               './dist/data/tf-idf/{}/{}-S-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
        
        fs2 = feature_selection.SelectKBest(feature_selection.chi2, k=1000).fit(X_, Y_)
        selectedX = fs2.transform(X)
        #save(fs2.transform(X), './dist/data/tf-idf/{}/{}-X-{}-chi2'.format(tfidfcfgSTR, name, tag))
        # write input index
        # F is output
        joblib.dump(fs2.transform(X),         './dist/data/tf-idf/{}/{}-X-{}-chi2-({}, {}).pkl'.format(tfidfcfgSTR, name, tag, selectedX.shape[0], selectedX.shape[1]))
        joblib.dump(F[fs2.get_support()],     './dist/data/tf-idf/{}/{}-F-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))
        joblib.dump(fs.scores_,               './dist/data/tf-idf/{}/{}-S-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))

        savefeatures(X,  corpus.labels_, F,  'nltk')

def runFeatureSelect():
    tags = ['python', 'php', 'html', 'android', 'javascript', 'sql']    


from src.algo import frames
def FeatureFrame(cellinit):
    return frames.FeatureFrame(cellinit)

"""
    tags = ['python', 'php', 'html', 'android', 'javascript', 'sql']    
    writetopfeatureblock('lemma', ['title'],         [3, 2], 3, 15)
    writetopfeatureblock('lemma', ['title', 'code'], [3, 2], 5, 25) # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
    writetopfeatureblock('lemma', ['title', 'body'], [3, 2], 5, 25)
    writetopfeatureblock('lemma', ['code', 'body'],  [3, 2], 7, 50)

    writetopfeatureblock('lemma', ['title'],         [1, 1], 3, 15)
    writetopfeatureblock('lemma', ['title', 'code'], [1, 1], 5, 25)
    writetopfeatureblock('lemma', ['title', 'body'], [1, 1], 5, 25)
    writetopfeatureblock('lemma', ['code', 'body'],  [1, 1], 7, 50)

    writetopfeatureblock('lemma', ['title'],         [0, 0], 3, 15)
    writetopfeatureblock('lemma', ['title', 'code'], [0, 0], 5, 25)
    writetopfeatureblock('lemma', ['title', 'body'], [0, 0], 5, 25)
    writetopfeatureblock('lemma', ['code', 'body'],  [0, 0], 7, 50)

    writetopfeatureblock('lemma', ['title'],         [0, 1], 3, 15)
    writetopfeatureblock('lemma', ['title', 'code'], [0, 1], 5, 25)
    writetopfeatureblock('lemma', ['title', 'body'], [0, 1], 5, 25)
    writetopfeatureblock('lemma', ['code', 'body'],  [0, 1], 7, 50)

"""