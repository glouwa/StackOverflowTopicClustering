import numpy as np
import matplotlib.pyplot as plt
from tfidf import StackoverflowCorpus
from scipy.cluster.hierarchy import dendrogram, linkage

wordtype = 'raw'
topfeature = 'title'
tfidfcfg= [1, 1] # 11 wolkig aber gelb, 32 beste klassifikations aber nix gelb, 00 separiert gut sonst bullshit
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
print("Corpus", len(corpus.documents), len(corpus.termssorted))

X = np.matrix(corpus.w.T)
F = corpus.termssorted
print("nltk reduced", X.shape)



Z = linkage(X, 'average')


"""
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()
"""


def  fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


R = fancy_dendrogram(
    Z,
    truncate_mode='level',
    p=8,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,  # useful in small plots so annotations don't overlap
    max_d=1,
)

def llf(id, a, b):
    if id < len(Z):
        return str(id)
    else:
        return '[%d %d %1.2f]' % (id, R[n-id,3])

fancy_dendrogram(
    Z,
    truncate_mode='level',
    p=8,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,  # useful in small plots so annotations don't overlap
    max_d=1,
    leaf_label_func=llf
)
plt.show()
