
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
"""
dot_data = tree.export_graphviz(dtree, out_file=None, 
                         feature_names=termvec,  
                         class_names=['jepp', 'nope'],  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = graphviz.Source(dot_data) 
graph.format = 'png'
graph.render('dtree_render',view=True)
"""