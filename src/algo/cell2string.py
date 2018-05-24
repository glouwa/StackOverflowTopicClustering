import os, time
import pandas as py
from sklearn.externals import joblib
import datetime

def none(frame):     
    #result = frame.copy
    frame[:] = '-'    
    return frame

def file2date(frame):
    def timediff(file):
        return str(time.ctime(os.path.getmtime(file))) if os.path.exists(file) else '-'
    return file2(frame.copy(), timediff)

def file2shape(frame):
    def loadshape(file):
        return str(joblib.load(file).shape)
    return file2(frame.copy(), loadshape)

def file2age(frame):
    def loadshape(file):
        ftime = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        delta = datetime.datetime.now() - ftime
        return str(time.ctime(delta))
    return file2(frame.copy(), loadshape)

def file2size(frame):
    def sizestr(file):
        return str(os.path.getsize(file))
    return file2(frame.copy(), sizestr)

def file2(frame, what):
    for row in frame.index.values:   
        path = './dist/data/'+'/'.join(row) + '/'        
        for col in frame.columns:
            colname = col
            filename = path + colname + '.pkl'
            if os.path.exists(filename):
                frame.loc[row,colname] = what(filename)        
            else:
                frame.loc[row,col] = '-'        
    return frame

