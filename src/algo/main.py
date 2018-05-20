import plots 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy.random import RandomState

from classify.pipelines import classify_pre_pipeline
from classify.pipelines import classify_pipelines
from cluster.pipelines import clustervis_pipelines, cluster_pipelines

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
from sklearn import utils

def classifyVisualizeCluster(X, Y, F, label, classifySubplot):
    X_ = X
    Y_ = Y
    F_ = F
    X_train, X_test, Y_train, Y_test = train_test_split(X_, Y_, test_size=.3, random_state=0)
    print(X_train.shape, len(Y_train))
    print(classifySubplot)
    ax = f1.add_subplot(classifySubplot[0], classifySubplot[1], classifySubplot[2])
    ax.set_title(label)
    classify(ax, X_train, X_test, Y_train, Y_test)
    ax.legend(fontsize='xx-small', loc=3) #, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
    plt.tight_layout()
    f1.savefig('img/classify.png')

    """
    fig = plt.figure(figsize=figuresize)
    fig.suptitle(label)
    T = {}
    clustervis(fig, X_test, Y_test, F_, T)
    plt.tight_layout()
    fig.savefig('img/{}-clustervis.png'.format(label))
    plt.close(fig)

    fig = plt.figure(figsize=figuresize)
    fig.suptitle('clusterd ({})'.format(label))
    cluster(fig, X_test, T['PCA'], F_)
    plt.tight_layout()
    fig.savefig('img/{}-cluster.png'.format(label))
    plt.close(fig)
    """

from sklearn.externals import joblib
tags = ['python', 'php', 'html', 'android', 'javascript', 'sql']

figuresize = (18, 12)
def analyseOneTag(tag, idx):
    #Y = corpus.labels_(tag) 
    #Y2 = corpus.labels(tag) 
    #assert(len(Y) == len(X))   
    #assert(len(Y2) == len(X2))   
    #print("{} Classifying '{}' or not, in {} {}".format(idx, tag, topfeature, wordtype))
    #print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))
    tfidf = "32_code_body"
    fsel = "chi2"
    X = joblib.load('./dist/data/tf-idf/{}/nltk-X-{}-{}.pkl'.format(tfidf, tag, fsel))
    F = joblib.load('./dist/data/tf-idf/{}/nltk-F-{}-{}.pkl'.format(tfidf, tag, fsel))
    Y = joblib.load('./dist/data/tf-idf/{}/nltk-Y-{}.pkl'.format(tfidf, tag))
    classifyVisualizeCluster(X, Y, F, '{} nltk {}'.format(tag, tfidf), [4, 3, idx+1]) #43
    #classifyVisualizeCluster(X2, Y2, F2, '{} sklearn'.format(tag), [4, 3, idx+1+6]) #6

f1 = plt.figure(figsize=figuresize)
plt.tight_layout()
for idx, tag in enumerate(['python', 'php', 'html', 'android', 'javascript', 'sql']): #,, , 
    analyseOneTag(tag, idx)

plt.show()
