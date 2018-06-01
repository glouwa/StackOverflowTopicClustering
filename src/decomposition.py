import numpy as np
from sklearn.externals import joblib
from src.algo.pipelines.clu import clustervis_pipelines

from ipywidgets import FloatProgress
from IPython.display import display

from src.algo import frames

def DecompositionFrame():
    return frames.DecompositionFrame()

def createDecompositions(frame):
    f = FloatProgress(min=0, max=frame.shape[0]) 
    display(f) 

    def savefeatures(srcpath, destpath, algo, dim):    
        #X, Y, F = joblib.load(srcpath, 'X', 'Y','F') 
        X = joblib.load(srcpath+'X.pkl')
        F = joblib.load(srcpath+'F.pkl')
        Y = joblib.load(srcpath+'Y.pkl')
        C = joblib.load(srcpath+'C.pkl')

        frames.save(destpath, 'assertF', F)
    
        clu_pipelines = clustervis_pipelines(int(dim))
        pipeline = clu_pipelines[algo]        
        P = pipeline.fit_transform(X)    
        COMP = pipeline.named_steps['clu'].components_
        
        frames.save(destpath, 'P', P)
        frames.save(destpath, 'COMP', COMP)

    for task in frame.index.values:
        f.value += 1
        tfidfpos = frame.index.names.index('tf-idf')+1
        destpath = './dist/data/'+'/'.join(task)+'/'        
        srcpath = './dist/data/'+'/'.join(task[:tfidfpos])+'/'
        
        algo = task[frame.index.names.index('algo')]    
        dim = task[frame.index.names.index('dim')]
        savefeatures(srcpath, destpath, algo, dim)        

    return frames.cell2string.file2shape(frame)    


import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import pandas as pd
from src.algo import frames
#def plotTopFeatures(path, scorefunc, tags):
def plotComponents(path, algo, dim, crange):
    
    F = joblib.load('./dist/data/'+path+'/F.pkl')    
    path_ = './dist/data/{}/decomposition/{}/{}'.format(path, algo, dim)
    P, C, Fassert = frames.load(path_, ['P', 'COMP', 'assertF'])
    np.testing.assert_array_equal(F, Fassert)
    
    componentsrange = list(range(*crange))
    print(componentsrange)

    fig = tools.make_subplots(rows=1, cols=len(componentsrange), horizontal_spacing=0.1)
    #horizontal_spacing=0.05,vertical_spacing=0.1, shared_yaxes=True

    for gidx, cidx in enumerate(componentsrange):
        c = C[cidx]        
        df = pd.DataFrame({ 'x':F, 'y':c })
        sorted = df.sort_values(by=['y'], ascending=False)

        trace1 = go.Bar(            
            x=sorted.y, 
            y=sorted.x,
            orientation = 'h',            
            #xaxis = "x2",
            #yaxis ="y3",
        )        
        fig.append_trace(trace1, 1, gidx+1)
        fig['layout']['xaxis{}'.format(gidx+1)].update(fixedrange=True)
        fig['layout']['yaxis{}'.format(gidx+1)].update(range=[50, -1], tickfont=dict(size=10))
    
    fig['layout'].update(
        #margin=dict(l=0, r=0, b=110, t=60),        
        title='Top 50 component term weights '+ 'algo' +' score',
        showlegend=False,
        height=800
    )    
    return py.iplot(fig, filename='top-components')    