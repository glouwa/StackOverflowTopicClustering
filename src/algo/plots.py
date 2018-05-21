import numpy as np
from sklearn import metrics

from matplotlib.colors import to_rgba
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

def precisionRecallPlot(ax, label, Y_test, Y_pred, defun):
    f1 = metrics.f1_score(Y_test, Y_pred)
    pr = metrics.precision_score(Y_test, Y_pred)
    rc = metrics.recall_score(Y_test, Y_pred)
    label = ('%.2f' % f1).lstrip('0') + ' ' + ('%.2f' % pr).lstrip('0') + ' ' + ('%.2f' % rc).lstrip('0') + " " + label        
    precision, recall, _ = metrics.precision_recall_curve(Y_test, defun)    
    ax.plot(recall, precision, label=label)
    #ax.legend(fontsize='xx-small', loc=3) #, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
    ax.legend(loc=3) #, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)    
    #ax.fill_between(recall, precision, step='post', alpha=0.2, color='b')    
    ax.set_xlabel('recall')
    ax.set_ylabel('precision')
    ax.set_ylim([0.0, 1.0])
    ax.set_xlim([0.0, 1.0])
    #ax.xticks(())
    #ax.yticks(())
    #ax.title('{0}: P={1:0.2f} R={2:0.2f}'.format(label, pr, rc))
    #ax.text(0.9, 0.9, ('%.2f' % pr).lstrip('0'), size=15, horizontalalignment='right')

def clustervis_(ax, label, pipeline, projected, termvec, colors):
    ax.set_title(label)
    #ax.set_xticks(())
    #ax.set_yticks(())
    #ax.set_zticks(())
    ax.set_xlabel(compbottom(pipeline, termvec, 0) + '  -  ' + comptop(pipeline, termvec, 0))
    ax.set_ylabel(compbottom(pipeline, termvec, 1) + '  -  ' + comptop(pipeline, termvec, 1))
    ax.set_zlabel(compbottom(pipeline, termvec, 2) + '  -  ' + comptop(pipeline, termvec, 2))
    colorset = np.vectorize(lambda e: 'y' if e == 0 else 'b')(colors)    
    ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], c=colorset)
    #ax.scatter(projected[:, 0], projected[:, 1], alpha=.1, c=colorset)

def clustervis(ax, label, pipeline, projected, termvec, colors):    
    ax.set_xticks(())
    ax.set_yticks(())        
    ax.scatter(projected[:, 0], projected[:, 1], alpha=.5, c=colors)
    #ax.scatter(projected[:, 0], projected[:, 1], alpha=.1, c=colorset)

def clustervisTrue(ax, label, pipeline, projected, termvec, colors):    
    ax.set_xticks(())
    ax.set_yticks(())    
    ax.set_xlabel(compbottom(pipeline, termvec, 0) + '  -  ' + comptop(pipeline, termvec, 0))
    ax.set_ylabel(compbottom(pipeline, termvec, 1) + '  -  ' + comptop(pipeline, termvec, 1))
    #ax.set_zlabel(compbottom(pipeline, termvec, 2) + '  -  ' + comptop(pipeline, termvec, 2))
    #colorset = np.vectorize(lambda e: 'k' if e == 0 else 'r')(colors)        
    colors = np.array(colors)
    x = projected[:,0]
    y = projected[:,1]
    
    
    ax.scatter(x[colors==0], y[colors==0], alpha=.05, c='.15')    
    ax.scatter(x[colors==1], y[colors==1], alpha=.3, c='r')
    #ax.scatter(projected[:, 0], projected[:, 1], alpha=.1, c=colorset)


def top_words(component, feature_names, n_top_words):    
    return [feature_names[i] for i in component.argsort()[:-n_top_words - 1:-1]]
        
def bottom_words(component, feature_names, n_top_words):    
    return [feature_names[i] for i in component.argsort()[:n_top_words]]

def compbottom(pca, termvec, cidx):
    return " ".join(bottom_words(pca.named_steps['clu'].components_[cidx], termvec, 2))

def comptop(pca, termvec, cidx):
    return " ".join(top_words(pca.named_steps['clu'].components_[cidx], termvec, 2))


from scipy.cluster.hierarchy import dendrogram
def  fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)
    llf = kwargs.pop('leaf_label_func', None)
    n = len(ddata)

    #print(ddata['leaves'])
    #print(ddata['leaves'].shape)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        count = 0
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            count+=1            
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate(llf(n*2-1-count), (x, y), xytext=(0, 0),
                             textcoords='offset points',
                             va='top', ha='right', rotation=45, fontsize=7.)
        #if max_d:
        #    plt.axhline(y=max_d, c='k')
    return ddata
