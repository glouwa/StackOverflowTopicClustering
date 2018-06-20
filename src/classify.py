import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy.random import RandomState
from sklearn.externals import joblib
import pandas as pd

from src.algo import plots 
from src.algo.pipelines.cls import classify_pre_pipeline
from src.algo.pipelines.cls import classify_pipelines
from src.algo.pipelines.clu import clustervis_pipelines, cluster_pipelines
from src.algo import frames

from ipywidgets import FloatProgress
from IPython.display import display

import warnings
warnings.filterwarnings('ignore')

def classifyAndPlotScore(f, ax, idx, title, X, Y):    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.1, random_state=0)            
    classify_pre_pipeline.fit(X_train, Y_train)
    X_train_ = classify_pre_pipeline.transform(X_train) 
    X_test_ = classify_pre_pipeline.transform(X_test)         
    ax.set_title(title)
    for label, pipeline in classify_pipelines.items():        
        pipeline.fit(X_train_, Y_train)
        Y_pred = pipeline.predict(X_test_)
        if hasattr(pipeline, 'decision_function'):
            Z = pipeline.decision_function(X_test_)
        elif hasattr(pipeline, 'predict_proba'):
            Z = pipeline.predict_proba(X_test_)[:, 1]
        else:
            Z = Y_pred
        
        plots.precisionRecallPlot(ax, title, label, Y_test, Y_pred, Z)
        f.value += 1

def run(path, algo, nfeatures, tags):    
    f1 = plt.figure(figsize=(20, 10))            
    f = FloatProgress(min=0, max=len(tags)*len(classify_pipelines))
    display(f)    

    path_ = './dist/data/{}/'.format(path)
    X, Y, F, C = frames.load(path_, ['X', 'Y', 'F', 'C'])
    Xpd = pd.DataFrame(X, columns=F)
    Ydf = pd.DataFrame(Y, columns=C)    

    for idx, tag in enumerate(tags):                        
        pathfs = '{}/featureselect/{}/{}'.format(path_, algo, tag)        
        scores, assertY, assertF = frames.load(pathfs, ['Scores', 'assertY', 'assertF'])
        
        Yc = Ydf.loc[:, tag]
        np.testing.assert_array_equal(Yc, assertY)
        np.testing.assert_array_equal(F, assertF)

        scoreDf = pd.DataFrame({ 'terms':F, 'scores':scores })
        scoreSorted = scoreDf.sort_values(by=['scores'], ascending=False)        
        scoreSortedterms = scoreSorted['terms']        
        scoreSortedtermscut = scoreSortedterms[:nfeatures]                
        Xs = Xpd.loc[:, scoreSortedtermscut]

        ax = f1.add_subplot(2, 2, idx+1)        
        #fig.suptitle('clusterd ({})'.format(label))
        classifyAndPlotScore(f, ax, idx, tag, Xs, Yc)
        #f.value = idx+1

    f1.tight_layout()
    f1.savefig('img/classify.png')
    f1.show()

from sklearn import metrics
def classifyAndPlotScore2(f, ax, idx, title, X, Y, gf1, gP, gR):    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.1, random_state=0)            
    classify_pre_pipeline.fit(X_train, Y_train)
    X_train_ = classify_pre_pipeline.transform(X_train) 
    X_test_ = classify_pre_pipeline.transform(X_test)             
    for label, pipeline in classify_pipelines.items():        
        pipeline.fit(X_train_, Y_train)
        Y_pred = pipeline.predict(X_test_)
        if hasattr(pipeline, 'decision_function'):
            Z = pipeline.decision_function(X_test_)
        elif hasattr(pipeline, 'predict_proba'):
            Z = pipeline.predict_proba(X_test_)[:, 1]
        else:
            Z = Y_pred
        
        #plots.precisionRecallPlot(ax, title, label, Y_test, Y_pred, Z)
        f.value += 1

        f1 = metrics.f1_score(Y_test, Y_pred)
        pr = metrics.precision_score(Y_test, Y_pred)
        rc = metrics.recall_score(Y_test, Y_pred)
        
        gf1[label] = gf1.get(label, [])
        gP[label] = gP.get(label, [])
        gR[label] = gR.get(label, [])

        gf1[label].append(f1)
        gP[label].append(pr)
        gR[label].append(rc)

import os
import json
from .featureselect import savefeatures
from scipy import signal

