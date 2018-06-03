import numpy as np
import json
import matplotlib.pyplot as plt
from src.algo.tfidf import StackoverflowCorpus

from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from sklearn import preprocessing
from sklearn import pipeline
from sklearn import decomposition
from sklearn.externals import joblib
from IPython.core.display import display, HTML

def top(component, feature_names, n_top_words):    
    #return " ".join([feature_names[i] for i in component.argsort()[:n_top_words]])
    return " ".join([feature_names[i] for i in np.argsort(component)[:-n_top_words - 1:-1]])

def preorder(node, visit):
    visit(node)    
    if not node.is_leaf():        
        postorder(node.get_right(), visit)	
        postorder(node.get_left(), visit) 

def postorder(node, visit):
    if not node.is_leaf():        
        postorder(node.get_right(), visit)	
        postorder(node.get_left(), visit) 
    visit(node)

def getRawCountMat(Z, XR, n, F):
    nodeMat = np.zeros((n+1, len(F)))    
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
            nodeMat[id-n] = np.add(left, right)

    tree = to_tree(Z)
    postorder(tree, visit)
    rootid = tree.get_id()-n    
    return nodeMat, tree

def getDampedCountMat(XR, n, F, nodeMat, tree):        
    dampedMat = nodeMat.copy()
    context = {}
    def visit(node):    
        if not node.is_leaf():
            id = node.get_id()
            if 'parent' in context:
                dampedMat[id-n] = np.subtract(dampedMat[id-n], context['parent']).clip(min=0)            
            context['parent'] = dampedMat[id-n]
    
    preorder(tree, visit)
    return dampedMat

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
    return nodemap[tree.get_id()-n]    
    
def createhierarchy(X_, XR, F, algo, preprocess, interndim):    
    Z = linkage(X_, algo)
    n = len(Z)

    nodeMat, tree = getRawCountMat(Z, XR, n, F)    
    dampedMat = getDampedCountMat(XR, n, F, nodeMat, tree)
    jsonroot = convertd3json(XR, n, F, dampedMat, tree)

    path = 'dist/visualisations/hierarchies/'    
    file = "{}{}{}-{}.d3.json".format(path, preprocess, interndim, algo)
    print(file)
    with open(file, 'w') as outfile:
        json.dump(jsonroot, outfile, indent=4)
    
def run(path, decomp, dim, highlight):        
    path = './dist/data/'+path+'/'    
    R = joblib.load(path+'../R.pkl')
    F = joblib.load(path+'F.pkl')
    R = np.squeeze(np.asarray(R))

    decomppath = path + 'decomposition/' + decomp + '/' + str(dim) + '/'
    X = joblib.load(decomppath + 'P.pkl')

    createhierarchy(X, R, F, 'ward', decomp, dim)

    file = "{}{}-ward".format(decomp, dim)
    iframe = """
        <iframe width="100%" 
                height="900"
                frameBorder="0" 
                src="http://localhost:3000/dist/visualisations/tree.html?f={}"
        </iframe>""".format(file)
    display(HTML(iframe))



            