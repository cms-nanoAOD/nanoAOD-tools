import os
import sys
import math
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

if (ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")!=0):
    print "Cannot load 'libPhysicsToolsNanoAODTools'"
    sys.exit(1)

class MuonSelection(Module):
    def __init__(self,isData=True):
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
        
        self.out.branch("met","F")
        
        self.out.branch("IsoMu24","I")
        self.out.branch("IsoTkMu24","I")
        self.out.branch("Mu24_eta2p1","I")
        self.out.branch("TkMu24_eta2p1","I")
        
        
        self.out.branch("trigger","I")
        if not self.isData:
            self.out.branch("genweight","F")
        
        #self.out.branch("nsv","I")
        
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
        
        self.out.fillBranch("met",event.MET_pt)
        

        
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

                
        #TODO: make separate module for electron selection
        event.selectedElectrons = {"loose":[]}
        for electron in electrons:
            if electron.pt>15 and math.fabs(electron.eta)<2.5 and electron.cutBased>0:
                event.selectedElectrons["loose"].append(electron)
        self.out.fillBranch("nLooseElectrons",len(event.selectedElectrons["loose"]))
                
        muonsForKinematics = [] 
        if len(event.selectedMuons["tight"])>0:
            muonsForKinematics = event.selectedMuons["tight"]
        else:
            muonsForKinematics = muons
                
        if len(muonsForKinematics)>0:
            self.out.fillBranch("muon1_pt",muonsForKinematics[0].pt)
            self.out.fillBranch("muon1_eta",muonsForKinematics[0].eta)
        else:
            self.out.fillBranch("muon1_pt",0)
            self.out.fillBranch("muon1_eta",0)
        
        if len(muonsForKinematics)>1:
            self.out.fillBranch("muon2_pt",muonsForKinematics[1].pt)
            self.out.fillBranch("muon2_eta",muonsForKinematics[1].eta)
            
            vec = ROOT.TLorentzVector(0,0,0,0)
            vec+=muonsForKinematics[0].p4()
            vec+=muonsForKinematics[1].p4()
            self.out.fillBranch("dimuon_mass",vec.M())
            
        else:
            self.out.fillBranch("muon2_pt",0)
            self.out.fillBranch("muon2_eta",0)
            
            self.out.fillBranch("dimuon_mass",0)
            
        self.out.fillBranch("met",event.MET_pt)
            
             
        if ((event.HLT_IsoMu24+event.HLT_IsoTkMu24)>0.5):
            self.out.fillBranch("trigger",1)
        else:
            self.out.fillBranch("trigger",0)
            
        self.out.fillBranch("IsoMu24",event.HLT_IsoMu24)
        self.out.fillBranch("IsoTkMu24",event.HLT_IsoTkMu24)
        self.out.fillBranch("Mu24_eta2p1",event.HLT_Mu24_eta2p1)
        self.out.fillBranch("TkMu24_eta2p1",event.HLT_TkMu24_eta2p1)
                   
        return True
        
        
class JetSelection(Module):
    def __init__(self,isData=True,getLeptonCollection=lambda x:None):
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
        
        for group in self.jetGroups.keys():
            self.out.branch("nSelectedJets_"+group,"I")
            self.out.branch("ht_"+group,"F")
            self.out.branch("mht_"+group,"F")
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
            self.out.branch("jet2_pt_"+group,"F")
            self.out.branch("jet2_eta_"+group,"F")
            
            if not self.isData:
                self.out.branch("jet1_type_"+group,"I")
                self.out.branch("jet2_type_"+group,"I")
            
            if group.find("central")>=0:
                for nmax in range(0,4):
                    self.out.branch("max_llp"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_b"+str(nmax+1)+"_"+group,"F")
                    self.out.branch("max_deepCSV"+str(nmax+1)+"_"+group,"F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        jettags = Collection(event, "llpdnnx")
        if not self.isData:
            jetorigin = Collection(event, "jetorigin")
        
        event.selectedJets = {}
        
        
        for group,groupSelector in self.jetGroups.iteritems():
            event.selectedJets[group] = {
                "loose":[],
                "ht":0.0,
                "mht":0.0,
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
            
            for muon in event.selectedMuons["tight"]:
                eventShapesL.addObject(muon.pt, muon.eta, muon.phi, muon.mass)
            
            for ijet,jet in enumerate(jets):
                if groupSelector(jet):
                    #jet cleaning
                    leptons = self.getLeptonCollection(event)
                    if leptons!=None and len(leptons)>0:
                        mindr = min(map(lambda lepton: self.deltaR(lepton,jet),leptons))
                        if mindr<0.4:
                            continue
                    
                    #put tag info into jets         
                    if ijet<len(jettags):
                        for flav in ["isB","isC","isUDS","isG","isLLP"]:
                            setattr(jet,"llpdnnx_"+flav,getattr(jettags[ijet],flav))   
                    else:
                        for flav in ["isB","isC","isUDS","isG","isLLP"]:
                            setattr(jet,"llpdnnx_"+flav,-1) 
                        
                    if not self.isData:
                        if ijet<len(jetorigin) and jetorigin[ijet].fromLLP:
                            jet.partonFlavour = 9 #override to indicate LLP jet
                       
                   
                            
                                   
                    event.selectedJets[group]["loose"].append(jet)
                    eventShapes.addObject(jet.pt, jet.eta, jet.phi, jet.mass)
                    eventShapesL.addObject(jet.pt, jet.eta, jet.phi, jet.mass)
                    event.selectedJets[group]["ht"]+=jet.pt
                    vecsum += jet.p4()
            event.selectedJets[group]["mht"] = vecsum.Pt()
            
            if len(event.selectedJets[group]["loose"])>0:
                self.out.fillBranch("jet1_pt_"+group,event.selectedJets[group]["loose"][0].pt)
                self.out.fillBranch("jet1_eta_"+group,event.selectedJets[group]["loose"][0].eta)
                if not self.isData:
                    self.out.fillBranch("jet1_type_"+group,-1 if event.selectedJets[group]["loose"][0].genJetIdx<0 else abs(event.selectedJets[group]["loose"][0].partonFlavour))
            else:
                self.out.fillBranch("jet1_pt_"+group,0)
                self.out.fillBranch("jet1_eta_"+group,0)
                if not self.isData:
                    self.out.fillBranch("jet1_type_"+group,0)
                    
            if len(event.selectedJets[group]["loose"])>1:
                self.out.fillBranch("jet2_pt_"+group,event.selectedJets[group]["loose"][1].pt)
                self.out.fillBranch("jet2_eta_"+group,event.selectedJets[group]["loose"][1].eta)
                if not self.isData:
                    self.out.fillBranch("jet2_type_"+group,-1 if event.selectedJets[group]["loose"][1].genJetIdx<0 else abs(event.selectedJets[group]["loose"][1].partonFlavour))
            else:
                self.out.fillBranch("jet2_pt_"+group,0)
                self.out.fillBranch("jet2_eta_"+group,0)
                if not self.isData:
                    self.out.fillBranch("jet2_type_"+group,0)
            
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
            
            minPhiL = math.pi
            for jet in event.selectedJets[group]["loose"]+event.selectedMuons["tight"]:
                negSum = -(vecsum-jet.p4())
                minPhiL = min(minPhiL,math.fabs(self.deltaPhi(negSum.Phi(),jet.phi)))
            event.selectedJets[group]["minPhiL"] = minPhiL
            self.out.fillBranch("minPhiL_"+group,minPhiL)
            
            if group.find("central")>=0:
                jetsByLLP = sorted(map(lambda j:j.llpdnnx_isLLP,event.selectedJets[group]["loose"]),reverse=True)
                jetsByB = sorted(map(lambda j:j.llpdnnx_isB,event.selectedJets[group]["loose"]),reverse=True)
                jetsByDeepCSV = sorted(map(lambda j:j.btagCSVV2 if j.btagCSVV2>0 else -1,event.selectedJets[group]["loose"]),reverse=True)
                
                for nmax in range(0,4):
                    if len(event.selectedJets[group]["loose"])>=(nmax+1):
                        self.out.fillBranch("max_llp"+str(nmax+1)+"_"+group,jetsByLLP[nmax])
                        self.out.fillBranch("max_b"+str(nmax+1)+"_"+group,jetsByB[nmax])
                        self.out.fillBranch("max_deepCSV"+str(nmax+1)+"_"+group,jetsByDeepCSV[nmax])
                    else:
                        self.out.fillBranch("max_llp"+str(nmax+1)+"_"+group,-1)
                        self.out.fillBranch("max_b"+str(nmax+1)+"_"+group,-1)
                        self.out.fillBranch("max_deepCSV"+str(nmax+1)+"_"+group,-1)
            
            self.out.fillBranch("nSelectedJets_"+group,len(event.selectedJets[group]["loose"]))
            self.out.fillBranch("ht_"+group,event.selectedJets[group]["ht"])
            self.out.fillBranch("mht_"+group,event.selectedJets[group]["mht"])
        return True
        
class JetTagging(Module):
    def __init__(self,isData=True,getJetCollection=lambda x:None):
        self.isData=isData
        self.getJetCollection = getJetCollection
        self.tagGroups = {
            "looseDeepCSV":lambda jet: jet.btagCSVV2>0.2219,
            "mediumDeepCSV":lambda jet: jet.btagCSVV2>0.6324,
            "tightDeepCSV":lambda jet: jet.btagCSVV2>0.8958,
        
            "looseLLP":lambda jet: jet.llpdnnx_isLLP>0.0400, #eff: 86% @ 1/10 bkg
            "mediumLLP":lambda jet: jet.llpdnnx_isLLP>0.1483, #eff: 71% @ 1/100 bkg
            "tightLLP":lambda jet: jet.llpdnnx_isLLP>0.5123, #eff: 60% @ 1/1000 bkg
            "ultraLLP":lambda jet: jet.llpdnnx_isLLP>0.8043, #eff: 52% @ 1/10000 bkg
            
            "looseB":lambda jet: jet.llpdnnx_isB>0.0381, #eff: 88% @ 1/10 bkg
            "mediumB":lambda jet: jet.llpdnnx_isB>0.1499, #eff: 73% @ 1/100 bkg
            "tightB":lambda jet: jet.llpdnnx_isB>0.3741, #eff: 52% @ 1/1000 bkg
            "ultraB":lambda jet: jet.llpdnnx_isB>0.6858, #eff: 31% @ 1/10000 bkg
        }
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for tagGroup in self.tagGroups.keys():
            self.out.branch("n"+tagGroup,"I")
        
        if not self.isData:
            self.out.branch("nTruePU","I")
            self.out.branch("nTrueB","I")
            self.out.branch("nTrueC","I")
            self.out.branch("nTrueUDS","I")
            self.out.branch("nTrueG","I")
            self.out.branch("nTrueLLP","I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = self.getJetCollection(event)
        if jets==None:
            return True
            
        event.jetTag = {}
        
        if not self.isData:
            event.jetTagTruth = {
                "nTruePU":0,
                "nTrueB":0,
                "nTrueC":0,
                "nTrueUDS":0,
                "nTrueG":0,
                "nTrueLLP":0,
            }
            
        for tagGroup in self.tagGroups.keys():
            event.jetTag[tagGroup] = 0
            
        for jet in jets:
            for tagGroup,groupSelector in self.tagGroups.iteritems():
                if groupSelector(jet):
                    event.jetTag[tagGroup] += 1
            if not self.isData:
                if jet.genJetIdx<0:
                    event.jetTagTruth["nTruePU"]+=1 
                if abs(jet.partonFlavour)==9:
                    event.jetTagTruth["nTrueLLP"]+=1 
                elif abs(jet.hadronFlavour)==5:
                    event.jetTagTruth["nTrueB"]+=1
                elif abs(jet.hadronFlavour)==4:
                    event.jetTagTruth["nTrueC"]+=1
                elif abs(jet.partonFlavour)>0 and abs(jet.partonFlavour)<4:
                    event.jetTagTruth["nTrueUDS"]+=1
                elif abs(jet.partonFlavour)==0 or abs(jet.partonFlavour)==21:
                    event.jetTagTruth["nTrueG"]+=1
                        
        for tagGroup in self.tagGroups.keys():
            self.out.fillBranch("n"+tagGroup,event.jetTag[tagGroup])
        
                  
        if not self.isData:               
            self.out.fillBranch("nTruePU",event.jetTagTruth["nTruePU"])
            self.out.fillBranch("nTrueB",event.jetTagTruth["nTrueB"])
            self.out.fillBranch("nTrueC",event.jetTagTruth["nTrueC"])
            self.out.fillBranch("nTrueUDS",event.jetTagTruth["nTrueUDS"])
            self.out.fillBranch("nTrueG",event.jetTagTruth["nTrueG"])
            self.out.fillBranch("nTrueLLP",event.jetTagTruth["nTrueLLP"])
                
            
            
        
                    
        #self.out.fillBranch("nSelectedJets",len(event.selectedJets["loose"]))
        return True
     
class PileupWeight(Module):
    def __init__(self,isData=True):
        self.mcFile = "/vols/build/cms/mkomm/LLP/CMSSW_10_2_0_pre2/src/data/pileup.root"
        self.dataFile = "/vols/build/cms/mkomm/LLP/CMSSW_10_2_0_pre2/src/data/PU69000.root"
        self.isData= isData
        
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
            for process in self.mcHistPerProcess.keys():
                if inputFile.GetName().find(process)>=0:
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
    def __init__(self,isData=True):
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
      
        
'''
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOX_180425-v2/180425_183459/0000/nano_6.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/nano_6.root.friend",
    ]
]
'''
'''
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SingleMuon_Run2016B-03Feb2017_ver2-v2/SingleMuon/Run2016B-03Feb2017_ver2-v2_NANOX_180425-v2/180425_185224/0000/nano_100.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SingleMuon_Run2016B-03Feb2017_ver2-v2/nano_100.root.friend"
    ]
]
'''
'''
files = [
    [
        "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOX_180425-v2/180425_182750/0000/nano_100.root",
        "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/nano_100.root.friend",
    ]
]
'''

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--isData', dest='isData', action='store_true',default=False)
parser.add_argument('--input', dest='inputFiles', action='append',default=[])
parser.add_argument('output', nargs=1)

args = parser.parse_args()

print "isData:",args.isData
print "inputs:",len(args.inputFiles)
for inputFile in args.inputFiles:
    rootFile = ROOT.TFile.Open(inputFile)
    if not rootFile:
        print "CRITICAL - file '"+inputFile+"' not found!"
        sys.exit(1)
    tree = rootFile.Get("Events")
    if not tree:
        print "CRITICAL - 'Events' tree not found in file '"+inputFile+"'!"
        sys.exit(1)
    print " - ",inputFile,", events=",tree.GetEntries()
    
print "output directory:",args.output[0]

p=PostProcessor(args.output[0],[args.inputFiles],cut=None,branchsel=None,modules=[
    #EventSkim(selection=lambda event: event.HLT_IsoMu24 or event.HLT_IsoTkMu24),
    MuonSelection(isData=args.isData),
    EventSkim(selection=lambda event: len(event.selectedMuons["tight"])>0),
    PileupWeight(isData=args.isData),
    JetSelection(isData=args.isData,getLeptonCollection=lambda event: event.selectedMuons["tight"]),
    EventSkim(selection=lambda event: len(event.selectedJets["all"]["loose"])>=3),
    JetTagging(isData=args.isData,getJetCollection=lambda event: event.selectedJets["central"]["loose"]),
    METFilters(isData=args.isData)
],friend=True)
p.run()


