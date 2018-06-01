import numpy as np
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib
from sklearn import model_selection
from ipywidgets import FloatProgress
from IPython.display import display
from src.algo import frames

def featuretranform(srcpath, destpath, algo, X, Y, k):
    if algo == 'chi2':
        fs = feature_selection.SelectKBest(feature_selection.chi2, k=k).fit(X, Y)    
    elif algo == 'f_classif':
        fs = feature_selection.SelectKBest(feature_selection.f_classif, k=k).fit(X, Y)    
    elif algo == 'mutual_info_classif':
        fs = feature_selection.SelectKBest(feature_selection.mutual_info_classif, k=k).fit(X, Y)
    else:
        assert(False)

    return fs.get_support(), fs.get_support(indices=True), fs.scores_, fs.pvalues_

def savefeatures(srcpath, destpath, tag, algo, nsamples, k):    
    #X, Y, F = joblib.load(srcpath, 'X', 'Y','F') 
    X = joblib.load(srcpath+'X.pkl')
    F = joblib.load(srcpath+'F.pkl')
    Y = joblib.load(srcpath+'Y.pkl')
    C = joblib.load(srcpath+'C.pkl')

    tagidx = list(C).index(tag)    
    Yc = Y[:, tagidx]

    frames.save(destpath, 'assertF', F)
    frames.save(destpath, 'assertY', Yc)

    X_train, _, Y_train, _ = model_selection.train_test_split(X, Yc, test_size=0, random_state=0)            
    fselsamples = nsamples
    X_ = X_train[:fselsamples]
    Y_ = Y_train[:fselsamples]
    assert(len(X_) > 500)
    
    mask, indices, scores, pvalues = featuretranform(srcpath, destpath, algo, X_, Y_, k)
        
    #frames.save(destpath, 'X',       X[:, mask])
    frames.save(destpath, 'Mask',    mask)
    frames.save(destpath, 'Indices', indices)    
    frames.save(destpath, 'Scores',  scores)
    frames.save(destpath, 'Pvalue',  pvalues)    

def FeatureFrame():
    return frames.FeatureFrame()

def run(frame, nsamples, k):    
    f = FloatProgress(min=0, max=frame.shape[0])
    display(f) 
    
    for task in frame.index.values:
        f.value += 1
        tfidfpos = frame.index.names.index('tf-idf')+1
        destpath = './dist/data/'+'/'.join(task)+'/'        
        srcpath = './dist/data/'+'/'.join(task[:tfidfpos])+'/'
        
        algo = task[frame.index.names.index('scorefunc')]    
        tag = task[frame.index.names.index('class')]
        savefeatures(srcpath, destpath, tag, algo, nsamples, k)        

    return frames.cell2string.file2shape(frame)    
    

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
        path_ = './dist/data/{}/featureselect/{}/{}'.format(path, scorefunc, tag)
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
    return py.iplot(fig, filename='top-features')    

    