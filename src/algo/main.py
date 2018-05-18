import plots 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from tfidf import StackoverflowCorpus
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sparse2dense import DenseTransformer
from numpy.random import RandomState

from sklearn import feature_selection


from classify.pipelines import classify_pre_pipeline
from classify.pipelines import classify_pipelines
from cluster.pipelines import clustervis_pipelines, cluster_pipelines
figuresize = (18, 12)

def classify(ax, X_train, X_test, Y_train, Y_test):
    classify_pre_pipeline.fit(X_train, Y_train)
    X_train_ = classify_pre_pipeline.transform(X_train) 
    X_test_ = classify_pre_pipeline.transform(X_test)     
    print("X_train_", X_train_.shape)   
    for label, pipeline in classify_pipelines.items():    
        print("classifying", label)
        pipeline.fit(X_train_, Y_train)
        Y_pred = pipeline.predict(X_test_)
        if hasattr(pipeline, 'decision_function'):
            Z = pipeline.decision_function(X_test_)
        elif hasattr(pipeline, 'predict_proba'):
            Z = pipeline.predict_proba(X_test_)[:, 1]
        else:
            Z = Y_pred
        plots.precisionRecallPlot(ax, label, Y_test, Y_pred, Z)
 
def clustervis(fig, X, Y, F, T):
    p=1
    for label, pipeline in clustervis_pipelines.items():
        print("visualising", label)
        T[label] = {}
        T[label]['projected'] = pipeline.fit_transform(X)    
        T[label]['pipeline'] = pipeline
        T[label]['features'] = F
        ax = fig.add_subplot(2, 3, p, projection='3d')        
        #ax = fig.add_subplot(2, 3, p)
        p+=1
        plots.clustervis(ax, label, pipeline, T[label]['projected'], F, Y)        

def cluster(fig, X, T, F):
    p=1
    for label, pipeline in cluster_pipelines.items():        
        print("clustering", label)      
        if hasattr(pipeline, 'predict'):
            Y_pred = pipeline.fit(X).predict(X)
        else:
            Y_pred = pipeline.fit_predict(X)
        ax = fig.add_subplot(2, 3, p, projection='3d')        
        #ax = fig.add_subplot(2, 3, p)
        p+=1
        plots.clustervis(ax, label, T['pipeline'], T['projected'], T['features'], Y_pred)  

def classifyVisualizeCluster(X, Y, F, label, classifySubplot):
    X_ = X
    F_ = F
    #fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=500).fit(X, Y)
    #X_ = fs.transform(X)    
    #F_ = F[fs.get_support()]

    X_train, X_test, Y_train, Y_test = train_test_split(X_, Y, test_size=.3, random_state=0)
    print(X_train.shape, len(Y_train))
    print(classifySubplot)
    ax = f1.add_subplot(classifySubplot[0], classifySubplot[1], classifySubplot[2])
    ax.set_title(label)
    classify(ax, X_train, X_test, Y_train, Y_test)
    ax.legend(fontsize='xx-small', loc=3) #, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
    plt.tight_layout()
    f1.savefig('img/classify.png')

    fig = plt.figure(figsize=figuresize)
    fig.suptitle(label)
    T = {}
    clustervis(fig, X_, Y, F_, T)
    plt.tight_layout()
    fig.savefig('img/{}-clustervis.png'.format(label))
    plt.close(fig)

    fig = plt.figure(figsize=figuresize)
    fig.suptitle('clusterd ({})'.format(label))
    cluster(fig, X_, T['PCA'], F_)
    plt.tight_layout()
    fig.savefig('img/{}-cluster.png'.format(label))
    plt.close(fig)

""" load data """
wordtype = 'lemma'
topfeature = ['title']
tfidfcfg= [3, 2] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
print("\n")

""" we are better than sklearn """
X = np.matrix(corpus.w.T)
F = corpus.termssorted
print("nltk reduced", X.shape)

""" sklearn is also cool """
pipeline = Pipeline([
    ('vect', text.CountVectorizer(stop_words='english', min_df=8, max_df=.9, binary=False, ngram_range=(1, 2))),
    ('tfidf', text.TfidfTransformer(sublinear_tf=True)), # smooth_idf=True
    ('dense', DenseTransformer()),
])
X2 = pipeline.fit_transform(corpus.documentsstr)
F2 = pipeline.named_steps['vect'].get_feature_names()
print("sklearn reduced", X2.shape, len(F2))

def analyseOneTag(tag, idx):
    Y = corpus.labels_(tag) 
    Y2 = corpus.labels(tag) 
    assert(len(Y) == len(X))   
    assert(len(Y2) == len(X2))   
    print("{} Classifying '{}' or not, in {} {}".format(idx, tag, topfeature, wordtype))
    print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))
    classifyVisualizeCluster(X, Y, F, '{} nltk {}{}'.format(tag, tfidfcfg[0], tfidfcfg[1]), [4, 3, idx+1]) #43
    classifyVisualizeCluster(X2, Y2, F2, '{} sklearn'.format(tag), [4, 3, idx+1+6]) #6

f1 = plt.figure(figsize=figuresize)
plt.tight_layout()
for idx, tag in enumerate(['python', 'php', 'html', 'android', 'c#', 'sql']): #,, 
    analyseOneTag(tag, idx)

plt.show()