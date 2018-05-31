import numpy as np
import pandas as pd
import itertools
import os
from sklearn.externals import joblib
import src.algo.cell2string 

cell2string = src.algo.cell2string 

##################################################################################################

wordveccolumns = ['$r_{c}$', '$r_{s}$', 's', 'f', '$r_{f}$', 'c', 'X','R','F', 'IDF', 'TDOC', 'Y', 'C']    
wordvecpathnames=['source', 'wordtype', 'vecimpl', 'htmlfeature', 'tf-idf']
wordvecpath = [
    ['stackoverflow'],           
    ['stem', 'lemma', 'raw'],
    ['nltk', 'sklearn'], 
    ['T', 'TI', 'TIB', 'TIC', 'TIBC', 'TB', 'TC', 'TBC'],  #noreuse("TBCI")
    ['32', '00', '11', '10', '01', '31', '30'], #combine("BLMR", "RCS")    
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
featurepathnames = ['transformation', 'scorefunc', 'class']
featurepath = [
    ['featureselect'],
    ['chi2', 'f_classif', 'mutual_info_classif'],
    ['python', 'android', 'javascript', 'java', 'php', 'c++', 'spring', 'pandas', 'html', 'sql', 'reactjs', 'c++', 'git', 'scala', 'oracle', 'csharp'],    
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

decompcolumns = ['P', 'COMP', 'assertF']
decomppathnames = ['transformation', 'algo', 'dim']
decomppath = [
    ['decomposition'],
    ['PCA', 'NMF', 'LDA', 'SVD'],
    ['2', '3', '4', '6', '8', '10', '12', '16', '24', '50', '100']
]
decomppath = list(itertools.chain(*[wordvecpath, decomppath]))
decomppathnames = list(itertools.chain(*[wordvecpathnames, decomppathnames]))

def DecompositionFrame():    
    miindex = pd.MultiIndex.from_product(
        decomppath,
        names=decomppathnames
    )            
    cells = np.empty((len(miindex), len(decompcolumns)), dtype=str)
    return pd.DataFrame(cells, index=miindex, columns=decompcolumns)

##################################################################################################

def load(path, namearr):
    return ( joblib.load(path+'/'+name+'.pkl') for name in namearr )

def save(path, name, M):    
    if not os.path.exists(path):
        os.makedirs(path)       
        print("makedir", path)        
    filename = path + '{}.pkl'.format(name)
    joblib.dump(M, filename)  