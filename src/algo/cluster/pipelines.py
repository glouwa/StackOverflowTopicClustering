from sklearn.pipeline import Pipeline

from sklearn import decomposition
from sklearn import preprocessing
from sklearn import cluster
from sklearn import mixture
from sklearn import neighbors

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
clustercount = 50
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
        #('clu', neighbors.NearestNeighbors()),
    ]),
    'GMM': Pipeline([                        
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', mixture.GaussianMixture(n_components=clustercount)),
    ]),
    'Birch': Pipeline([                        
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', cluster.Birch(n_clusters=clustercount)),
    ]),    
    'DBScan': Pipeline([                                
        ('clu', cluster.DBSCAN(eps=0.3, min_samples=10)),
    ]),    
}

cluster_pipelines = {        
    'DBScan': Pipeline([                                
        ('sca', preprocessing.StandardScaler()),
        ('clu', cluster.DBSCAN(min_samples=10)),
    ]),
    'Agglo': Pipeline([                                
        ('sca', preprocessing.StandardScaler()),
        ('clu', cluster.AgglomerativeClustering(n_clusters=clustercount, linkage='ward')),
    ]),
    'AffPro': Pipeline([                                
        ('sca', preprocessing.StandardScaler()),
        ('clu', cluster.AffinityPropagation()),
    ]),
}

"""
'spectral': Pipeline([                        
        ('sca', preprocessing.MaxAbsScaler()),
        ('clus', cluster.SpectralClustering(n_clusters=clustercount)),
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
        #('clu', neighbors.NearestNeighbors()),
    ]),
"""
