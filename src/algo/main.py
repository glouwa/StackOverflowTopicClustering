import plots 
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from tfidf import StackoverflowCorpus
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
from sparse2dense import DenseTransformer
from pprint import pprint
from numpy.random import RandomState

from sklearn import decomposition
from sklearn import preprocessing
from sklearn import feature_selection
from sklearn import svm

from classify.pipelines import classify_pipelines
from cluster.pipelines import cluster_pipelines

""" load data """
theoneandonlyclass = 'python'
wordtype = 'lemma'
topfeature = 'title'
tfidfcfg= [0, 0]
corpus = StackoverflowCorpus('bag-of-words/stackoverflow-' + wordtype, topfeature, tfidfcfg[0], tfidfcfg[1])
Y = corpus.labels(theoneandonlyclass)
print("Corpus", len(corpus.documents), len(corpus.termssorted))
print("Classifying {} or not, in {} {}".format(theoneandonlyclass, topfeature, wordtype))
print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))

""" nltk or sklearn """
X = np.matrix(corpus.w.T)
print("nltk reduced", X.shape)

pipeline = Pipeline([
    ('vect', text.CountVectorizer(stop_words='english', min_df=10, max_df=1.0, binary=False)),
    ('tfidf', text.TfidfTransformer()),
    ('dense', DenseTransformer()),
])
X2 = pipeline.fit_transform(corpus.documentsstr)
print("sklearn reduced", X2.shape)

""" do some stuff """
f1 = plt.figure()
def classify():
    for label, pipeline in classify_pipelines.items():    
        print("time for", label)
        pipeline.fit(X_train, Y_train)
        Y_pred = pipeline.predict(X_test)
        Z = Y_pred
        plots.precisionRecallPlot(ax, label, Y_test, Y_pred, Z)
    
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.25, random_state=0)
print(X_train.shape, len(Y_train))
ax = f1.add_subplot(211)    
ax.set_title('nltk preprocessing {}{}'.format(tfidfcfg[0], tfidfcfg[1]))
classify()
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    

X_train, X_test, Y_train, Y_test = train_test_split(X2, Y, test_size=.25, random_state=0)
print(X_train.shape, len(Y_train))
ax = plt.subplot(212)
ax.set_title('sklearn preprocessing')
classify()
ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
plt.tight_layout()

""" vis reduced """
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
fig.suptitle('nltk preprocessing {}{}'.format(tfidfcfg[0], tfidfcfg[1]))
p=1
for label, pipeline in cluster_pipelines.items():
    print("time for", label)
    projected = pipeline.fit_transform(X)    
    ax = fig.add_subplot(2, 4, p, projection='3d')
    ax.set_title(label)
    p+=1
    #ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.5, c=kmeans.labels_.astype(float))
    ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.2, c=Y)
plt.tight_layout()


fig = plt.figure()
fig.suptitle('sklearn preprocessing')
p=1
for label, pipeline in cluster_pipelines.items():
    print("time for", label)
    projected = pipeline.fit_transform(X2)
    ax = fig.add_subplot(2, 4, p, projection='3d')
    ax.set_title(label)
    p+=1
    #ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.5, c=kmeans.labels_.astype(float))
    ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.2, c=Y)
plt.tight_layout()
plt.show()