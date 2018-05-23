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

import warnings
warnings.filterwarnings('ignore')

def classifyAndPlotScore(f, ax, idx, title, X, Y, F):    
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
        
        plots.precisionRecallPlot(ax, label, Y_test, Y_pred, Z)
        f.value += 1

def run(tfidf, fsel, tags):    
    f1 = plt.figure(figsize=(20, 10))            
    f = FloatProgress(min=0, max=len(tags)*len(classify_pipelines))
    display(f)    
    for idx, tag in enumerate(tags):        
        X = joblib.load('./dist/data/tf-idf/{}/nltk-X-{}-{}.pkl'.format(tfidf, tag, fsel))
        F = joblib.load('./dist/data/tf-idf/{}/nltk-F-{}-{}.pkl'.format(tfidf, tag, fsel))
        Y = joblib.load('./dist/data/tf-idf/{}/nltk-Y-{}.pkl'.format(tfidf, tag))

        ax = f1.add_subplot(2, 2, idx+1)        
        #fig.suptitle('clusterd ({})'.format(label))
        classifyAndPlotScore(f, ax, idx, '{} nltk {}'.format(tag, tfidf), X, Y, F)
        #f.value = idx+1

    f1.tight_layout()
    f1.savefig('img/classify.png')
    f1.show()    

if __name__ == "__main__":
    run('00_title_body', 'chi2', ['python', 'android', 'html', 'sql']) #,, , 'python', 'php',  , 'javascript',  
