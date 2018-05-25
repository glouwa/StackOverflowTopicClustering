import numpy as np
import pandas as pd
import itertools
import os
from sklearn.externals import joblib
import src.algo.cell2string 

cell2string = src.algo.cell2string 

##################################################################################################

wordveccolumns = ['$r_{c}$', '$r_{s}$', 's', 'f', '$r_{f}$', 'c', 'X','R','F', 'Y', 'C']    
wordvecpathnames=['source', 'wordtype', 'vecimpl', 'tf-idf', 'htmlfeature']
wordvecpath = [
    ['stackoverflow'],           
    ['stem', 'lemma', 'raw'],
    ['nltk', 'sklearn'], 
    ['32', '00', '11', '10', '01', '31', '30'], #combine("BLMR", "RCS")
    ['T', 'TI', 'TIB', 'TIC', 'TIBC', 'TB', 'TC', 'TBC'],  #noreuse("TBCI")
]

def WordVecFrame():    
    miindex = pd.MultiIndex.from_product(
        wordvecpath,
        names=wordvecpathnames
    )            
    cells = np.empty((len(miindex), len(wordveccolumns)), dtype=str)
    return pd.DataFrame(cells, index=miindex, columns=wordveccolumns)

##################################################################################################

featurecolumns = ['X', 'Mask', 'Indices', 'Scores', 'Pvalue', 'assertF', 'assertY']    
featurepathnames = ['class', 'scorefunc']
featurepath = [
    ['python', 'android', 'javascript', 'java', 'php', 'c++', 'spring', 'pandas', 'html', 'sql'],
    ['chi2', 'f_classif', 'mutual_info_classif']
]
featurepath = list(itertools.chain(*[wordvecpath, featurepath]))
featurepathnames = list(itertools.chain(*[wordvecpathnames, featurepathnames]))

def FeatureFrame():    
    miindex = pd.MultiIndex.from_product(
        featurepath,
        names=featurepathnames
    )            
    cells = np.empty((len(miindex), len(featurecolumns)), dtype=str)
    return pd.DataFrame(cells, index=miindex, columns=featurecolumns)

##################################################################################################

decomppathnames = ['algo', 'dim']
decomppath = [
    ['PCA', 'NMF', 'LDA', 'SVD'],
    ['2', '3', '4', '6', '8', '10', '12', '16']
]
decomppath = list(itertools.chain(*[wordvecpath, decomppath]))
decomppathnames = list(itertools.chain(*[wordvecpathnames, decomppathnames]))

def DecompositionFrame():    
    miindex = pd.MultiIndex.from_product(
        decomppath,
        names=decomppathnames
    )            
    cells = np.empty((len(miindex), len(wordveccolumns)), dtype=str)
    return pd.DataFrame(cells, index=miindex, columns=wordveccolumns)

##################################################################################################

def load(path, namearr):
    return ( joblib.load(path+'/'+name+'.pkl') for name in namearr )

def save(path, name, M):    
    if not os.path.exists(path):
        os.makedirs(path)       
        print("makedir", path)        
    filename = path + '{}.pkl'.format(name)
    joblib.dump(M, filename)  