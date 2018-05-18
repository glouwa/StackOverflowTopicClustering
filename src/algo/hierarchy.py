import numpy as np
import json
import matplotlib.pyplot as plt
from pprint import pprint
from tfidf import StackoverflowCorpus
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from plots import fancy_dendrogram

from sklearn import preprocessing
from sklearn import pipeline
from sklearn import decomposition

wordtype = 'lemma'
topfeature = ['title']
tfidfcfg= [0, 0] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
print("Corpus", len(corpus.documents), len(corpus.termssorted))

interndim = 10
algo = 'complete' # 'ward' 'single*' 'complete' 'average*''centroid ''median' 

X_ = np.matrix(corpus.w.T)

p = pipeline.Pipeline([
    ('sca', preprocessing.MaxAbsScaler()),
    #('clu', decomposition.PCA(n_components=interndim)),  
    ('clu', decomposition.TruncatedSVD(n_components=interndim)),
    ('norm', preprocessing.MaxAbsScaler()) 
])
X = p.fit_transform(X_)
F = corpus.termssorted
XL = corpus.doctermRaw.T

def top(component, feature_names, n_top_words):        
    #return " ".join([feature_names[i] for i in component.argsort()[:n_top_words]])
    return " ".join([feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]])    

print("nltk reduced", X.shape)

Z = linkage(X, algo)

max_d = 2
n = len(Z)
print("zlen", n, Z.shape)
nodeMat = np.zeros((n+1, len(corpus.termssorted)))
print("nodemat", nodeMat.shape)
print("XL", XL.shape)

allterms = sum(XL)
print("all terms shape", allterms.shape)
print("all terms sum:", top(allterms, F, 10))
def visit(node):    
    if not node.is_leaf():        
        id = node.get_id()
        assert(id > n)
        lid = node.get_left().get_id()
        rid = node.get_right().get_id()
        assert(lid >= 0 and rid >= 0)
        left  = XL[lid] if lid < n else nodeMat[lid-n]
        right = XL[rid] if rid < n else nodeMat[rid-n]        
        #nodeMat[id-n-1] = np.add(left, right)
        nodeMat[id-n] = left + right

def postorder(node, visit):
    if not node.is_leaf():        
        postorder(node.get_right(), visit)	
        postorder(node.get_left(), visit) 
    visit(node)

tree = to_tree(Z)
postorder(tree, visit)
rootid = tree.get_id()-n
print("rootid", rootid)
print("rootid", top(nodeMat[rootid], F, 10))

nodemap = {} # kack index
nodemap[0] = { 'name':'dummy' }
def visitjson(node):    
    if node.is_leaf():    
        id = node.get_id()      
        nodemap[id] = {
            "name": top(XL[id], F, 3),
            "numLeafs": node.get_count()
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
            "numLeafs": node.get_count(),
            "children": [ left, right ]
        }

postorder(tree, visitjson)
jsf = nodemap[rootid]
path = '../../proj10/hypertree-of-life/dist/hierarchies/Kddm/'
with open("{}SVD{}-{}.json".format(path, interndim, algo), 'w') as outfile:
    json.dump(jsf, outfile, indent=4)

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