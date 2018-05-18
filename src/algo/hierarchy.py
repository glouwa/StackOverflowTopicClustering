import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from tfidf import StackoverflowCorpus
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree

from sklearn import preprocessing
from sklearn import pipeline
from sklearn import decomposition

wordtype = 'lemma'
topfeature = 'title'
tfidfcfg= [3, 2] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
print("Corpus", len(corpus.documents), len(corpus.termssorted))

interndim = 100

X_ = np.matrix(corpus.w.T)

p = pipeline.Pipeline([
    ('sca', preprocessing.MaxAbsScaler()),
    #('clu', decomposition.PCA(n_components=interndim))    
    ('clu', decomposition.TruncatedSVD(n_components=interndim)),
    ('norm', preprocessing.MaxAbsScaler()) 
])
X = p.fit_transform(X_)
C = p.named_steps['clu'].components_
F = corpus.termssorted
print("Compoentens", C.shape)

def top(component, feature_names, n_top_words):        
    return " ".join([feature_names[i] for i in component.argsort()[:n_top_words]])
    #return " ".join([feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]])    


for c in C:
    print(top(c, F, 3))


print("nltk reduced", X.shape)

#Z = linkage(X, 'ward')
#Z = linkage(X, 'single')
Z = linkage(X, 'complete')
#Z = linkage(X, 'average')

print(Z[:20])

acc = {}
acc['count'] = 0

def visit(n):
    acc['count'] += 1
    if n.get_id() > len(Z):
        print(acc['count'], n.get_id())
    



to_tree(Z).pre_order(visit)

max_d = 10

from scipy.cluster.hierarchy import fcluster
clusters = fcluster(Z, max_d, criterion='distance')
print(clusters.shape)

def  fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    #print(ddata['leaves'])
    #print(ddata['leaves'].shape)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        count = 0
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            count+=1            
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate(llf(n*2-1-count), (x, y), xytext=(0, 0),
                             textcoords='offset points',
                             va='top', ha='right', rotation=45, fontsize=7.)
        #if max_d:
        #    plt.axhline(y=max_d, c='k')
    return ddata

n = len(Z)
print("zlen", n, Z.shape)

#nodeMat = np.zeros((n, len(corpus.termssorted)))
nodeMat = np.zeros((n, interndim))

print(nodeMat.shape)
print(nodeMat[0].shape)

for idx, node in enumerate(Z):    
    lid = int(node[0])
    rid = int(node[1])    
    left  = X[lid] if lid < n else nodeMat[lid-n]
    right = X[rid] if rid < n else nodeMat[rid-n]        
    nodeMat[idx] = (left + right)/2

def component2term(cw, c):
    #print(cw.shape, c.shape)    
    o = np.dot(cw, c)
    #print("outer", o.shape)    
    return o
    s = sum(o)
    print("orig", s.shape)
    return s

def llf(id):
    if id < n:
        cw = C[id]
    else:
        cw = nodeMat[id-n]
    tw = component2term(cw, C)
    return top(tw, F, 3)
    
print(llf(n*2-1))
#top(X[0], F, 3)
#print(llf(n-1))

fancy_dendrogram(
    Z,
    truncate_mode='lastp', #lastp level
    p=50,
    leaf_rotation=90.,    
    leaf_font_size=8.,
    show_contracted=False,
    annotate_above=0,  # useful in small plots so annotations don't overlap 
    max_d=max_d,
    leaf_label_func=llf
)
plt.show()
#orientation='left',
#right=0.4,