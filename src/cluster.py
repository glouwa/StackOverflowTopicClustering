import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy.random import RandomState
from sklearn.externals import joblib
from sklearn import metrics

from src.algo import plots 
from src.algo.pipelines.cls import classify_pre_pipeline
from src.algo.pipelines.cls import classify_pipelines
from src.algo.pipelines.clu import clustervis_pipelines, cluster_pipelines, cluster_pipelines2
from src.algo import frames

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

def cluster(path, decompositions, dimensions, algos, clustercounts):
    runcount = len(decompositions) * len(dimensions) * len(algos) * len(clustercounts)
    f = FloatProgress(min=0, max=runcount)
    display(f)     
    for composition in decompositions:
        path_composition = './dist/data/' + path + 'decomposition/' + composition + '/'
        for dimension in dimensions:
            path_dimension = path_composition + str(dimension) + '/'
            P = joblib.load(path_dimension + 'P.pkl')
            for algo in algos:
                path_algo = path_dimension + algo + '/'
                for clustercount in clustercounts:
                    path_algo_clustercount = path_algo + str(clustercount) + '/'

                    clu_pipelines = cluster_pipelines2(clustercount)
                    pipeline = clu_pipelines[algo]
                    if hasattr(pipeline, 'predict'):
                        Y_pred = pipeline.fit(P).predict(P)
                    else:
                        Y_pred = pipeline.fit_predict(P)

                    frames.save(path_algo_clustercount, 'Y_pred', Y_pred)                    
                    f.value += 1

def clusterScore(path, decompositions, dimensions, algos, clustercounts, tag):
    runcount = len(decompositions) * len(dimensions) * len(algos) * len(clustercounts)
    f = FloatProgress(min=0, max=runcount)
    display(f)     

    Yall, C = frames.load('./dist/data/' + path, ['Y', 'C'])    
    Y = Yall[:, C.tolist().index(tag)]
    print(Y.shape)
    f1_bestcluster = 0
    best_dim = 0
    best_algo = ''
    best_clustercount = 0

    for composition in decompositions:
        path_composition = './dist/data/' + path + 'decomposition/' + composition + '/'
        for dimension in dimensions:
            path_dimension = path_composition + str(dimension) + '/'
            for algo in algos:
                path_algo = path_dimension + algo + '/'
                for clustercount in clustercounts:
                    path_algo_clustercount = path_algo + str(clustercount) + '/'

                    Y_pred = joblib.load(path_algo_clustercount + 'Y_pred.pkl')                                        

                    for clusternr in range(clustercount):
                        Y_pred_tag_01 = Y_pred == clusternr                        
                        f1_currentcluster = metrics.f1_score(Y, Y_pred_tag_01)
                        
                        if f1_currentcluster > f1_bestcluster:
                            f1_bestcluster = f1_currentcluster
                            best_dim = dimension
                            best_algo = algo
                            best_clustercount = clustercount
                    
                    f.value += 1
        print(composition, best_dim, best_algo, best_clustercount, f1_bestcluster)
        f1_bestcluster = 0        

def run(path, decompskeys, algokeys, samples, numclusters, interdim, tag):
    f = FloatProgress(min=0, max=len(cluster_pipelines(0, 0, 'PCA'))) 
    display(f) 

    path = './dist/data/' + path    
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
    x, y, z = np.random.multivariate_normal(np.array([0,3,0]), np.eye(3), 400).transpose()
    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=marker
    )

    x2, y2, z2 = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 100).transpose()
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
