
import numpy as np
import scipy as sp
from sklearn.cluster import KMeans
from sklearn import decomposition
from numpy.random import RandomState
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from tfidf import StackoverflowCorpus
import graphviz 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import preprocessing

theoneandonlyclass = 'javascript'
print("Classifying {} or not".format(theoneandonlyclass))

doctermspace = StackoverflowCorpus('bag-of-words/stackoverflow-lemma', 'title', 3, 2)
print("DocumentSpace", len(doctermspace.documents), len(doctermspace.termssorted))

termvec = doctermspace.termssorted
X = np.matrix(doctermspace.w.T)
#X = preprocessing.StandardScaler().fit_transform(X)
X = preprocessing.MaxAbsScaler().fit_transform(X)
#X = preprocessing.RobustScaler().fit_transform(X)

Y = [1 if theoneandonlyclass in doc['terms']['tags'][0] else 0 for doc in doctermspace.documentsraw]
print("Xshape", X.shape)
print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))    

""" K-means """

kmeans = KMeans(n_clusters=50, random_state=0).fit(X)
prediction = kmeans.predict(X)
print(len(prediction))

""" PCA """

#KernelPCA(n_components=3, whiten=True)
#pca = decomposition.KernelPCA(n_components=3, kernel='cosine') #“linear” | “poly” | “rbf” | “sigmoid” | “cosine” 
pca = decomposition.PCA(n_components=3, whiten=True)
#pca = LinearDiscriminantAnalysis(n_components=3, solver='svd') # svd lsqr eigen
projected = pca.fit_transform(X)
print(projected.shape)

kmeans = KMeans(n_clusters=15, random_state=0).fit(projected)
prediction = kmeans.predict(projected)
print(len(prediction))

#X_r2 = lda.fit(X, y).transform(X)
def top_words(component, feature_names, n_top_words):    
    return [feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]]
        

def bottom_words(component, feature_names, n_top_words):    
    return [feature_names[i] for i in component.argsort()[:n_top_words]]
        


#print("\nPCA Components", pca.components_)
if True:
    print("PCA Components shape" , pca.components_.shape)    
    max = np.argmax(pca.components_, axis=1)
    min = np.argmin(pca.components_, axis=1)

    for idx, c in enumerate(pca.components_):
        print("Component", idx)
        print(" ".join(top_words(c, termvec, 10)))
        print(" ".join(bottom_words(c, termvec, 10)))

    print("PCA Components max", max)    
    print("PCA Components min", min)    
    print(termvec[max[0]], termvec[max[1]], termvec[max[2]])
    print(termvec[min[0]], termvec[min[1]], termvec[min[2]])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.5, c=kmeans.labels_.astype(float))
ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.2, c=Y)

def compbottom(pca, cidx):
    return " ".join(bottom_words(pca.components_[cidx], termvec, 5))

def comptop(pca, cidx):
    return " ".join(top_words(pca.components_[cidx], termvec, 5))

if True:
    ax.set_xlabel(compbottom(pca, 0) + '  -  ' + comptop(pca, 0))
    ax.set_ylabel(compbottom(pca, 1) + '  -  ' + comptop(pca, 1))
    ax.set_zlabel(compbottom(pca, 2) + '  -  ' + comptop(pca, 2))

plt.show()


