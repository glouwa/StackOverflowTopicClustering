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

cols = 5
rows = 4
def createProjectionsAndShowTruth(fig, X, Y, F, T):    
    clu_pipelines = clustervis_pipelines(5)
    for pojidx, label in enumerate(clu_pipelines.keys()):        
        pipeline = clu_pipelines[label]
        T[label] = {}
        T[label]['projected'] = pipeline.fit_transform(X)    
        T[label]['pipeline'] = pipeline
        T[label]['features'] = F     

        ax = fig.add_subplot(rows, cols, pojidx*cols+1)        #, projection='3d'           
        ax.set_title(label, loc='left')        
        plots.clustervisTrue(ax, label, pipeline, T[label]['projected'], F, Y)        

def runClusterAlgosAndPlotForEachProjection(f, fig, X, Ts, F, numclusters, interdim):        
    for algoidx, label in enumerate(cluster_pipelines(0, 0, 'PCA').keys()):
        for pidx, p in enumerate(clustervis_pipelines(0).keys()):
            clu_pipelines = cluster_pipelines(numclusters, 4 if label == 'DBScan' else interdim, p)
            pipeline = clu_pipelines[label]
            if hasattr(pipeline, 'predict'):
                Y_pred = pipeline.fit(X).predict(X)
            else:
                Y_pred = pipeline.fit_predict(X)   

            ax = fig.add_subplot(rows, cols, pidx*cols+algoidx+2) # projection='3d'    
            if pidx == 0:
                ax.set_title(label)            
            plots.clustervis(ax, label, Ts[p]['pipeline'], Ts[p]['projected'], Ts[p]['features'], Y_pred)  
        f.value += 1

from src.algo import frames
def DecompositionFrame():
    return frames.DecompositionFrame()

def run2(frame):
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
    return py.iplot(fig, filename='make-subplots-multiple-with-titles')    

def run(path, decompskeys, algokeys, samples, numclusters, interdim, tag):
    f = FloatProgress(min=0, max=len(cluster_pipelines(0, 0, 'PCA'))) 
    display(f) 

    path = './dist/data/'+path    
    C = joblib.load(path+'C.pkl')    
    X = joblib.load(path+'X.pkl')
    F = joblib.load(path+'F.pkl')
    Y = joblib.load(path+'Y.pkl')[:,list(C).index(tag)]
    Ts = {}    
    print(X.shape, Y.shape, F.shape)
    
    fig = plt.figure(figsize=(20, 16))   
    
    _, X_test, _, Y_test = train_test_split(X, Y, test_size=.3, random_state=0)        
    createProjectionsAndShowTruth(fig, X_test[:samples], Y_test[:samples], F, Ts)    
    runClusterAlgosAndPlotForEachProjection(f, fig, X_test[:samples], Ts, F, numclusters, interdim)
    
    plt.tight_layout()
    fig.savefig('img/{}-cluster.png'.format('proj x clu'))
    fig.show()    

def runPlotly(tfidf, decompskeys, algokeys, samples, tag):    
    import plotly.plotly as py
    import plotly.graph_objs as go
    import numpy as np

    marker=dict(
        size=5,        
        opacity=0.99
    )
    x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=marker
    )

    x2, y2, z2 = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 50).transpose()
    marker.update(dict(color='red'))
    trace2 = go.Scatter3d(
        x=x2,
        y=y2,
        z=z2,
        mode='markers',
        marker=marker
    )
    data = [trace1, trace2]
    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        autosize=False,    
        height=500,
    )
    fig = go.Figure(data=data, layout=layout)
    return py.iplot(fig, filename='simple-3d-scatter')

if __name__ == "__main__":    
    run('stackoverflow/lemma/nltk/11/TB/', ['PCA', 'NMF', 'LDA', 'SVD'], ['Ward', 'K-Means', 'GMM', 'DBScan'], 2000, 'android')    
