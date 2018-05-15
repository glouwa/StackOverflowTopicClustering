import plots 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from tfidf import StackoverflowCorpus
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sparse2dense import DenseTransformer
from pprint import pprint
from numpy.random import RandomState

from sklearn import decomposition
from sklearn import preprocessing
from sklearn import feature_selection
from sklearn import svm

from classify.pipelines import classify_pipelines
from cluster.pipelines import clustervis_pipelines, cluster_pipelines

""" load data """
theoneandonlyclass = 'python'
wordtype = 'raw'
topfeature = 'title'
tfidfcfg= [1, 1] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
Y = corpus.labels(theoneandonlyclass)
print("Corpus", len(corpus.documents), len(corpus.termssorted))
print("Classifying {} or not, in {} {}".format(theoneandonlyclass, topfeature, wordtype))
print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))

def classify(ax, X_train, X_test, Y_train, Y_test):
    for label, pipeline in classify_pipelines.items():    
        print("classifying", label)
        pipeline.fit(X_train, Y_train)
        Y_pred = pipeline.predict(X_test)
        if hasattr(pipeline, 'decision_function'):
            Z = pipeline.decision_function(X_test)            
        elif hasattr(pipeline, 'predict_proba'):
            Z = pipeline.predict_proba(X_test)[:, 1]
        else:
            Z = Y_pred
        plots.precisionRecallPlot(ax, label, Y_test, Y_pred, Z)
 
def clustervis(fig, X, F, T):
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
        pipeline.fit(X)
        Y_pred = pipeline.predict(X)
        ax = fig.add_subplot(2, 3, p, projection='3d')        
        #ax = fig.add_subplot(2, 3, p)
        p+=1
        plots.clustervis(ax, label, T['pipeline'], T['projected'], T['features'], Y_pred)  

def classifyVisualizeCluster(X, F, label, classifySubplot):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3, random_state=0)
    print(X_train.shape, len(Y_train))
    ax = f1.add_subplot(classifySubplot)
    ax.set_title(label)
    classify(ax, X_train, X_test, Y_train, Y_test)
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
    plt.tight_layout()

    fig = plt.figure()
    fig.suptitle(label)
    T = {}
    clustervis(fig, X, F, T)
    plt.tight_layout()

    fig = plt.figure()
    fig.suptitle('clusterd ({})'.format(label))
    cluster(fig, X, T['PCA'], F)
    plt.tight_layout()

f1 = plt.figure()
""" we are better than sklearn """
X = np.matrix(corpus.w.T)
F = corpus.termssorted
print("nltk reduced", X.shape)
classifyVisualizeCluster(X, F, 'nltk preprocessing {}{}'.format(tfidfcfg[0], tfidfcfg[1]), 211)

""" sklearn is also cool """
pipeline = Pipeline([
    ('vect', text.CountVectorizer(stop_words='english', min_df=5, max_df=1.0, binary=False)),
    ('tfidf', text.TfidfTransformer(sublinear_tf=True)),
    ('dense', DenseTransformer()),
])
X2 = pipeline.fit_transform(corpus.documentsstr)
F2 = pipeline.named_steps['vect'].get_feature_names()
print("sklearn reduced", X2.shape, len(F2))
classifyVisualizeCluster(X2, F2, 'sklearn preprocessing', 212)

plt.show()