def run2(path, algo, nfeatures):    
    f1 = plt.figure(figsize=(20, 40))            
    maxC = 200
    f = FloatProgress(min=0, max=maxC*len(classify_pipelines))
    display(f)    

    path_ = './dist/data/{}/'.format(path)
    X, Y, F, C = frames.load(path_, ['X', 'Y', 'F', 'C'])
    Xpd = pd.DataFrame(X, columns=F)
    Ydf = pd.DataFrame(Y, columns=C)    

    tpcs = []
    gf1 = {}
    gR = {}
    gP = {}
    
    for idx in range(0, maxC):        
        Yc = Ydf.iloc[:, idx]        
        tpc = int(np.count_nonzero(Yc))        
        tpcs.append(tpc)

    ax = f1.add_subplot(4, 1, 1)
    tpcs_as = list(reversed(np.argsort(tpcs)))
    ax.plot(range(0, maxC), [tpcs[i] for i in tpcs_as], label="class member count")
    ax.legend(loc=1)

    for idx in tpcs_as:
        pathfs = '{}featureselect/{}/{}'.format(path_, "chi2", C[idx])        
        if not os.path.exists(pathfs):            
            savefeatures(path_, pathfs+'/', C[idx], "chi2", 10000, 1000)        
        scores, assertY, assertF = frames.load(pathfs, ['Scores', 'assertY', 'assertF'])
        
        Yc = Ydf.iloc[:, idx]
        np.testing.assert_array_equal(Yc, assertY)
        np.testing.assert_array_equal(F, assertF)

        scoreDf = pd.DataFrame({ 'terms':F, 'scores':scores })
        scoreSorted = scoreDf.sort_values(by=['scores'], ascending=False)        
        scoreSortedterms = scoreSorted['terms']        
        scoreSortedtermscut = scoreSortedterms[:nfeatures]                
        Xs = Xpd.loc[:, scoreSortedtermscut]

        classifyAndPlotScore2(f, None, idx, C[idx], Xs, Yc, gf1, gP, gR)
        
        tpc = int(np.count_nonzero(Yc))        
        tpcs.append(tpc)
    
    resampled = 50

    ax = f1.add_subplot(4, 1, 2)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, resampled), signal.resample(gf1[algo], resampled), label=algo)
        ax.legend(loc=1)

    ax = f1.add_subplot(4, 1, 3)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, resampled), signal.resample(gP[algo], resampled), label=algo)
        ax.legend(loc=1)

    ax = f1.add_subplot(4, 1, 4)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, resampled), signal.resample(gR[algo], resampled), label=algo)
        ax.legend(loc=1)
    
    joblib.dump(tpcs_as, 'tpcs_as.pkl')
    joblib.dump(gf1, 'gf1.pkl')
    joblib.dump(gP, 'gP.pkl')
    joblib.dump(gR, 'gR.pkl')
    
    f1.tight_layout()
    f1.savefig('img/classify_fs.png')
    f1.show()    

def plot2():
    tpcs_as = joblib.load('tpcs_as.pkl')
    gf1 = joblib.load('gf1.pkl')
    gR = joblib.load('gP.pkl')
    gP = joblib.load('gR.pkl')

    maxC = 200
    f1 = plt.figure(figsize=(20, 40))  
    
    #ax = f1.add_subplot(4, 1, 1)    
    #ax.plot(range(0, maxC), [tpcs[i] for i in tpcs_as], label="class member count")
    #ax.legend(loc=1)

    resampled = 5

    filter = lambda arr: pd.rolling_mean(pd.DataFrame(arr), 50)
    #filter = lambda arr: signal.resample(arr, resampled)
    #filter = lambda arr: signal.savgol_filter(arr, 51, 2)
    #filter = lambda arr: arr
    #filter = lambda arr: signal.lfilter([1.0/50]*50, 1, arr)
    
    
    ax = f1.add_subplot(4, 1, 2)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, maxC), filter(gf1[algo]), label=algo)
        ax.legend(loc=1)

    ax = f1.add_subplot(4, 1, 3)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, maxC), filter(gP[algo]), label=algo)
        ax.legend(loc=1)

    ax = f1.add_subplot(4, 1, 4)
    for algo in classify_pipelines.keys():
        ax.plot(range(0, maxC), filter(gR[algo]), label=algo)
        ax.legend(loc=1)

    f1.tight_layout()
    f1.savefig('img/classify_fs.png')
    f1.show()    

if __name__ == "__main__":
    run('00_title_body', 'chi2', ['python', 'android', 'html', 'java']) #,, , 'python', 'php',  , 'javascript',  
