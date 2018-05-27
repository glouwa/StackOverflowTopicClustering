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

def run(path, algo, nfeatures, tags):    
    f1 = plt.figure(figsize=(20, 10))            
    f = FloatProgress(min=0, max=len(tags)*len(classify_pipelines))
    display(f)    
    path_ = './dist/data/{}/'.format(path)
    X, Y, F, C = frames.load(path_, ['X', 'Y', 'F', 'C'])
    Xpd = pd.DataFrame(X, columns=F)
    Ydf = pd.DataFrame(Y, columns=C)    

    for idx, tag in enumerate(tags):                        
        pathfs = '{}/{}/{}/'.format(path_, tag, algo)        
        scores, pvalues, assertY, assertF = frames.load(pathfs, ['Scores', 'Pvalue', 'assertY', 'assertF'])
        
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

if __name__ == "__main__":
    run('00_title_body', 'chi2', ['python', 'android', 'html', 'java']) #,, , 'python', 'php',  , 'javascript',  

import plotly.plotly as py
import plotly.graph_objs as go
from src.algo import frames
from plotly import tools
import pandas as pd
def plotTopFeatures(path, scorefunc, tags):

    fig = tools.make_subplots(rows=1, cols=len(tags), horizontal_spacing=0.1)
    #horizontal_spacing=0.05,vertical_spacing=0.1, shared_yaxes=True

    for idx, tag in enumerate(tags):
        #path_ = './dist/data/'+path+'/'+tag+'/'+scorefunc
        path_ = './dist/data/{}/{}/{}/'.format(path, tag, scorefunc)
        F, Y, scores, pvalues = frames.load(path_, ['assertF', 'assertY', 'Scores', 'Pvalue'])
        # assert assertY == Y aus tfidf
        # assert assertY == Y aus tfidf

        classmembercount = int(np.count_nonzero(Y))
        samples = int(len(Y)/1000)

        df = pd.DataFrame({ 'x':F, 'y':scores })
        sorted = df.sort_values(by=['y'], ascending=False)

        trace1 = go.Bar(
            name = '{} <sub>{} / {}K</sub>'.format(tag, classmembercount, samples),
            x=sorted.y, 
            y=sorted.x,
            orientation = 'h',            
            #xaxis = "x2",
            #yaxis ="y3",
        )        
        fig.append_trace(trace1, 1, idx+1)
    
    def fixedrange(): 
        return dict(                        
            fixedrange=True
        )

    def top20(): 
        return dict(            
            #autorange='reversed',
            #domain=['true', 'android'],
            range=[50, -1],               
            tickfont=dict(size=10)
        )

    fig['layout'].update(
        #margin=dict(l=0, r=0, b=110, t=60),        
        title='Top 50 terms sorted by '+ scorefunc +' score',
        legend=dict(orientation="h", x=.07, y=1.07),
        height=800,        
        xaxis1=fixedrange(),   
        xaxis2=fixedrange(),
        xaxis3=fixedrange(),        
        xaxis4=fixedrange(), 
        xaxis5=fixedrange(), 
        xaxis6=fixedrange(), 
        
        yaxis1=top20(),
        yaxis2=top20(),
        yaxis3=top20(),
        yaxis4=top20(),
        yaxis5=top20(),
        yaxis6=top20(),
    )
    return py.iplot(fig, filename='make-subplots-multiple-with-titles')    

    