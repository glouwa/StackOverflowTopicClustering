import numpy as np
import pandas as pd
import itertools

columns = ['$r_{c}$', '$r_{s}$', 's', 'f', '$r_{f}$', 'c', 'X','R','F', 'Y', 'C']    

##################################################################################################

wordvecpathnames=['source', 'wordtype', 'vecimpl', 'tf-idf', 'htmlfeature']
wordvecpath = [
    ['stackoverflow'],           
    ['stem', 'lemma', 'raw'],
    ['nltk', 'sklearn'], 
    ['32', '00', '11', '10', '01'], #combine("BLMR", "RCS")
    ['T', 'TB', 'TC', 'TBC'],  #noreuse("TBCI")
]

def WordVecFrame(initcell):    
    miindex = pd.MultiIndex.from_product(
        wordvecpath,
        names=wordvecpathnames
    )            
    cells = np.empty((len(miindex), len(columns)), dtype=str)
    cells[:] = initcell
    return pd.DataFrame(cells, index=miindex, columns=columns)

##################################################################################################

featurepathnames = ['class', 'scorefunc']
featurepath = [
    ['android', 'javascript', 'java', 'php'],
    ['chi2', 'mi', 'f_classif', 'mutual_info_classif']
]
featurepath = list(itertools.chain(*[wordvecpath, featurepath]))
featurepathnames = list(itertools.chain(*[wordvecpathnames, featurepathnames]))

def FeatureFrame(initcell):    
    miindex = pd.MultiIndex.from_product(
        featurepath,
        names=featurepathnames
    )            
    cells = np.empty((len(miindex), len(columns)), dtype=str)
    cells[:] = initcell
    return pd.DataFrame(cells, index=miindex, columns=columns)

##################################################################################################

decomppathnames = ['algo', 'dim']
decomppath = [
    ['PCA', 'NMF', 'LDA', 'SVD'],
    ['2', '3', '4', '6', '8', '10', '12', '16']
]
decomppath = list(itertools.chain(*[wordvecpath, decomppath]))
decomppathnames = list(itertools.chain(*[wordvecpathnames, decomppathnames]))

def DecompositionFrame(initcell):    
    miindex = pd.MultiIndex.from_product(
        decomppath,
        names=decomppathnames
    )            
    cells = np.empty((len(miindex), len(columns)), dtype=str)
    cells[:] = initcell
    return pd.DataFrame(cells, index=miindex, columns=columns)