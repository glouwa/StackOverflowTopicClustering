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
"""
def run(tfidf, fsel, tags):    
    f1 = plt.figure(figsize=(20, 10))            
    f = FloatProgress(min=0, max=len(tags)*len(classify_pipelines))
    display(f)    
    for idx, tag in enumerate(tags):        
        X = joblib.load('./dist/data/tf-idf/{}/nltk-X-{}-{}.pkl'.format(tfidf, tag, fsel))      
        Y = joblib.load('./dist/data/tf-idf/{}/nltk-Y-{}.pkl'.format(tfidf, tag))

        ax = f1.add_subplot(2, 2, idx+1)        
        #fig.suptitle('clusterd ({})'.format(label))
        classifyAndPlotScore(f, ax, idx, '{} nltk {}'.format(tag, tfidf), X, Y)
        #f.value = idx+1

    f1.tight_layout()
    f1.savefig('img/classify.png')
    f1.show()    
"""
def run(path, algo, tags):    
    f1 = plt.figure(figsize=(20, 10))            
    f = FloatProgress(min=0, max=len(tags)*len(classify_pipelines))
    display(f)    
    for idx, tag in enumerate(tags):        
        X = joblib.load('./dist/data/{}/{}/{}/X.pkl'.format(path, tag, algo))        
        Y = joblib.load('./dist/data/{}/{}/{}/assertY.pkl'.format(path, tag, algo))

        ax = f1.add_subplot(2, 2, idx+1)        
        #fig.suptitle('clusterd ({})'.format(label))
        classifyAndPlotScore(f, ax, idx, tag, X, Y)
        #f.value = idx+1

    f1.tight_layout()
    f1.savefig('img/classify.png')
    f1.show()    

if __name__ == "__main__":
    run('00_title_body', 'chi2', ['python', 'android', 'html', 'java']) #,, , 'python', 'php',  , 'javascript',  

import plotly.plotly as py
import plotly.graph_objs as go
from src.algo import frames
from plotly import tools
import pandas as pd
def plotselection(path, tags, scorefunc):

    fig = tools.make_subplots(rows=len(tags), cols=1, subplot_titles=tuple(tags))

    for idx, tag in enumerate(tags):
        mask, indices, scores, pvalues = frames.load('./dist/data/'+path+'/'+tag+'/chi2', ['Mask', 'Indices', 'Scores', 'Pvalue'])
        F = joblib.load('./dist/data/{}/{}/{}/assertF.pkl'.format(path, tag, scorefunc))
        # assert assertY == Y aus tfidf
        # assert assertY == Y aus tfidf

        df = pd.DataFrame({
            'x':F,
            'y':scores
        })
        sorted = df.sort_values(by=['y'], ascending=False)

        trace1 = go.Bar(x=sorted.x, y=sorted.y)        
        fig.append_trace(trace1, idx+1, 1)
    
    fig['layout'].update(
        margin=dict(l=0, r=0, b=110, t=60),        
        title='top 20 tags for android chi2',        
        height=200*len(tags),
        yaxis1=dict(                        
            fixedrange=True
        ),        
        yaxis2=dict(                        
            fixedrange=True            
        ),
        yaxis3=dict(                        
            fixedrange=True
        ),
        xaxis1=dict(            
            #domain=[0, .01]            
            range=[-1, 50],
            tickfont=dict(          
                size=10,          
            ),
        ),
        xaxis2=dict(            
            #domain=[0, .01]            
            range=[-1, 50],
            tickfont=dict(          
                size=10,          
            ),
        ),
        xaxis3=dict(            
            #domain=[0, .01]            
            range=[-1, 50],
            tickfont=dict(          
                size=10,
            ),
        ),
    )
    return py.iplot(fig, filename='make-subplots-multiple-with-titles')    

    