from sklearn.pipeline import Pipeline

from sklearn import decomposition
from sklearn import preprocessing

cluster_pipelines = {
    'PCA': Pipeline([
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.PCA(n_components=3))    
    ]),
    'NMF': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.NMF(n_components=3, random_state=1, alpha=.1, l1_ratio=.5)),
    ]),
    'DL': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.DictionaryLearning(n_components=3)),
    ]),
    'LatentDA': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.LatentDirichletAllocation(n_components=3, learning_method='online')),
    ]),
    'SVD': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.TruncatedSVD(n_components=3)),
    ]),
    'FastICA': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.FastICA(n_components=3)),
    ]),
    'FactorAnalysis': Pipeline([                
        ('sca', preprocessing.MinMaxScaler()),
        ('clu', decomposition.KernelPCA(n_components=3, kernel='sigmoid')),
    ])
}


