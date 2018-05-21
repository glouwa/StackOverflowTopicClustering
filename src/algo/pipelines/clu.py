from sklearn.pipeline import Pipeline

from sklearn import decomposition
from sklearn import preprocessing
from sklearn import cluster
from sklearn import mixture
from sklearn import neighbors


def clustervis_pipelines(visdim):
    return {
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
        'LDA': Pipeline([                
            ('sca', preprocessing.MaxAbsScaler()),
            ('clu', decomposition.LatentDirichletAllocation(n_components=visdim, learning_method='online')),
            ('sca2', preprocessing.MaxAbsScaler()),
        ]),
        'SVD': Pipeline([                
            ('sca', preprocessing.MaxAbsScaler()),
            ('clu', decomposition.TruncatedSVD(n_components=visdim)),
            ('sca2', preprocessing.MaxAbsScaler()),
        ])    
    }

"""
'FastICA': Pipeline([
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.FastICA(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ])    

    'FA': Pipeline([                
        ('sca', preprocessing.MaxAbsScaler()),
        ('clu', decomposition.FactorAnalysis(n_components=visdim)),
        ('sca2', preprocessing.MaxAbsScaler()),
    ]),
"""

#decomp = decomposition.TruncatedSVD(featuredim)
#decomp = decomposition.LatentDirichletAllocation(n_components=featuredim, learning_method='batch')
#decomp = decomposition.NMF(n_components=featuredim, random_state=1, alpha=.1, l1_ratio=.5)

def cluster_pipelines(clustercount, featuredim, decompstr):
    decomp = clustervis_pipelines(featuredim)[decompstr]    
    return {            
        'Agglomerative': Pipeline([                                
            ('decomp', decomp),
            ('clu', cluster.AgglomerativeClustering(n_clusters=clustercount, linkage='ward')),
        ]),    
        'K-Means': Pipeline([                
            ('decomp', decomp),
            ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++', max_iter=100, n_init=1)),
        ]),
        'LDA': Pipeline([                
            ('decomp', decomp),
            ('clu', cluster.KMeans(n_clusters=clustercount, init='k-means++')),
            #('clu', neighbors.NearestNeighbors()),
        ]),
        'GMM': Pipeline([                        
            ('decomp', decomp),
            ('clu', mixture.GaussianMixture(n_components=clustercount)),
        ]),
        'DBScan': Pipeline([          
            ('decomp', decomp),
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
