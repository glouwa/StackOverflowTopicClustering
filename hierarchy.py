import numpy as np
import json
import matplotlib.pyplot as plt
from src.algo.tfidf import StackoverflowCorpus

from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from sklearn import preprocessing
from sklearn import pipeline
from sklearn import decomposition
from sklearn.externals import joblib

def top(component, feature_names, n_top_words):        
    #return " ".join([feature_names[i] for i in component.argsort()[:n_top_words]])
    return " ".join([feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]])    

def postorder(node, visit):
    if not node.is_leaf():        
        postorder(node.get_right(), visit)	
        postorder(node.get_left(), visit) 
    visit(node)

def calc(X_, algo, preprocess, interndim):
    if preprocess == 'LDA':
        prepro = decomposition.LatentDirichletAllocation(n_components=interndim, learning_method='batch')
    elif preprocess == 'PCA':        
        prepro = decomposition.PCA(n_components=interndim) 
    else:
        prepro = decomposition.TruncatedSVD(n_components=interndim)

    p = pipeline.Pipeline([
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', prepro),  
        ('norm', preprocessing.MaxAbsScaler()) 
    ])
    X = p.fit_transform(X_)
    Z = linkage(X, algo)
    n = len(Z)
    return Z, n

def getRawCountMat(Z, XR, n, F):
    nodeMat = np.zeros((n+1, len(F)))
    print("nodemat", nodeMat.shape)
    print("XL", XR.shape)
    print("zlen", n, Z.shape)
    
    allterms = sum(XR)
    print("all terms shape", allterms.shape)
    print("all terms sum:", top(allterms, F, 10))
    def visit(node):    
        if not node.is_leaf():        
            id = node.get_id()
            assert(id > n)
            lid = node.get_left().get_id()
            rid = node.get_right().get_id()
            assert(lid >= 0 and rid >= 0)
            left  = XR[lid] if lid < n else nodeMat[lid-n]
            right = XR[rid] if rid < n else nodeMat[rid-n]        
            #nodeMat[id-n-1] = np.add(left, right)
            nodeMat[id-n] = left + right

    tree = to_tree(Z)
    postorder(tree, visit)
    rootid = tree.get_id()-n
    print("rootid", rootid)
    print("rootid", top(nodeMat[rootid], F, 10))
    return nodeMat, tree

def convertd3json(XR, n, F, nodeMat, tree):
    nodemap = {} # kack index
    nodemap[0] = { 'name':'dummy' }
    def visitjson(node):    
        if node.is_leaf():    
            id = node.get_id()      
            nodemap[id] = {
                "name": top(XR[id], F, 3),
                "numLeafs": node.get_count()-1
            }
        else:        
            id = node.get_id()
            assert(id > n)
            lid = node.get_left().get_id()
            rid = node.get_right().get_id()
            left  = nodemap[lid] if lid < n else nodemap[lid-n]        
            right = nodemap[rid] if rid < n else nodemap[rid-n]        
            nodemap[id-n] = {
                "name": top(nodeMat[id-n], F, 3),
                "numLeafs": node.get_count()-1,
                "children": [ left, right ]
            }
    postorder(tree, visitjson)
    return nodemap[ tree.get_id()-n]    
    
def createhierarchy(X_, XR, F, algo, preprocess, interndim):        
    Z, n = calc(X_, algo, preprocess, interndim)
    nodeMat, tree = getRawCountMat(Z, XR, n, F)    
    jsonroot = convertd3json(XR, n, F, nodeMat, tree)

    path = '../../proj10/hypertree-of-life/dist/hierarchies/Open-Tree-of-Life/'    
    with open("{}{}{}-{}.d3.json".format(path, preprocess, interndim, algo), 'w') as outfile:
        json.dump(jsonroot, outfile, indent=4)
    
def run(tfidf, comp, dims, highlight):    
    X_ = joblib.load('./dist/data/tf-idf/{}/nltk-X.pkl'.format(tfidf))
    XR = joblib.load('./dist/data/tf-idf/{}/nltk-XR.pkl'.format(tfidf))
    F  = joblib.load('./dist/data/tf-idf/{}/nltk-F.pkl'.format(tfidf))
    print("F", F.shape, F)

    createhierarchy(X_, XR, F, 'ward', 'SVD', 10)
    createhierarchy(X_, XR, F, 'ward', 'SVD', 20)
    createhierarchy(X_, XR, F, 'ward', 'LDA', 10)
    createhierarchy(X_, XR, F, 'ward', 'LDA', 20)
    createhierarchy(X_, XR, F, 'ward', 'PCA', 10)

"""
def llf(id):
    if id < n:
        return top(XL[id], F, 3)
    else:
        return top(nodeMat[id-n-1], F, 3)

print("nodemat done")
fancy_dendrogram(
    Z,
    truncate_mode='level', #lastp level
    p=8,
    leaf_rotation=90.,    
    leaf_font_size=8.,
    show_contracted=False,
    annotate_above=0,  # useful in small plots so annotations don't overlap 
    max_d=max_d,
    leaf_label_func=llf
)
plt.show()
"""