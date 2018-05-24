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

def save(name, M, D):
        if not os.path.exists(D):
            os.makedirs(D)       
            print("makedir", D)        
        filename = D + '{}.pkl'.format(name)
        joblib.dump(M, filename)  
        #print(filename)

def loadCounter(wordtype, topfeature, tfidfcfg, mindf, mintf):    
    #print("nltk", wordtype, topfeature, tfidfcfg, mindf, mintf)
    corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, 
        topfeature, tfidfcfg[0], tfidfcfg[1], mindf, mintf)
    
    X = np.matrix(corpus.w.T)
    XR = np.matrix(corpus.doctermRaw.T)
    F = corpus.termssorted    
    Y = []
    tags = ['python', 'php', 'html', 'android', 'javascript', 'sql'] 
    for tag in tags:         
        Y.append(corpus.labels_(tag))
    return X, XR, F, np.array(Y).T, np.array(tags)

def writetopfeatureblock(outpath, wordtype, vecimpl, topfeature, tfidfcfg, mindf, mintf):    
    X, R, F, Y, C = loadCounter(wordtype, topfeature, tfidfcfg, mindf, mintf)
    directory = './dist/data/'+outpath+'/'        
    save("X",  X,  directory)
    save("R", R, directory)
    save("F",  F,  directory)
    save('Y', Y, directory)
    save('C', C, directory)
    return X, R, F, Y, C

def tfidfframe():
    miindex = pd.MultiIndex.from_product(
        [ ['stackoverflow'],           
          ['stem', 'lemma', 'raw'],
          ['nltk', 'sklearn'], 
          ['32', '00', '11', '10', '01'], #combine("BLMR", "RCS")
          ['T', 'TB', 'TC', 'TBC']  #noreuse("TBCI")
        ],
        names=['source', 'wordtype', 'vecimpl', 'tf-idf', 'htmlfeature']
    )
    #cells = np.arange(len(miindex)*len(micolumns)).reshape((len(miindex),len(micolumns)))
    columns = ['$r_{c}$', '$r_{s}$', 's', 'f', '$r_{f}$', 'c', 'X','R','F', 'Y', 'C']    
    cells = np.arange(len(miindex)*len(columns)).reshape((len(miindex),len(columns)))
    cells = np.zeros((len(miindex), len(columns)))
    return pd.DataFrame(cells,index=miindex, columns=columns).sort_index().sort_index(axis=1)

def plot(path):

    path = './dist/data/'+path+'/'   

    #y = samples
    #x = terms
    #z = count | tfidf


    C = joblib.load(path+'C.pkl')    
    X = joblib.load(path+'X.pkl')
    #R
    F = joblib.load(path+'F.pkl')
    """
    IDF = 
    S = 
    df = pandas.DataFrame(X, index=, columns=)
    """
    
    

    

    print(X[:,1].shape)    
    print(X[:,2].shape)    
    print(X[:,3].shape)    

    """
    go.Scatter3d(        
        z=[:300], # dfXX[:300]            
    )
    """
    

    data = [
        go.Surface(            
            z= X[:300], # dfXX[:300]                        
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
            aspectratio = dict( x=1, y=1.7, z=0.2 ),
            aspectmode = 'manual'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return py.iplot(fig, filename='elevations-3d-surface')

def run(frame):    
    print("select", frame.shape)
    #print("select.index", frame.index.shape)
    #print("select.index", frame.index.values)
    
    minDfTfMap = {
        'T': (3,15),    
        'TI': (5,15),
        'TB': (5,25),
        'TC': (5,25),
        'TBC': (7,50) 
    }
    htmlfeatureMap = {
        'T': ['title'], 
        'TB': ['title', 'body'],
        'TC': ['title', 'code'],
        'TBC': ['title', 'body', 'code']
    }
    #tfidfMap = lambda str: map(list(str), lambda e: int(e))
    tfidfMap = {
        '32': [3,2],
        '11': [1,1],
        '00': [0,0],
        '10': [1,0]
    }
    for task in frame.index.values:
        #print("path", '/'.join(task))
        wordtype = task[1] 
        vecimpl = task[2] 
        tfidfcfg = tfidfMap[task[3]]
        topfeature = htmlfeatureMap[task[4]]        
        mindf = minDfTfMap[task[4]][0]
        mintf = minDfTfMap[task[4]][1]
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
    
def plan(s):    
    frame = tfidfframe()    
    #print("dataframe.index.shape", frame.index.shape)
    #print("dataframe.index.names", frame.index.names)    
    select = frame.loc[s, :]
    print("dataframe", frame.shape, "→",  "select", select.shape)
    
    def timediff(file):
        return str(time.ctime(os.path.getmtime(file))) if os.path.exists(file) else '-'

    for task in select.index.values:
        path = './dist/data/'+'/'.join(task) + '/'        
        # modified = time.ctime(os.path.getctime(file)))
        
        for col in frame.columns:
            frame.loc[task,col] = '-'

        frame.loc[task,'R'] = timediff(path + 'R.pkl')        
        frame.loc[task,'C'] = timediff(path + 'C.pkl')        
        frame.loc[task,'F'] = timediff(path + 'F.pkl')        
        frame.loc[task,'X'] = timediff(path + 'X.pkl')        
        frame.loc[task,'Y'] = timediff(path + 'Y.pkl')        
        
    #print("select.index.shape", select.index.shape)
    #print("select.index.names", select.index.names)    
    return frame.loc[s, :]    

if __name__ == "__main__":      
    s = (slice('stackoverflow'), slice('lemma'), slice('nltk'), slice('00', '32'), slice('T', 'TB'))    
    s = plan(s)
    run(s)

