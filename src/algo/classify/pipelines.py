from sklearn.pipeline import Pipeline

from sklearn import preprocessing
from sklearn import decomposition
from sklearn import ensemble
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

_slow_or_bad_pipelines = {    
    'KNeighborsClassifier': Pipeline([        
        ('clf', KNeighborsClassifier(2))        
    ]),
    'GaussianProcessClassifier': Pipeline([        
        ('clf', GaussianProcessClassifier(1.0 * RBF(1.0)))
    ]),
    'GaussianNB': Pipeline([
        ('clf', GaussianNB())
    ]),
    'QuadraticDiscriminantAnalysis': Pipeline([        
        ('clf', QuadraticDiscriminantAnalysis())        
    ]),
    'ExtraTreeClassifier': Pipeline([                
        ('clf', ExtraTreeClassifier())        
    ]),
}

classify_pipelines = {
    'SGDClassifier': Pipeline([                
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None))    
    ]),
    'MLPClassifier': Pipeline([  
        ('clf', MLPClassifier(alpha=1))        
    ]),
    'Linear SVM': Pipeline([        
        ('nmf', decomposition.NMF(n_components=20, random_state=1, alpha=.1, l1_ratio=.5)),
        ('clf', svm.LinearSVC(C=1))
    ]),    
    'LinearDiscriminantAnalysis': Pipeline([        
        ('nmf', decomposition.NMF(n_components=20, random_state=1, alpha=.1, l1_ratio=.5)),
        #('scale', preprocessing.Normalizer()),
        ('clf', LinearDiscriminantAnalysis())
    ]),
    'DecisionTreeClassifier': Pipeline([                
        ('clf', DecisionTreeClassifier())        
    ]),    
    'RandomForestClassifier': Pipeline([        
        ('clf', ensemble.RandomForestClassifier())
    ]),
    'AdaBoostClassifier': Pipeline([        
        ('clf', ensemble.AdaBoostClassifier())        
    ]),               
}
