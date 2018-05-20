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
        ('clu', decomposition.PCA(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
    'NMF': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.NMF(n_components=visdim, random_state=1, alpha=.1, l1_ratio=.5)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
    'FA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.FactorAnalysis(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
    'LatentDA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.LatentDirichletAllocation(n_components=visdim, learning_method='online')),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
    'SVD': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.TruncatedSVD(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
    'FastICA': Pipeline([
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.FastICA(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ])    
}

featuredim = 40
decomp = decomposition.PCA(n_components=featuredim)
#decomp = decomposition.TruncatedSVD(featuredim)
#decomp = decomposition.LatentDirichletAllocation(n_components=featuredim, learning_method='batch')
#decomp = decomposition.NMF(n_components=featuredim, random_state=1, alpha=.1, l1_ratio=.5)

clustercount = 15
cluster_pipelines = {            
    'Agglo': Pipeline([                                
        ('sca', preprocessing.MaxAbsScaler(copy=False)),
        ('pca', decomp),
        ('norm', preprocessing.MaxAbsScaler(copy=False)),
        ('clu', cluster.AgglomerativeClustering(n_clusters=clustercount, linkage='ward')),
    ]),    
    'Kmeans': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler(copy=False)),
        ('decomp', decomp),
        ('norm', preprocessing.MaxAbsScaler(copy=False)),
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
    ]),
    'LDA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler(copy=False)),        
        ('lda', decomp),
        ('norm', preprocessing.MaxAbsScaler(copy=False)),
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++')),
        #('clu', neighbors.NearestNeighbors()),
    ]),
    'GMM': Pipeline([                        
        ('sca', preprocessing.MaxAbsScaler(copy=False)),
        ('pca', decomposition.PCA(n_components=featuredim)),
        ('norm', preprocessing.MaxAbsScaler(copy=False)),
        ('clu', mixture.GaussianMixture(n_components=clustercount)),
    ]),
    'DBScan': Pipeline([          
        ('sca', preprocessing.MaxAbsScaler(copy=False)),
        ('pca', decomposition.PCA(n_components=4)),
        ('norm', preprocessing.MaxAbsScaler(copy=False)),
        ('clu', cluster.DBSCAN(eps=0.1, min_samples=20)),
    ]), 
    
}
"""
   'AffPro': Pipeline([                                
        ('sca', preprocessing.MaxAbsScaler()),
        ('pca', decomposition.PCA(n_components=3)),
        ('clu', cluster.AffinityPropagation(max_iter=50)),
    ]), 

"""
"""

'Agglo2': Pipeline([                                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', cluster.FeatureAgglomeration(n_clusters=clustercount, linkage='ward')),
    ]),

'spectral': Pipeline([                        
        ('sca', preprocessing.MaxAbsScaler()),
        ('clus', cluster.SpectralClustering(n_clusters=clustercount)),
        ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
        #('clu', neighbors.NearestNeighbors()),
    ]),
"""
