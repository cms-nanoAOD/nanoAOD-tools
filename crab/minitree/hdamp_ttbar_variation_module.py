##https://twiki.cern.ch/twiki/bin/viewauth/CMS/MLReweighting
import onnxruntime as ort
import ROOT
import numpy as np
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e

def rapidity (eta, mass, pt):
        y = 0.5 * math.log((math.sqrt(mass**2 + pt**2 * math.cosh(eta)**2) + pt * math.sinh(eta)) / (math.sqrt(mass**2 + pt**2 * math.cosh(eta)**2) - pt * math.sinh(eta)))
        return y

class hdampproducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("hdamp_Up","F")
        self.out.branch("hdamp_Down","F")
        self.out.branch("Top_quark_count","I")
        ## create inference session using ort.InferenceSession from a given model
        self.ort_sess_Down = ort.InferenceSession('Onnx_Model/model12Down.onnx',providers=['CPUExecutionProvider'])
        self.ort_sess_Up = ort.InferenceSession('Onnx_Model/model12Up.onnx',providers=['CPUExecutionProvider'])
        self.input_name = self.ort_sess_Down.get_inputs()[0].name
        self.label_name = self.ort_sess_Down.get_outputs()[0].name
        
        ##Values that you have to set
        self.hdamp = 1.379 ##This value is the value of hdamp of your NanoAOD divided by 172.5
        self.maxM =  243.9517 ##This value is needed to normalise the mass of the particles in each event and comes from the maximum mass value we had in the training+validation sample

        # PDGid to small float dictionary
        self.PID2FLOAT_MAP = {21: 0,
                        6: .1, -6: .2,
                        5: .3, -5: .4,
                        4: .5, -4: .6,
                        3: .7, -3: .8,
                        2: 0.9, -2: 1.0,
                        1: 1.1, -1: 1.2}


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    ##Def of rapidity
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # Get the desired arrays from the data
        Genparts = Collection(event,"GenPart")
        GenPart_pdgId,GenPart_statusFlags,GenPart_pt,GenPart_phi,GenPart_eta,GenPart_mass = ([] for i in range(6))
        for genpart in Genparts:
            GenPart_statusFlags.append(genpart.statusFlags)
            GenPart_pt.append(genpart.pt)
            GenPart_phi.append(genpart.phi)
            GenPart_eta.append(genpart.eta)
            GenPart_mass.append(genpart.mass)
            GenPart_pdgId.append(genpart.pdgId)

        #print(GenPart_pdgId)
        countTop = 0
        ptop = ROOT.TLorentzVector()
        patop = ROOT.TLorentzVector()

        for i in range(0, len(GenPart_pdgId)):
            if GenPart_pdgId[i] == 6:

                if (((GenPart_statusFlags[i] >> 12) & 0x1) > 0):
                    countTop += 1
                    ptop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i])
            
            if GenPart_pdgId[i] == -6:

                if (((GenPart_statusFlags[i] >> 12) & 0x1) > 0):
                    countTop += 1
                    patop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i])
        
            # Creating the array with all info needed to pass to the NN model, already normalised
        particlesvector=[]
        P0 = []
        particlesvector.append([math.log10(ptop.Pt()), rapidity(ptop.Eta(), ptop.M(), ptop.Pt()), ptop.Phi(), ptop.M()/self.maxM, self.PID2FLOAT_MAP.get(6, 0), self.hdamp])
        particlesvector.append([math.log10(patop.Pt()), rapidity(patop.Eta(), patop.M(), patop.Pt()), patop.Phi(), patop.M()/self.maxM, self.PID2FLOAT_MAP.get(6, 0), self.hdamp])
        P0.append(particlesvector)
        P0=np.array(P0)
        #print(P0.shape)
        #print(P0)

        p_tt = ptop + patop

        ## run inference
        pred_Down = self.ort_sess_Down.run([self.label_name], {self.input_name: P0.astype(np.float32)})[0]
        pred_Up = self.ort_sess_Up.run([self.label_name], {self.input_name: P0.astype(np.float32)})[0]
        if (p_tt.Pt()<1000):
            weight_Down = pred_Down[:,0]/pred_Down[:,1]
            weight_Up = pred_Up[:,0]/pred_Up[:,1]
        else:
            weight_Down = [1.0]
            weight_Up = [1.0]
     
        #print('countTop:'+str(countTop)+"weoght Up: %s Down: %s"%(weight_Up[0],weight_Down[0]))
        #print("/n---------------------------------------------------/n")

        self.out.fillBranch("hdamp_Up",weight_Up[0])
        self.out.fillBranch("hdamp_Down",weight_Down[0])
        self.out.fillBranch("Top_quark_count",countTop)

        return True

hdamp_vari_mainModule = lambda : hdampproducer()    