import os
import sys
import math
import numpy as np
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
class_dict = {0:'b', 1:'c', 2:'ud', 3:'g', 4:'llp'}

if (ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")!=0):
    print "Cannot load 'libPhysicsToolsNanoAODTools'"
    sys.exit(1)

class XTagProducer(Module):
    def __init__(self, isData=False):
        pass
        
    def beginJob(self):
        self.nEvents = 0
        self.nLLPParam = {
            -3:0,
            0:0,
            3:0,
        }
        self.nLLPctau1 = 0
        self.nLLPTruth = 0
        
    def endJob(self):
        if self.nLLPTruth > 0:
            print "--- ctau1 ---"
            print "accuracy = %5.2f%%"%(100.*self.nLLPctau1/(self.nLLPTruth))
            #print "--- Parametric ---"
            #for ctau_value in self.nLLPParam.keys(): 
                #print "ctau=%3.1f, acc=%5.2f%%"%(ctau_value,100.*self.nLLPParam[ctau_value]/(self.nLLPTruth))
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.setup(inputTree)
        
    def setupTFEval(self,tree,modelFile,featureDict):
        tfEval = ROOT.TFEval()
        if (not tfEval.loadGraph(modelFile)):
            sys.exit(1)
            
        tfEval.addOutputNodeName("prediction")
        print "--- Model: ",modelFile," ---"
        for groupName,featureCfg in featureDict.iteritems():
            if featureCfg.has_key("max"):
                print "building group ... %s, shape=[%i,%i]"%(groupName,featureCfg["max"],len(featureCfg["branches"]))
                lengthBranch = ROOT.TFEval.BranchAccessor(tree.arrayReader(featureCfg["length"]))
                featureGroup = ROOT.TFEval.ArrayFeatureGroup(
                    groupName,
                    len(featureCfg["branches"]),
                    featureCfg["max"],
                    lengthBranch
                )
                for branchName in featureCfg["branches"]:
                    print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                tfEval.addFeatureGroup(featureGroup)
            else:
                print "building group ... %s, shape=[%i]"%(groupName,len(featureCfg["branches"]))
                featureGroup = ROOT.TFEval.ValueFeatureGroup(
                    groupName,
                    len(featureCfg["branches"])
                )
                for branchName in featureCfg["branches"]:
                    print " + add feature: ",branchName
                    featureGroup.addFeature(ROOT.TFEval.BranchAccessor(tree.arrayReader(branchName)))
                tfEval.addFeatureGroup(featureGroup)
                
        return tfEval
        
    def setup(self,tree):
        #load dynamically from file
        featureDict = import_module('feature_dict').featureDict
        self.tfEvalctau1 = self.setupTFEval(tree,"model2_ctau1.pb",featureDict)
        #self.tfEvalParametric = self.setupTFEval(tree,"model_parametric.pb",featureDict)
        
        genFeatureGroup = ROOT.TFEval.ValueFeatureGroup("gen",1)
        self.nJets = 0
        self.logctau = 0
        genFeatureGroup.addFeature(ROOT.TFEval.PyAccessor(lambda: self.nJets, lambda x: self.logctau))
        #self.tfEvalParametric.addFeatureGroup(genFeatureGroup)
        
        self._ttreereaderversion = tree._ttreereaderversion
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets = Collection(event, "Jet")
        jetorigin = Collection(event, "jetorigin")
        nTaggedJet = {0:0, 1:0, 2:0, 3:0, 4:0}

        threshold = 0.8
        threshold_b = 0.75

        scores = [0, 0, 0, 0, 0]
        
        for ijet in range(len(jetorigin)):

            if jetorigin[ijet].fromLLP > 0.5:  
                self.nLLPTruth+=1
                
            #NOTE: one cannot access any other branches between setup & call to evaluate
            if event._tree._ttreereaderversion > self._ttreereaderversion:
                self.setup(event._tree)
                    
            self.nJets = len(jets)
                
            resultCtau1 = self.tfEvalctau1.evaluate(ijet)
            predictedCtau1_class = np.argmax(resultCtau1.get("prediction"))
            predictedCtau1_score = resultCtau1.get("prediction")[predictedCtau1_class]

            #print resultCtau1.get("prediction")[0],resultCtau1.get("prediction")[1],resultCtau1.get("prediction")[2],resultCtau1.get("prediction")[3],resultCtau1.get("prediction")[4]
            
            #print predictedCtau1_class, predictedCtau1_score
            
            if (resultCtau1.get("prediction")[0] > threshold_b):
                nTaggedJet[0] += 1
             
            if (resultCtau1.get("prediction")[4] > threshold):
                nTaggedJet[4] += 1
    
            if predictedCtau1_class==4 and jetorigin[ijet].fromLLP > 0.5:
                self.nLLPctau1 +=1

            scores[0] = max(scores[0], resultCtau1.get("prediction")[0])
            scores[1] = max(scores[1], resultCtau1.get("prediction")[1])
            scores[2] = max(scores[2], resultCtau1.get("prediction")[2] + resultCtau1.get("prediction")[3])
            scores[3] = max(scores[3], resultCtau1.get("prediction")[4])

            #for ctau_value in self.nLLPParam.keys():
                #self.logctau = 1.*ctau_value
                #result = self.tfEvalParametric.evaluate(ijet)
                #prediction = result.gent("prediction")
                #predicted_class = np.argmax(prediction)
                #if predicted_class==4:
                    #self.nLLPParam[ctau_value]+=1
            #print "\n predicted class:", class_dict[predictedCtau1_class], "\n" #index 4 is LLP class
            
        #print nTaggedJet
        
        self.out.fillBranch("nbJets", nTaggedJet[0])
        #self.out.fillBranch("ncJets", nTaggedJet[1])
        #self.out.fillBranch("nudsgJets", nTaggedJet[2]+nTaggedJet[3])        
        self.out.fillBranch("nLLPJets", nTaggedJet[4])
        self.out.fillBranch("probLLP", scores[3])
        self.out.fillBranch("disc1LLP", 1./(1.-scores[3]+1e-5))
        self.out.fillBranch("disc2LLP", -math.log(1.-scores[3]+1e-5))
        self.out.fillBranch("probB", scores[0])
        self.out.fillBranch("probC", scores[1])
        self.out.fillBranch("probLight", scores[2])

        return True
 
class MuonSelection(Module):
    def __init__(self,isData=False):
        self.isData = isData
        
        self.tightPt = 26.
        self.tightEta = 2.4
        
        self.loosePt = 10.
        self.looseEta = 2.5
        
        if not self.isData:
            trackSFFile = ROOT.TFile("PhysicsTools/NanoAODTools/data/muon/track_EfficienciesAndSF_RunBtoH.root")
            self.trackSF = trackSFFile.Get("ratio_eff_aeta_dr030e030_corr")
            
            triggerSFBToF = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/trigger_EfficienciesAndSF_RunBtoF.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio"
            )
            triggerSFGToH = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/trigger_EfficienciesAndSF_RunGtoH.root",
                "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio"
            )
            self.triggerSFHist = self.combineHist2D(
                triggerSFBToF,
                triggerSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            
            idTightSFBToF = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunBtoF.root",
                "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
            )
            idTightSFGToH = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/id_EfficienciesAndSF_RunGtoH.root",
                "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio"
            )
            self.idTightSFHist = self.combineHist2D(
                idTightSFBToF,
                idTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
            
            
            isoTightSFBToF = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunBtoF.root",
                "TightISO_TightID_pt_eta/pt_abseta_ratio"
            )
            isoTightSFGToH = self.getHist(
                "PhysicsTools/NanoAODTools/data/muon/iso_EfficienciesAndSF_RunGtoH.root",
                "TightISO_TightID_pt_eta/pt_abseta_ratio"
            )
            self.isoTightSFHist = self.combineHist2D(
                isoTightSFBToF,
                isoTightSFGToH,
                1.-16226.5/35916.4,
                16226.5/35916.4
            )
 
    def getHist(self,relFileName,histName):
        rootFile = ROOT.TFile(os.path.expandvars("$CMSSW_BASE/src/"+relFileName))
        hist = rootFile.Get(histName)
        if not hist:
            raise Exception("Hist file '"+histName+"' not found in file '"+relFileName+"'")
        hist = hist.Clone(histName+str(random.random()))
        hist.SetDirectory(0)
        rootFile.Close()
        return hist
        
    def combineHist2D(self,hist1,hist2,w1,w2):
        result = hist1.Clone(hist1.GetName()+hist2.GetName())
        result.SetDirectory(0)
        for ibin in range(hist1.GetNbinsX()):
            for jbin in range(hist2.GetNbinsX()):
                result.SetBinContent(ibin+1,jbin+1,
                    w1*hist1.GetBinContent(ibin+1,jbin+1)+\
                    w2*hist2.GetBinContent(ibin+1,jbin+1)
                )
                result.SetBinError(ibin+1,jbin+1,
                    max([
                        hist1.GetBinContent(ibin+1,jbin+1),
                        hist2.GetBinContent(ibin+1,jbin+1)
                    ])
                )
        return result
        
    def getSFPtEta(self,hist,pt,eta):
        ptBin = hist.GetXaxis().FindBin(pt)
        etaBin = hist.GetYaxis().FindBin(math.fabs(eta))
        
        if ptBin==0:
            ptBin=1
        if ptBin>hist.GetNbinsX():
            ptBin=hist.GetNbinsX()
            
        if etaBin==0:
            etaBin = 1
        if etaBin>hist.GetNbinsY():
            etaBin=hist.GetNbinsY()
            
        return hist.GetBinContent(ptBin,etaBin),hist.GetBinError(ptBin,etaBin)
    
    
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree
        self.out.branch("nTightMuons","I")
        self.out.branch("nLooseMuons","I")
        self.out.branch("nLooseElectrons","I")
        
        self.out.branch("muon1_pt","F")
        self.out.branch("muon1_eta","F")
        
        self.out.branch("muon2_pt","F")
        self.out.branch("muon2_eta","F")
        
        self.out.branch("dimuon_mass","F")
        
        self.out.branch("IsoMu24","I")
        self.out.branch("IsoTkMu24","I")
        self.out.branch("Mu24_eta2p1","I")
        self.out.branch("TkMu24_eta2p1","I")

        self.out.branch("muon_trigger", "I")
        
        if not self.isData:
            self.out.branch("genweight","F")
        
        if not self.isData:
            self.out.branch("muon_track_weight", "F")
            self.out.branch("muon_trigger_weight", "F")
            self.out.branch("muon_iso_weight","F")
            self.out.branch("muon_id_weight","F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        #trigObjs = Collection(event, "TrigObj")
        if not self.isData:
            self.out.fillBranch("genweight",event.genWeight)
        #self.out.fillBranch("nsv",event.nSV)
        
        event.selectedMuons = {
            "tight":[],
            "loose":[],
            "weights":{
                "track":1.,
                "trigger":1.,
                "iso":1.,
                "id":1.
            }
        }
        
        #https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
        for muon in muons:
            if muon.pt>self.tightPt and math.fabs(muon.eta)<self.tightEta and muon.tightId==1 and muon.pfRelIso04_all<0.15:
                event.selectedMuons["tight"].append(muon)
                
                if not self.isData:
                    weight_id,weight_id_err = self.getSFPtEta(self.idTightSFHist,muon.pt,muon.eta)
                    weight_iso,weight_iso_err = self.getSFPtEta(self.isoTightSFHist,muon.pt,muon.eta)
                    event.selectedMuons["weights"]["id"]*=weight_id
                    event.selectedMuons["weights"]["iso"]*=weight_iso
                    event.selectedMuons["weights"]["track"]*=self.trackSF.Eval(math.fabs(muon.eta))
            
            #all muons in nanoaod are at least loose muons
            elif muon.pt>self.loosePt and math.fabs(muon.eta)<self.looseEta and muon.pfRelIso04_all<0.25:
                event.selectedMuons["loose"].append(muon)
            
        self.out.fillBranch("nTightMuons",len(event.selectedMuons["tight"]))
        self.out.fillBranch("nLooseMuons",len(event.selectedMuons["loose"]))
        
        if not self.isData and ((event.HLT_IsoMu24>0.5) or (event.HLT_IsoTkMu24>0.5)):
            #Note: for now assume hardest tight muon fired the trigger (may not be always correct)
            #TODO: matching this against trigger objects would be better
            if len(event.selectedMuons["tight"])>0:
                sf,err = self.getSFPtEta(self.triggerSFHist,event.selectedMuons["tight"][0].pt,math.fabs(event.selectedMuons["tight"][0].eta))
                event.selectedMuons["weights"]["trigger"]*=sf
        
        if not self.isData:
            self.out.fillBranch("muon_track_weight",event.selectedMuons["weights"]["track"])
            self.out.fillBranch("muon_trigger_weight",event.selectedMuons["weights"]["trigger"])
            self.out.fillBranch("muon_id_weight",event.selectedMuons["weights"]["id"])
            self.out.fillBranch("muon_iso_weight",event.selectedMuons["weights"]["iso"])
                
        muonsForKinematics = [] 
        if len(event.selectedMuons["tight"])>0:
            muonsForKinematics = event.selectedMuons["tight"]
        else:
            muonsForKinematics = muons
                
        if len(muonsForKinematics)>0:
            self.out.fillBranch("muon1_pt",muonsForKinematics[0].pt)
            self.out.fillBranch("muon1_eta",muonsForKinematics[0].eta)
        #else:
            #self.out.fillBranch("muon1_pt",0)
            #self.out.fillBranch("muon1_eta",0)
        
        if len(muonsForKinematics)>1:
            self.out.fillBranch("muon2_pt",muonsForKinematics[1].pt)
            self.out.fillBranch("muon2_eta",muonsForKinematics[1].eta)
            
            vec = ROOT.TLorentzVector(0,0,0,0)
            vec+=muonsForKinematics[0].p4()
            vec+=muonsForKinematics[1].p4()
            self.out.fillBranch("dimuon_mass",vec.M())
            
        #else:
            #self.out.fillBranch("muon2_pt",0)
            #self.out.fillBranch("muon2_eta",0)
            
            #self.out.fillBranch("dimuon_mass",0)
            
             
        if ((event.HLT_IsoMu24+event.HLT_IsoTkMu24)>0.5):
            self.out.fillBranch("muon_trigger",1)
        else:
            self.out.fillBranch("muon_trigger",0)
            
        self.out.fillBranch("IsoMu24",event.HLT_IsoMu24)
        self.out.fillBranch("IsoTkMu24",event.HLT_IsoTkMu24)
        self.out.fillBranch("Mu24_eta2p1",event.HLT_Mu24_eta2p1)
        self.out.fillBranch("TkMu24_eta2p1",event.HLT_TkMu24_eta2p1)
                   
        return True

class ElectronSelection(Module):
    def __init__(self,isData=False):
        self.isData = isData
        
        self.loosePt = 15.
        self.looseEta = 2.5
    
    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nLooseElectrons","I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        
        #TODO: make separate module for electron selection
        event.selectedElectrons = {"loose":[]}
        for electron in electrons:
            if electron.pt>self.loosePt and math.fabs(electron.eta)<self.looseEta and electron.cutBased>0:
                event.selectedElectrons["loose"].append(electron)

    	self.out.fillBranch("nLooseElectrons",len(event.selectedElectrons["loose"]))
        self.out.fillBranch("genweight",event.genWeight)

        return True

class JetSelection(Module):

    def __init__(self,isData=False,getLeptonCollection=lambda x:None):
        self.isData=isData
        self.getLeptonCollection = getLeptonCollection
        self.jetGroups = {
            "central":lambda jet: jet.jetId>0 and jet.pt>30. and math.fabs(jet.eta)<2.4,
            "all":lambda jet: jet.jetId>0 and ((jet.pt>30. and math.fabs(jet.eta)<2.4) or (jet.pt>50. and math.fabs(jet.eta)<5.0)),
        }

        
    def deltaPhi(self,phi1,phi2):
        res = phi1-phi2
        while (res>math.pi):
            res -= 2*math.pi
        while (res<=-math.pi):
            res += 2*math.pi
        return res 
        
    def deltaR(self,j1,j2):
        return math.sqrt(
            (j1.eta-j2.eta)**2+\
            self.deltaPhi(j1.phi,j2.phi)**2
        )
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("trigger", "I")
        self.out.branch("nsv", "I")
        self.out.branch("MET_phi", "F")
        self.out.branch("MET_pt", "F")
        
        for group in self.jetGroups.keys():

            self.out.branch("chEmEF_"+group, "F")
            self.out.branch("chHEF_"+group, "F")
            self.out.branch("neEmEF_"+group, "F")
            self.out.branch("neHEF_"+group, "F")
            self.out.branch("jetId_"+group, "I")
            self.out.branch("CHM_"+group,"I")
            self.out.branch("nConstituents_"+group, "I")
            self.out.branch("nSelectedJets_"+group,"I")
            self.out.branch("nLLPJets","I")
            self.out.branch("nbJets","I")
            self.out.branch("probLLP","F")
            self.out.branch("disc1LLP", "F")
            self.out.branch("disc2LLP", "F")
            self.out.branch("probB","F")
            self.out.branch("probC","F")
            self.out.branch("probLight","F")
            self.out.branch("ht_"+group,"F")
            self.out.branch("mht_"+group,"F")
            self.out.branch("mhtovermet_"+group,"F")
            self.out.branch("averagem_"+group,"F")
            self.out.branch("minPhi_"+group,"F")
            self.out.branch("minPhiL_"+group,"F")
            
            self.out.branch("alphaT_"+group,"F")
            self.out.branch("alphaTL_"+group,"F")
            self.out.branch("C_"+group,"F")
            self.out.branch("D_"+group,"F")
            self.out.branch("isotropy_"+group,"F")
            self.out.branch("sphericity_"+group,"F")
            
            self.out.branch("jet1_pt_"+group,"F")
            self.out.branch("jet1_eta_"+group,"F")
            self.out.branch("jet1_delta_phi_mht_"+group, "F")
            self.out.branch("jet2_pt_"+group,"F")
            self.out.branch("jet2_eta_"+group,"F")
            self.out.branch("jet2_delta_phi_mht_"+group, "F")
            self.out.branch("jet3_pt_"+group,"F")
            self.out.branch("jet3_eta_"+group,"F")
            self.out.branch("jet3_delta_phi_mht_"+group, "F")
            
            if not self.isData:
                self.out.branch("jet1_type_"+group,"I")
                self.out.branch("jet2_type_"+group,"I")
                self.out.branch("jet3_type_"+group,"I")
            
            '''
            if group.find("central")>=0:
                for nmax in range(0,4):
                    self.out.branch("max_llp"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_b"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_deepCSV"+str(nmax+1)+"_"+group,"F")
                    '''
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        if not self.isData:
            
            if not self.isData:
                self.out.branch("jet1_type_"+group,"I")
                self.out.branch("jet2_type_"+group,"I")
            
            '''
            if group.find("central")>=0:
                for nmax in range(0,4):
                    self.out.branch("max_llp"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_b"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_deepCSV"+str(nmax+1)+"_"+group,"F")
                    '''
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        if not self.isData:
            jetorigin = Collection(event, "jetorigin")
        
        event.selectedJets = {}
        
        for group,groupSelector in self.jetGroups.iteritems():
            event.selectedJets[group] = {
                "loose":[],
                "ht":0.0,
                "mht":0.0,
                "mhtovermet":0.0,
                "averagem":0.0,
                "minPhi":0.0,
                "minPhiL":0.0,
                
                "alphaT":0.0,
                "alphaTL":0.0,
                "isotropy":0.0,
                "sphericity":0.0,
                "C":0.0,
                "D":0.0,
            }
            vecsum = ROOT.TLorentzVector()
            eventShapes = ROOT.EventShapes()
            eventShapesL = ROOT.EventShapes()

            for ijet,jet in enumerate(jets):

                if groupSelector(jet):

                    #jet cleaning
                    leptons = self.getLeptonCollection(event)
                    if leptons!=None and len(leptons)>0:
                        mindr = min(map(lambda lepton: self.deltaR(lepton,jet),leptons))
                        if mindr<0.4:
                            continue

                    self.out.fillBranch("chEmEF_"+group, jet.chEmEF)
                    self.out.fillBranch("chHEF_"+group, jet.chHEF)
                    self.out.fillBranch("neEmEF_"+group, jet.neEmEF)
                    self.out.fillBranch("neHEF_"+group, jet.neHEF)
                    self.out.fillBranch("jetId_"+group, jet.jetId)
                    self.out.fillBranch("CHM_"+group, jet.CHM)
                    self.out.fillBranch("nConstituents_"+group, jet.nConstituents)
           
                    if not self.isData:
                        if ijet<len(jetorigin) and jetorigin[ijet].fromLLP:
                            jet.partonFlavour = 9 #override to indicate LLP jet
                                   
                    event.selectedJets[group]["loose"].append(jet)
                    eventShapes.addObject(jet.pt, jet.eta, jet.phi, jet.mass)
                    eventShapesL.addObject(jet.pt, jet.eta, jet.phi, jet.mass)
                    event.selectedJets[group]["ht"]+=jet.pt
                    vecsum += jet.p4()
                    event.selectedJets[group]["mht"] = vecsum.Pt()
                    event.selectedJets[group]["averagem"] = vecsum.Mag()/len(event.selectedJets[group]["loose"])
                    event.selectedJets[group]["mhtovermet"] = vecsum.Pt()/event.MET_pt

            if len(event.selectedJets[group]["loose"])>0:
                self.out.fillBranch("jet1_pt_"+group,event.selectedJets[group]["loose"][0].pt)
                self.out.fillBranch("jet1_eta_"+group,event.selectedJets[group]["loose"][0].eta)
                self.out.fillBranch("jet1_delta_phi_mht_"+group, abs(event.selectedJets[group]["loose"][0].p4().DeltaPhi(vecsum)))
                if not self.isData:
                    self.out.fillBranch("jet1_type_"+group,-1 if event.selectedJets[group]["loose"][0].genJetIdx<0 else abs(event.selectedJets[group]["loose"][0].partonFlavour))
            else:
                #self.out.fillBranch("jet1_pt_"+group,0)
                #self.out.fillBranch("jet1_eta_"+group,0)
                #self.out.fillBranch("jet1_delta_phi_mht_"+group, 0)
                if not self.isData:
                    self.out.fillBranch("jet1_type_"+group,0)
                    
            if len(event.selectedJets[group]["loose"])>1:
                self.out.fillBranch("jet2_pt_"+group,event.selectedJets[group]["loose"][1].pt)
                self.out.fillBranch("jet2_eta_"+group,event.selectedJets[group]["loose"][1].eta)
                self.out.fillBranch("jet2_delta_phi_mht_"+group, abs(event.selectedJets[group]["loose"][1].p4().DeltaPhi(vecsum)))
                if not self.isData:
                    self.out.fillBranch("jet2_type_"+group,-1 if event.selectedJets[group]["loose"][1].genJetIdx<0 else abs(event.selectedJets[group]["loose"][1].partonFlavour))
            else:
                #self.out.fillBranch("jet2_pt_"+group,0)
                #self.out.fillBranch("jet2_eta_"+group,0)
                #self.out.fillBranch("jet2_delta_phi_mht_"+group, 0)
                if not self.isData:
                    self.out.fillBranch("jet2_type_"+group,0)
                     
            if len(event.selectedJets[group]["loose"])>2:
                self.out.fillBranch("jet3_pt_"+group,event.selectedJets[group]["loose"][2].pt)
                self.out.fillBranch("jet3_eta_"+group,event.selectedJets[group]["loose"][2].eta)
                self.out.fillBranch("jet3_delta_phi_mht_"+group, abs(event.selectedJets[group]["loose"][2].p4().DeltaPhi(vecsum)))
                if not self.isData:
                    self.out.fillBranch("jet3_type_"+group,-1 if event.selectedJets[group]["loose"][2].genJetIdx<0 else abs(event.selectedJets[group]["loose"][2].partonFlavour))
            else:
                #self.out.fillBranch("jet3_pt_"+group,0)
                #self.out.fillBranch("jet3_eta_"+group,0)
                #self.out.fillBranch("jet3_delta_phi_mht_"+group, 0)
                if not self.isData:
                    self.out.fillBranch("jet3_type_"+group,0)
            
            if len(event.selectedJets[group]["loose"])>1:
                event.selectedJets[group]["alphaT"] = eventShapes.alphaT()
                event.selectedJets[group]["alphaTL"] = eventShapesL.alphaT()
                event.selectedJets[group]["isotropy"] = eventShapes.isotropy()
                event.selectedJets[group]["sphericity"] = eventShapes.sphericity()
                event.selectedJets[group]["C"] = eventShapes.C()
                event.selectedJets[group]["D"] = eventShapes.D()
                 
            self.out.fillBranch("alphaT_"+group,event.selectedJets[group]["alphaT"])
            self.out.fillBranch("alphaTL_"+group,event.selectedJets[group]["alphaTL"])
            self.out.fillBranch("isotropy_"+group,event.selectedJets[group]["isotropy"])
            self.out.fillBranch("sphericity_"+group,event.selectedJets[group]["sphericity"])
            self.out.fillBranch("C_"+group,event.selectedJets[group]["C"])
            self.out.fillBranch("D_"+group,event.selectedJets[group]["D"])
            
            minPhi = math.pi
            for jet in event.selectedJets[group]["loose"]:
                negSum = -(vecsum-jet.p4())
                minPhi = min(minPhi,math.fabs(self.deltaPhi(negSum.Phi(),jet.phi)))
            event.selectedJets[group]["minPhi"] = minPhi
            self.out.fillBranch("minPhi_"+group,minPhi)

            self.out.fillBranch("nSelectedJets_"+group,len(event.selectedJets[group]["loose"]))
            self.out.fillBranch("ht_"+group,event.selectedJets[group]["ht"])
            self.out.fillBranch("mht_"+group,event.selectedJets[group]["mht"])
            self.out.fillBranch("averagem_"+group,event.selectedJets[group]["averagem"])
            self.out.fillBranch("mhtovermet_"+group,event.selectedJets[group]["mhtovermet"])

        if event.HLT_PFMET120_PFMHT120_IDTight > 0.5:
            self.out.fillBranch("trigger", 1)
        else:
            self.out.fillBranch("trigger", 0)

        self.out.fillBranch("MET_pt", event.MET_pt)
        self.out.fillBranch("MET_phi", event.MET_phi)
            
        self.out.fillBranch("nsv", event.nSV)

        return True
 
                             
class EventSkim(Module):
    def __init__(self,selection=lambda event: True):
        self.selection = selection
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        return self.selection(event)
        
class METFilters(Module):
    def __init__(self,isData=False):
        self.isData=isData
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#Moriond_2017
        if event.Flag_goodVertices==0:
            return False
        if event.Flag_globalTightHalo2016Filter==0:
            return False
        if event.Flag_HBHENoiseFilter==0:
            return False
        if event.Flag_HBHENoiseIsoFilter==0:
            return False
        if event.Flag_EcalDeadCellTriggerPrimitiveFilter==0:
            return False
        if self.isData and event.Flag_eeBadScFilter==0: #not suggested on MC
            return False
        return True
      
class PileupWeight(Module):
    def __init__(self,isData=False,processName=None):
        self.mcFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/pileup.root")
        self.dataFile = os.path.expandvars("$CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/pu/PU69000.root")
        self.isData= isData
        self.processName = processName
        
    def beginJob(self):
        if not self.isData:
            self.mcHistPerProcess = {}
            fMC = ROOT.TFile(self.mcFile)
            if not fMC:
                print "ERROR: Cannot find pileup file: ",self.mcFile
                sys.exit(1)
            for k in fMC.GetListOfKeys():
                self.mcHistPerProcess[k.GetName()] = fMC.Get(k.GetName()).Clone(k.GetName())
                self.mcHistPerProcess[k.GetName()].SetDirectory(0)
            fMC.Close()
            
            fData = ROOT.TFile(self.dataFile)
            if not fData:
                print "ERROR: Cannot find pileup file: ",self.dataFile
                sys.exit(1)
                
            self.dataHist = fData.Get("pileup").Clone("pileup")
            self.dataHist.SetDirectory(0)
            self.normHist(self.dataHist)
        
    def getWeight(self,nTrueInteractions):
        mcBin = self.mcHist.FindBin(nTrueInteractions)
        dataBin = self.dataHist.FindBin(nTrueInteractions)
        w = self.dataHist.GetBinContent(dataBin)/(self.mcHist.GetBinContent(mcBin)+self.mcHist.Integral()*0.0001)
        if w>5.:
            w = 0
        return w
        
    def endJob(self):
        pass
        
    def normHist(self,hist):
        #normalization makes weight independent of binning scheme/range of histograms
        hist.Scale(1./hist.Integral())
        for ibin in range(hist.GetNbinsX()):
            w = hist.GetBinWidth(ibin+1)
            c = hist.GetBinContent(ibin+1)
            hist.SetBinContent(ibin+1,c/w)
                
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if not self.isData:
            self.mcHist = None
            for process in self.mcHistPerProcess.keys():
                processName = inputFile.GetName()
                if self.processName!=None:
                    processName = self.processName
                if processName.find(process)>=0:
                    self.mcHist = self.mcHistPerProcess[process]
                    break
            if self.mcHist==None:
                print "ERROR: Cannot find pileup profile for file: "+inputFile.GetName()
                sys.exit(1)
            self.normHist(self.mcHist)
                
        self.out = wrappedOutputTree
        self.out.branch("puweight","F")
        self.sum2 = 0
        self.sum = 0
        self.n = 0
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if not self.isData and self.n>0 and (self.sum2/(1.*self.n))>(self.sum**2/(1.*self.n**2)):
            avg = 1.*self.sum/self.n
            sig = math.sqrt(self.sum2/(1.*self.n)-self.sum**2/(1.*self.n**2))
            print "Average pileup weight: %6.3f +- %6.3f"%(avg,sig)
        
    def analyze(self, event):
        event.puWeight = 1.
        if not self.isData:
            event.puWeight = self.getWeight(event.Pileup_nTrueInt)
        self.n += 1
        self.sum+=event.puWeight
        self.sum2+=event.puWeight**2
        self.out.fillBranch("puweight",event.puWeight)
        return True

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--isData', dest='isData', action='store_true',default=False)
#parser.add_argument('--input', dest='inputFiles', action='append',default=[])
#parser.add_argument('output', nargs=1)
parser.add_argument('--job_id', dest='jobId', type=int)
parser.add_argument('--file_id', dest='fileId', type=int)

args = parser.parse_args()

txtFiles = sorted(os.listdir("/vols/build/cms/vc1117/CMSSW_10_2_0_pre6/src/samples"))
processDict = {}
pileupHists = {}

job_id = args.jobId
file_id = args.fileId

txtFile = txtFiles[job_id]
process = txtFile.split(".")[0]
print "-"*100
print "The process is:", process
print "-"*100

files = []

f = open ("/vols/build/cms/vc1117/CMSSW_10_2_0_pre6/src/samples/"+txtFile)
print "reading ",txtFile, "..."
for i, l in enumerate(f):
    if i == file_id:
        fileName = l.replace("\n","").replace("\r","")
        print "opening",fileName
        rootFile=None
        while (rootFile==None):
            rootFile = ROOT.TFile.Open(fileName)
        if not rootFile:
            print "Cannot found file: ",rootFile, "-> retry"
            continue
        else:
            files.append(fileName)

print files

print "isData:",args.isData

outputDir = os.path.join("/vols/cms/vc1117/LLP/SR", process)

print "output directory:", outputDir


p=PostProcessor(outputDir,[files],cut=None,branchsel=None,modules=[
#p=PostProcessor(args.output[0],[args.inputFiles],cut=None,branchsel=None,modules=[
    MuonSelection(isData=args.isData),
    ElectronSelection(isData=args.isData),
    JetSelection(isData=args.isData),
    EventSkim(selection=lambda event: event.trigger > 0.5 or event.muon_trigger > 0.5),
    EventSkim(selection=lambda event: len(event.selectedJets["central"]["loose"])>0),
	METFilters(isData=args.isData),
    EventSkim(selection=lambda event: len(event.selectedElectrons["loose"])==0),
    EventSkim(selection=lambda event: len(event.selectedMuons["loose"])==0),
    EventSkim(selection=lambda event: len(event.selectedMuons["tight"])==1 or len(event.selectedMuons["tight"]) == 2 or len(event.selectedMuons["tight"]) == 0),
    XTagProducer(isData=args.isData),
    PileupWeight(isData=args.isData,processName=process),
],friend=True)
p.run()
