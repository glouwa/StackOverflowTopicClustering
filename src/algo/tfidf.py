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

np.set_printoptions(threshold=np.nan)
np.set_printoptions(precision=3)
np.set_printoptions(linewidth=80)

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
    def __init__(self, docs, docraw, docstr, tfmode, idfmode):        
        self.documents = docs  #[d.split(' ') for d in doc] #np.array(list(map((lambda d: d.split(' ')), doc)))        
        self.termssorted = sorted(set(functools.reduce((lambda x, y: x+y), self.documents)))        
        """
        termdf = {}
        for d in self.documents:
            thisdoccounted = False
            for t in d:  
                if not thisdoccounted:
                    termdf[t] = termdf.get(t, 0) + 1
                    thisdoccounted = True

        termsfilterd = { k:v for k,v in termdf.items() if v > 2 }
        self.termssorted = list(sorted(termsfilterd.keys()))
        """        
        
        self.doctermRaw = np.zeros((len(self.termssorted), len(self.documents)))
        for didx, d in enumerate(self.documents):
            for t in d:    
                t_idx = self.termssorted.index(t)
                self.doctermRaw[t_idx][didx] = self.doctermRaw[t_idx][didx] + 1
        print("doctermshape", self.doctermRaw.shape)

        
        termfilter = np.sum(self.doctermRaw, axis=1) > 5
        print("tfilter", len(termfilter))
        self.doctermRaw = self.doctermRaw[termfilter]
        print("doctermshape", self.doctermRaw.shape)
                
        docfilter = np.sum(self.doctermRaw, axis=0) > 2
        print("dfilter", len(docfilter))
        self.doctermRaw = self.doctermRaw[:,docfilter]
        self.documentsraw_ = np.array(docraw)[docfilter]
        #self.documentsstr = np.array(docstr)[docfilter]
        self.documentsraw = docraw
        self.documentsstr = docstr
        """
        self.documentsraw_ = docraw        
        self.documentsraw = docraw
        self.documentsstr = docstr
        """
                
        self.termssorted = np.array(self.termssorted)[termfilter]        
        #print("new termshape", self.termssorted.shape)
        
        self.maxTermOccurence = np.max(self.doctermRaw.T, axis=1)  
        #print("strange", self.doctermRaw.T > 0)      
        self.doctermMax = sum(self.doctermRaw.T > 0)
        print("self.doctermMax", self.doctermMax.shape)
        #print("max", self.doctermMax)
        self.setTfIdfMode(tfmode, idfmode)

    def transform(self, rawdocs):
        return []

    def setTfIdfMode(self, tfmode, idfmode):
        print('# CalcWeights: {}, {}'.format(tfmode, idfmode)) 
        logbase = 10
        tfx = [
            self.doctermRaw,
            self.doctermRaw / self.maxTermOccurence,
            np.vectorize(lambda f: 0 if f==0 else 1.0)(self.doctermRaw),
            np.vectorize(lambda f: 1 + math.log(f, logbase) if f>0 else 0.0)(self.doctermRaw)
        ]        
        idfx = [
            np.vectorize(lambda ni: math.log(float(len(self.documents))/float(ni+1), logbase))(self.doctermMax),
            np.vectorize(lambda ni: math.log(1+len(self.documents)/float(ni+1), logbase))(self.doctermMax),
            np.zeros(len(self.termssorted))
        ]
        for i in range(len(self.termssorted)): 
            idfx[2][i] = math.log(1+max(self.doctermMax)/float(self.doctermMax[i]+1), logbase)
                
        self.tf = tfx[tfmode]
        self.idf = idfx[idfmode]
        self.w = (self.tf.T * self.idf).T        
        #plt.plot(self, None)
        return self.w
   
    def run(self, qstr):
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
    def __init__(self, file, feature, tfmode, idfmode):      
        """
        termsetfile = json.load(open('./dist/data/'+file+'-meta.json'))        
        termmap = termsetfile['distributions']['terms'][feature]['key']           
        termidx = {}
        termvec = []
        tid = 0
        for tkey, tvalue in termmap.items():
            termidx[tkey] = tid
            termvec.append(tkey)
            tid += 1
        """
        docmap = json.load(open('./dist/data/'+file+'.json'))        
        docarray = []        
        docarrayraw = []
        docarraystr = []
        docid = 0
        for dkey, _ in docmap.items():
            currentdocterms = []
            currentdocstr = []
            for f in feature:
                for sentence in docmap[dkey]['terms'][f]:            
                    currentdocstr.append(' '.join(sentence))
                    for term in sentence:
                        currentdocterms.append(term)
            docarray.append(currentdocterms)            
            docarraystr.append('. '.join(currentdocstr))
            docarrayraw.append(docmap[dkey])            
            docid += 1
        
        DocumentSpace.__init__(self, docarray, docarrayraw, docarraystr, tfmode, idfmode)

    def labels(self, tag):
        return [1 if tag in doc['terms']['tags'][0] else 0 for doc in self.documentsraw]

    def labels_(self, tag):
        return [1 if tag in doc['terms']['tags'][0] else 0 for doc in self.documentsraw_]
