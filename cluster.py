import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy.random import RandomState
from sklearn.externals import joblib

from src.algo import plots 
from src.algo.pipelines.cls import classify_pre_pipeline
from src.algo.pipelines.cls import classify_pipelines
from src.algo.pipelines.clu import clustervis_pipelines, cluster_pipelines

from ipywidgets import FloatProgress
from IPython.display import display

cols = 6
rows = 4
def createProjectionsAndShowTruth(fig, X, Y, F, T):    
    clu_pipelines = clustervis_pipelines(3)
    for pojidx, label in enumerate(clu_pipelines.keys()):        
        pipeline = clu_pipelines[label]
        T[label] = {}
        T[label]['projected'] = pipeline.fit_transform(X)    
        T[label]['pipeline'] = pipeline
        T[label]['features'] = F     

        ax = fig.add_subplot(rows, cols, pojidx*cols+1)        #, projection='3d'           
        ax.set_title(label, loc='left')
        #fig.suptitle('clusterd ({})'.format(label))
        plots.clustervisTrue(ax, label, pipeline, T[label]['projected'], F, Y)        

def runClusterAlgosAndPlotForEachProjection(f, fig, X, Ts, F):        
    for algoidx, label in enumerate(cluster_pipelines(0, 0, 'PCA').keys()):
        for pidx, p in enumerate(clustervis_pipelines(0).keys()):
            clu_pipelines = cluster_pipelines(5, 4 if label == 'DBScan' else 25, p)
            pipeline = clu_pipelines[label]
            if hasattr(pipeline, 'predict'):
                Y_pred = pipeline.fit(X).predict(X)
            else:
                Y_pred = pipeline.fit_predict(X)   

            ax = fig.add_subplot(rows, cols, pidx*cols+algoidx+2) # projection='3d'    
            if pidx == 0:
                ax.set_title(label)
            #fig.suptitle(label)    
            plots.clustervis(ax, label, Ts[p]['pipeline'], Ts[p]['projected'], Ts[p]['features'], Y_pred)  
        f.value += 1


def run(tag):        
    f = FloatProgress(min=0, max=len(cluster_pipelines(0, 0, 'PCA'))) 
    display(f) 

    samples = 2000                
    tfidf = "11_title"
    X = joblib.load('./dist/data/tf-idf/{}/nltk-X.pkl'.format(tfidf))
    F = joblib.load('./dist/data/tf-idf/{}/nltk-F.pkl'.format(tfidf))
    Y = joblib.load('./dist/data/tf-idf/{}/nltk-Y-{}.pkl'.format(tfidf, tag))
    Ts = {}    
    
    fig = plt.figure(figsize=(20, 14))   
    
    _, X_test, _, Y_test = train_test_split(X, Y, test_size=.3, random_state=0)        
    createProjectionsAndShowTruth(fig, X_test[:samples], Y_test[:samples], F, Ts)    
    runClusterAlgosAndPlotForEachProjection(f, fig, X_test[:samples], Ts, F)
    
    plt.tight_layout()
    fig.savefig('img/{}-cluster.png'.format('proj x clu'))
    fig.show()    

if __name__ == "__main__":    
    run('android')    

"""

import time

max_count = 100



count = 0
while count <= max_count:
    f.value += 1 # signal to increment the progress bar
    time.sleep(.1)
    count += 1
"""
