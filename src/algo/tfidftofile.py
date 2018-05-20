import numpy as np
from tfidf import StackoverflowCorpus
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sparse2dense import DenseTransformer
from sklearn.externals import joblib

def writetopfeatureblock(wordtype, topfeature, tfidfcfg):    
    topfeatureSTR = '{}_{}'.format(topfeature[0], topfeature[1])     
    tfidfcfgSTR = '{}{}_{}'.format(tfidfcfg[0], tfidfcfg[1], topfeatureSTR)
    corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
    print("\n")

    X = np.matrix(corpus.w.T)
    F = corpus.termssorted
    print("nltk reduced", X.shape)

    """
    pipeline = Pipeline([
        ('vect', text.CountVectorizer(stop_words='english', min_df=15, max_df=.9, binary=False, ngram_range=(1, 2))),
        ('tfidf', text.TfidfTransformer(sublinear_tf=True)), # smooth_idf=True
        ('dense', DenseTransformer()),
    ])
    X2 = pipeline.fit_transform(corpus.documentsstr)
    F2 = pipeline.named_steps['vect'].get_feature_names()
    print("sklearn reduced", X2.shape, len(F2))
    """

    def savetfidf(X, Yf, F, name):
        tags = ['python', 'php', 'html', 'android', 'javascript', 'sql']    
        for tag in tags:        
            Y = Yf(tag)
            joblib.dump(Y,                        './dist/data/tf-idf/{}/{}-Y-{}.pkl'.format(tfidfcfgSTR, name, tag))
            fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=500).fit(X, Y)
            joblib.dump(fs.transform(X),          './dist/data/tf-idf/{}/{}-X-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
            joblib.dump(F[fs.get_support()],      './dist/data/tf-idf/{}/{}-F-{}-mi.pkl'.format(tfidfcfgSTR, name, tag))
            fs2 = feature_selection.SelectKBest(feature_selection.chi2, k=500).fit(X, Y)
            joblib.dump(fs2.transform(X),         './dist/data/tf-idf/{}/{}-X-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))
            joblib.dump(F[fs2.get_support()],     './dist/data/tf-idf/{}/{}-F-{}-chi2.pkl'.format(tfidfcfgSTR, name, tag))
        joblib.dump(X,                            './dist/data/tf-idf/{}/{}-X.pkl'.format(tfidfcfgSTR, name))
        joblib.dump(F,                            './dist/data/tf-idf/{}/{}-F.pkl'.format(tfidfcfgSTR, name))

    savetfidf(X,  corpus.labels_, F,  'nltk')
    #savetfidf(X2, corpus.labels,  F2, 'sklearn')


writetopfeatureblock('lemma', ['title', 'code'], [3, 2]) # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
writetopfeatureblock('lemma', ['title', 'body'], [3, 2])
writetopfeatureblock('lemma', ['code', 'body'], [3, 2])