import os
import sys
import math
import json
import ROOT
import random

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PDFWeights(Module):
    def __init__(self,pdfset,members,globalOptions={"isData":False}):
        self.pdfset = pdfset
        self.members = members
        self.globalOptions=globalOptions
        
    def beginJob(self):
        self.lha = ROOT.LHAInterface()
        self.lha.load(self.pdfset,self.members)
        
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for i in range(0,9):
            self.out.branch("scaleweight_%i"%i,"F")
        for i in range(0,self.members):
            self.out.branch("lheweight_%i"%i,"F")
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
            
    def analyze(self, event):
        q = event.Generator_scalePDF
        x1 = event.Generator_x1
        x2 = event.Generator_x2
        id1 = event.Generator_id1
        id2 = event.Generator_id2
        
        muF = self.lha.evalPDF(x1,q,id1)*self.lha.evalPDF(x2,q,id2)
        muR = self.lha.evalAlphas(q)**4 #(4 partons)
        #print muF,muR
        
        muFUp = self.lha.evalPDF(x1,2*q,id1)*self.lha.evalPDF(x2,2*q,id2)
        muFDown = self.lha.evalPDF(x1,0.5*q,id1)*self.lha.evalPDF(x2,0.5*q,id2)
        
        muRUp = self.lha.evalAlphas(2*q)**4
        muRDown = self.lha.evalAlphas(0.5*q)**4
        
        
        #override alphaS
        muR = 1
        muRUp = 1
        muRDown = 1
        
        '''
        LHE scale variation weights (w_var / w_nominal); 
        [0] is mur=0.5 muf=0.5 ; 
        [1] is mur=0.5 muf=1 ; 
        [2] is mur=0.5 muf=2 ; 
        [3] is mur=1 muf=0.5 ; 
        [4] is mur=1 muf=1 ; 
        [5] is mur=1 muf=2 ; 
        [6] is mur=2 muf=0.5 ; 
        [7] is mur=2 muf=1 ; 
        [8] is mur=2 muf=2
        '''
        
        self.out.fillBranch("scaleweight_0",muFDown*muRDown/muF/muR)
        self.out.fillBranch("scaleweight_1",muF*muRDown/muF/muR)
        self.out.fillBranch("scaleweight_2",muFUp*muRDown/muF/muR)
        
        self.out.fillBranch("scaleweight_3",muFDown*muR/muF/muR)
        self.out.fillBranch("scaleweight_4",muF*muR/muF/muR)
        self.out.fillBranch("scaleweight_5",muFUp*muR/muF/muR)
        
        self.out.fillBranch("scaleweight_6",muFDown*muRUp/muF/muR)
        self.out.fillBranch("scaleweight_7",muF*muRUp/muF/muR)
        self.out.fillBranch("scaleweight_8",muFUp*muRUp/muF/muR)
        
        pdfEv1 = self.lha.getEigenvalues(x1,q,id1)
        pdfEv2 = self.lha.getEigenvalues(x2,q,id2)
        
        for i in range(self.members):
            weight = pdfEv1[i]*pdfEv2[i]/pdfEv1[0]/pdfEv2[0]
            if weight>5. or weight<0.2:
                weight = 1.
            self.out.fillBranch("lheweight_%i"%i,weight)
                
        return True
