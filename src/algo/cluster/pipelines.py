from sklearn.pipeline import Pipeline

from sklearn import decomposition
from sklearn import preprocessing
from sklearn import cluster

visdim = 3
clustervis_pipelines = {
    'PCA': Pipeline([
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.PCA(n_components=visdim))    
    ]),
    'NMF': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.NMF(n_components=visdim, random_state=1, alpha=.1, l1_ratio=.5)),
    ]),
    'DL': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.DictionaryLearning(n_components=visdim)),
    ]),
    'LatentDA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.LatentDirichletAllocation(n_components=visdim, learning_method='online')),
    ]),
    'SVD': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.TruncatedSVD(n_components=visdim)),
    ]),
    'FastICA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.FastICA(n_components=visdim)),
    ])    
}

featuredim = 30
clustercount = 15
cluster_pipelines = {    
    'Kmeans': Pipeline([                
        ('sca', decomposition.TruncatedSVD(featuredim)),
        ('norm', preprocessing.Normalizer(copy=False)),        
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
    ]),
    'LDA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('nmf', decomposition.NMF(n_components=featuredim, random_state=1, alpha=.1, l1_ratio=.5)),
        ('lda', decomposition.LatentDirichletAllocation(n_components=featuredim, max_iter=5, learning_method='online', learning_offset=50., random_state=0)),
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
    ])    
}