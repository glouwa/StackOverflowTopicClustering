import numpy as np
import json
import matplotlib.pyplot as plt
from tools.tfidf import StackoverflowCorpus
from tools.plots import fancy_dendrogram

from scipy.cluster.hierarchy import dendrogram, linkage, to_tree
from sklearn import preprocessing
from sklearn import pipeline
from sklearn import decomposition
from sklearn.externals import joblib

"""
wordtype = 'lemma'
topfeature = ['title', 'body']
tfidfcfg= [3, 2] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
print("Corpus", len(corpus.documents), len(corpus.termssorted))
"""

#interndim = 100
#algo = 'ward' # 'ward' 'single*' 'complete' 'average*''centroid ''median' 

tfidf = "11_title"
X_ = joblib.load('./dist/data/tf-idf/{}/nltk-X.pkl'.format(tfidf))
XR = joblib.load('./dist/data/tf-idf/{}/nltk-XR.pkl'.format(tfidf))
F = joblib.load('./dist/data/tf-idf/{}/nltk-F.pkl'.format(tfidf))

#F = zip(F, np.sum(XR, axis=0)).items()
#print(F)

def top(component, feature_names, n_top_words):        
    #return " ".join([feature_names[i] for i in component.argsort()[:n_top_words]])
    return " ".join([feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]])    

def createhierarchy(algo, preprocess, interndim):    
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
    #F = corpus.termssorted
    #L = corpus.doctermRaw.T
    Z = linkage(X, algo)
    n = len(Z)
    print("nltk reduced", X.shape)

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
    jsf = nodemap[rootid]
    path = '../../proj10/hypertree-of-life/dist/hierarchies/Open-Tree-of-Life/'
    with open("{}{}{}-{}.d3.json".format(path, preprocess, interndim, algo), 'w') as outfile:
        json.dump(jsf, outfile, indent=4)

createhierarchy('ward', 'SVD', 10)
createhierarchy('ward', 'SVD', 20)
createhierarchy('ward', 'LDA', 10)
createhierarchy('ward', 'LDA', 20)
createhierarchy('ward', 'PCA', 10)

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