import numpy as np
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib

def writetopfeatureblock(wordtype, topfeature, tfidfcfg, mindf, mintf):    
    topfeatureSTR = '_'.join(topfeature)     
    tfidfcfgSTR = '{}{}_{}'.format(tfidfcfg[0], tfidfcfg[1], topfeatureSTR)
    corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1], mindf, mintf)
    print("\n")

    X = np.matrix(corpus.w.T)
    XR = np.matrix(corpus.doctermRaw.T)
    F = corpus.termssorted
    print("nltk reduced", X.shape)

    def savetfidf(X, Yf, F, name):
        fselsamples = 10000
        tags = ['python', 'php', 'html', 'android', 'javascript', 'sql']    
        joblib.dump(X,                            './dist/data/tf-idf/{}/{}-X.pkl'.format(tfidfcfgSTR, name))
        joblib.dump(XR,                           './dist/data/tf-idf/{}/{}-XR.pkl'.format(tfidfcfgSTR, name))
        joblib.dump(F,                            './dist/data/tf-idf/{}/{}-F.pkl'.format(tfidfcfgSTR, name))
        for tag in tags:        
            Y = Yf(tag)
            joblib.dump(Y,                        './dist/data/tf-idf/{}/{}-Y-{}.pkl'.format(tfidfcfgSTR, name, tag))
            fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=500).fit(X[:fselsamples], Y[:fselsamples])
            joblib.dump(fs.transform(X),          './dist/data/tf-idf/{}/{}-X-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
            joblib.dump(F[fs.get_support()],      './dist/data/tf-idf/{}/{}-F-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
            fs2 = feature_selection.SelectKBest(feature_selection.chi2, k=500).fit(X[:fselsamples], Y[:fselsamples])
            joblib.dump(fs2.transform(X),         './dist/data/tf-idf/{}/{}-X-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))
            joblib.dump(F[fs2.get_support()],     './dist/data/tf-idf/{}/{}-F-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))
        
    savetfidf(X,  corpus.labels_, F,  'nltk')
    #savetfidf(X2, corpus.labels,  F2, 'sklearn')


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