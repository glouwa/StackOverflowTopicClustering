from sklearn import metrics
import matplotlib.pyplot as plt

def precisionRecallPlot(ax, label, Y_test, Y_pred, defun):    
    pr = metrics.precision_score(Y_test, Y_pred)
    rc = metrics.recall_score(Y_test, Y_pred)
    label = ('%.2f' % pr).lstrip('0') + ' ' + ('%.2f' % rc).lstrip('0') + " " + label
    precision, recall, _ = metrics.precision_recall_curve(Y_test, defun)    
    ax.plot(recall, precision, label=label)
    #ax.fill_between(recall, precision, step='post', alpha=0.2, color='b')    
    ax.set_xlabel('recall')
    ax.set_ylabel('precision')
    ax.set_ylim([0.0, 1.0])
    ax.set_xlim([0.0, 1.0])
    #ax.xticks(())
    #ax.yticks(())
    #ax.title('{0}: P={1:0.2f} R={2:0.2f}'.format(label, pr, rc))
    #ax.text(0.9, 0.9, ('%.2f' % pr).lstrip('0'), size=15, horizontalalignment='right')


