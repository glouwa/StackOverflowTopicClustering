import numpy as np
import pandas as pd    
import plotly.plotly as py
import plotly.graph_objs as go
from src.algo.tfidf import StackoverflowCorpus
from src.algo.tools.sparse2dense import DenseTransformer
from sklearn import feature_selection
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sklearn.externals import joblib
from sklearn import model_selection
import os, time
from src.algo import frames
      
def calcTfIdf(wordtype, topfeature, tfidfcfg, mindf, mintf):    
    corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, 
        topfeature, tfidfcfg[0], tfidfcfg[1], mindf, mintf)
    
    X = np.matrix(corpus.w.T)
    R = np.matrix(corpus.doctermRaw.T)
    F = corpus.termssorted    
    IDF = corpus.idf
    TDOC = corpus.doctermMax
    Y = []
    Cdict = corpus.getClasses() #['python', 'php', 'html', 'android', 'javascript', 'sql'] 
    tags = pd.DataFrame({ 
        'tags': list(Cdict.keys()), 
        'counts': list(Cdict.values()) 
    })
    sorted = tags.sort_values(by=['counts'], ascending=False)    
    C_ = sorted.loc[:,'tags']    
    C = C_[:200]
    for tag in C:         
        Y.append(corpus.labels_(tag))
    return X, R, F, IDF, TDOC, np.array(Y).T, np.array(C)

def writetopfeatureblock(outpath, wordtype, vecimpl, topfeature, tfidfcfg, mindf, mintf):    
    X, R, F, IDF, TDOC, Y, C = calcTfIdf(wordtype, topfeature, tfidfcfg, mindf, mintf)
    directory = './dist/data/'+outpath+'/'        
    frames.save(directory, "X", X)
    frames.save(directory+'../', "R", R)
    frames.save(directory, "F", F)
    frames.save(directory, "IDF", IDF)
    frames.save(directory, "TDOC", TDOC)
    frames.save(directory, 'Y', Y)
    frames.save(directory, 'C', C)
    return X, R, F, Y, C

def run(frame):    
    print("select", frame.shape)
    #print("select.index", frame.index.shape)
    #print("select.index", frame.index.values)
    
    minDfTfMap = {
        'T':    (2,10),    
        'TI':   (2,10),
        'TIB':  (5,25),
        'TIC':  (5,25),
        'TIBC': (7,50),
        'TB':   (5,25),
        'TC':   (5,25),
        'TBC':  (7,50), 
    }
    htmlfeatureMap = {
        'T':    ['title'], 
        'TI':   ['title', 'inlinecode'],                
        'TIB':  ['title', 'inlinecode', 'body'],        
        'TIC':  ['title', 'inlinecode', 'code'],
        'TIBC': ['title', 'inlinecode', 'body', 'code'],
        'TB':   ['title', 'body'],
        'TC':   ['title', 'code'],        
        'TBC':  ['title', 'body', 'code']
    }
    #tfidfMap = lambda str: map(list(str), lambda e: int(e))
    tfidfMap = {
        '32': [3,2],
        '31': [3,1],
        '30': [3,0],
        '11': [1,1],
        '00': [0,0],
        '10': [1,0],
        '01': [0,1]
    }
    for task in frame.index.values:
        #print("path", '/'.join(task))
        wordtype = task[1] 
        vecimpl = task[2] 
        tfidfcfg = tfidfMap[task[4]]
        topfeature = htmlfeatureMap[task[3]]        
        mindf = minDfTfMap[task[3]][0]
        mintf = minDfTfMap[task[3]][1]
        X, R, F, Y, C = writetopfeatureblock('/'.join(task), wordtype, vecimpl, topfeature, tfidfcfg, mindf, mintf) 
        frame.loc[task,'R'] = str(R.shape)
        frame.loc[task,'X'] = str(X.shape)
        frame.loc[task,'F'] = str(F.shape)
        frame.loc[task,'Y'] = str(Y.shape)
        frame.loc[task,'C'] = str(C.shape)
        frame.loc[task,'s'] = str(X.shape[0])
        frame.loc[task,'f'] = str(X.shape[1])        
        frame.loc[task,'c'] = str(C.shape[0])

    #print("done")
    return frame

def WordVecFrame():
    return frames.WordVecFrame()

if __name__ == "__main__":      
    s = (slice('stackoverflow'), slice('lemma'), slice('nltk'), slice('00', '32'), slice('T', 'TB'))    
    s = plan(s)
    run(s)

def NlpVecPanda(path):
    C = joblib.load(path+'C.pkl')    
    X = joblib.load(path+'X.pkl')    
    F = joblib.load(path+'F.pkl')
    IDF = joblib.load(path+'IDF.pkl')    
    docsize = np.sum(X, axis=1).tolist()    
    return pd.DataFrame(X, index=pd.Index(docsize), columns=IDF).sort_index(axis=1).sort_index(axis=0)
    
def plot(path):    
    tfidf = NlpVecPanda('./dist/data/'+path+'/')
    data = [
        go.Surface(
            z= tfidf[::40].as_matrix(), # dfXX[:300],
            showscale= False,
            colorscale= [
                # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
                [0, 'gba(1, 1, 1)'],
                [0.1, 'rgb(1, 1, 1)'],

                # Let values between 10-20% of the min and max of z
                # have color rgb(20, 20, 20)
                [0.1, 'rgb(0, 1, 0)'],
                [0.4, 'rgb(0, 1, 0)'],

                # Values between 20-30% of the min and max of z
                # have color rgb(40, 40, 40)                
                [0.4, 'rgb(80, 80, 80)'],
                [0.5, 'rgb(80, 80, 80)'],

                [0.5, 'rgb(100, 100, 100)'],
                [0.6, 'rgb(100, 100, 100)'],

                [0.6, 'rgb(120, 120, 120)'],
                [0.7, 'rgb(120, 120, 120)'],

                [0.7, 'rgb(140, 140, 140)'],
                [0.8, 'rgb(140, 140, 140)'],

                [0.8, 'rgb(255, 0, 0)'],
                [0.9, 'rgb(255, 0, 0)'],

                [0.9, 'rgb(.0, .0, .0)'],
                [1.0, 'rgb(1, .0, .0)']
            ],
        )
    ]
    layout = go.Layout(
        title='Mt Bruno Elevation',        
        autosize=True,                
        margin=dict(
            l=5,
            r=0,
            b=0,
            t=0
        ),
        scene=dict(            
            aspectratio = dict( x=1.7, y=1, z=0.2 ),
            aspectmode = 'manual'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return py.iplot(fig, filename='elevations-3d-surface')
