
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

theoneandonlyclass = 'python'
print("Classifying {} or not".format(theoneandonlyclass))

doctermspace = StackoverflowCorpus('bag-of-words/stackoverflow-lemma', 'title', 3, 2)
print("DocumentSpace", len(doctermspace.documents), len(doctermspace.termssorted))

termvec = doctermspace.termssorted
X = np.matrix(doctermspace.w.T)
#X = preprocessing.StandardScaler().fit_transform(X)
X = preprocessing.MinMaxScaler().fit_transform(X)
#X = preprocessing.RobustScaler().fit_transform(X)

Y = [1 if theoneandonlyclass in doc['terms']['tags'][0] else 0 for doc in doctermspace.documentsraw]
print("Xshape", X.shape)
print("Y01", np.count_nonzero(Y), len(Y)-np.count_nonzero(Y))    

random_state = RandomState(0)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.5, random_state=random_state)

def precisionRecallPlot(y_test, y_score):
    average_precision = average_precision_score(y_test, y_score)
    precision, recall, _ = precision_recall_curve(y_test, y_score)

    plt.plot(recall, precision, color='b', alpha=0.2)
    #plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    

""" Decision Tree """

dtree = DecisionTreeClassifier()
dtree.fit(X, Y)
dtreepredict = dtree.predict(X_test)
precisionRecallPlot(y_test, dtreepredict)

#print("\nTree importance", dtree.feature_importances_)
print("Tree importance shape", dtree.feature_importances_.shape)
print("Tree importance max", np.argmax(dtree.feature_importances_))
print("Tree importance max", termvec[np.argmax(dtree.feature_importances_)])


termssortedimportance, bla = zip(*sorted(zip(dtree.feature_importances_, termvec)))
#print("Tree importance max", termssortedimportance, bla)

dot_data = tree.export_graphviz(dtree, out_file=None, 
                         feature_names=termvec,  
                         class_names=['jepp', 'nope'],  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = graphviz.Source(dot_data) 
graph.format = 'png'
graph.render('dtree_render',view=True)

""" SVM """

svm = svm.SVC(gamma=2, C=1)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)
#precisionRecallPlot(y_test, y_pred)

gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
#precisionRecallPlot(y_test, y_pred)

"""
gnb = MultinomialNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
precisionRecallPlot(y_test, y_pred)
"""
gnb = BernoulliNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
#precisionRecallPlot(y_test, y_pred)

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

kmeans = KMeans(n_clusters=5, random_state=0).fit(projected)
prediction = kmeans.predict(projected)
print(len(prediction))

#X_r2 = lda.fit(X, y).transform(X)

#print("\nPCA Components", pca.components_)
if True:
    print("PCA Components shape" , pca.components_.shape)
    max = np.argsmax(pca.components_, axis=1)
    min = np.argmin(pca.components_, axis=1)

    print("PCA Components max", max)
    print("PCA Components min", min)
    print(termvec[max[0]], termvec[max[1]], termvec[max[2]])
    print(termvec[min[0]], termvec[min[1]], termvec[min[2]])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.5, c=kmeans.labels_.astype(float))
ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], alpha=.2, c=prediction)
if True:
    ax.set_xlabel(termvec[min[0]] + '                   ' + termvec[max[0]])
    ax.set_ylabel(termvec[min[1]] + '                   ' + termvec[max[1]])
    ax.set_zlabel(termvec[min[2]] + '                   ' + termvec[max[2]])

plt.show()


