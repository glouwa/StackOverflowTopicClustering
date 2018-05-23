#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: glouwa
"""
import math
import json
import functools
import numpy as np
#import plt
"""
np.set_printoptions(threshold=np.nan)
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=80)
"""
class DocumentSpace:
    documents=None
    documentsraw=None
    documentsstr=None
    documentcount=None
    termssorted=None    
    doctermRaw=None    
    doctermMax=None
    maxTermOccurence=None       
    tf=None 
    idf=None 
    w=None
    def __init__(self, docs, docraw, docstr, tfmode, idfmode, mindf, mintf):        
        self.documents = docs  #[d.split(' ') for d in doc] #np.array(list(map((lambda d: d.split(' ')), doc)))        
        #self.termssorted = sorted(set(functools.reduce((lambda x, y: x+y), self.documents)))        
        termf = {}
        for d in self.documents:            
            for t in d:                  
                termf[t] = termf.get(t, 0) + 1
        
        termsfilterd = { k:v for k,v in termf.items() if v > mintf }
        self.termssorted = list(sorted(termsfilterd.keys()))
                
        self.doctermRaw = np.zeros((len(self.termssorted), len(self.documents)))
        for didx, d in enumerate(self.documents):
            for t in d:  
                if t in self.termssorted:  
                    t_idx = self.termssorted.index(t)
                    self.doctermRaw[t_idx][didx] = self.doctermRaw[t_idx][didx] + 1
        #print(self.doctermRaw.T.shape, "rawdoctermshape")
        
        termfilter = (sum(self.doctermRaw.T > 0) > mindf) & (np.sum(self.doctermRaw, axis=1) > mintf) 
        #print("tfilter", len(termfilter))
        self.doctermRaw = self.doctermRaw[termfilter]
        #print("doctermshape", self.doctermRaw.shape)
                
        docfilter = (sum(self.doctermRaw > 0) > mindf) #np.sum(self.doctermRaw, axis=0) > 5 # sum(self.doctermRaw.T > 0) > 5
        #print("dfilter", len(docfilter))
        self.doctermRaw = self.doctermRaw[:,docfilter]
        self.documentsraw_ = np.array(docraw)[docfilter]
        #self.documentsstr = np.array(docstr)[docfilter]
        #self.documentsraw = docraw
        #self.documentsstr = docstr
                
        self.termssorted = np.array(self.termssorted)[termfilter]        
        #print("new termshape", self.termssorted.shape)
        
        self.maxTermOccurence = np.max(self.doctermRaw.T, axis=1)  
        #print("strange", self.doctermRaw.T > 0)      
        self.doctermMax = sum(self.doctermRaw.T > 0)
        #print("self.doctermMax", self.doctermMax.shape)
        #print("max", self.doctermMax)
        self.setTfIdfMode(tfmode, idfmode)

    def transform(self, rawdocs):
        return []

    def setTfIdfMode(self, tfmode, idfmode):
        #print('# CalcWeights: {}, {}'.format(tfmode, idfmode)) 
        logbase = 10
        dz = 1
        tfx = [
            self.doctermRaw,
            self.doctermRaw / self.maxTermOccurence,
            np.vectorize(lambda f: 0 if f==0 else 1.0)(self.doctermRaw),
            np.vectorize(lambda f: 1 + math.log(f, logbase) if f>0 else 0.0)(self.doctermRaw)
        ]        
        idfx = [
            np.vectorize(lambda ni: math.log(float(len(self.documents))/float(ni+dz), logbase))(self.doctermMax),
            np.vectorize(lambda ni: math.log(1+len(self.documents)/float(ni+dz), logbase))(self.doctermMax),
            np.zeros(len(self.termssorted))
        ]
        for i in range(len(self.termssorted)): 
            idfx[2][i] = math.log(1+max(self.doctermMax)/float(self.doctermMax[i]+dz), logbase)
                
        self.tf = tfx[tfmode]
        self.idf = idfx[idfmode]
        self.w = (self.tf.T * self.idf).T        
        #plt.plot(self, None)
        return self.w
   
    def query(self, qstr):
        print('# Query: {}'.format(qstr)) 
        qarr = qstr.split(' ')
        q = np.zeros((len(self.termssorted)))
        for qi in range(len(qarr)):                
            if (qarr[qi] in self.termssorted):
                t_idx = self.termssorted.index(qarr[qi])
                q[t_idx] = self.idf[t_idx]        
        res = np.zeros((len(self.documents)))
        for d in range(len(self.documents)):
            res[d] = np.dot(self.w.T[d],q) / np.linalg.norm(self.w.T[d]) / np.linalg.norm(q)
        #plt.plot(self, res)
        return res
    
    def summary(self):
        print("Document terms", self.documents)
        print("Document count", self.documentcount)        
        print("Alpha sorted terms", self.termssorted)
        print("Term count", len(self.termssorted))        
        print("DocTerm binary", self.doctermMax)
        print("Final weights", self.w)

class StackoverflowCorpus(DocumentSpace):    
    def __init__(self, file, feature, tfmode, idfmode, mindf, mintf):       
        docmap = json.load(open('./dist/data/'+file+'.json'))        
        docarray = []        
        docarrayraw = []
        docarraystr = []
        docid = 0
        for dkey, _ in docmap.items():
            currentdocterms = []
            #currentdocstr = []
            for f in feature:
                for sentence in docmap[dkey]['terms'][f]:            
                    #currentdocstr.append(' '.join(sentence))
                    for term in sentence:
                        currentdocterms.append(term)
            docarray.append(currentdocterms)            
            #docarraystr.append('. '.join(currentdocstr))
            docarrayraw.append(docmap[dkey])            
            docid += 1
        
        DocumentSpace.__init__(self, docarray, docarrayraw, docarraystr, tfmode, idfmode, mindf, mintf)

    def labelstr(self):
        return [1 if tag in doc['terms']['tags'][0] else 0 for doc in self.documentsraw_]

    def labels(self, tag):
        return [1 if tag in doc['terms']['tags'][0] else 0 for doc in self.documentsraw]

    def labels_(self, tag):
        return [1 if tag in doc['terms']['tags'][0] else 0 for doc in self.documentsraw_]
