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


    
    

class MuonSelection(Module):
    def __init__(self,isData=True):
        self.isData = isData
        
        self.tightPt = 26.
        self.tightEta = 2.1
        
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
        
        if not self.isData:
            self.out.branch("muon_trigger_weight", "F")
            self.out.branch("muon_iso_weight","F")
            self.out.branch("muon_id_weight","F")
                
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        #trigObjs = Collection(event, "TrigObj")
        
        event.selectedMuons = {
            "tight":[],
            "loose":[],
            "weights":{
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
                
            #all muons in nanoaod are at least loose muons
            elif muon.pt>self.loosePt and math.fabs(muon.eta)<self.looseEta and muon.pfRelIso04_all<0.25:
                event.selectedMuons["loose"].append(muon)
                
        if not self.isData and event.HLT_Mu24_eta2p1:
            #Note: for now assume hardest tight muon fired the trigger (may not be always correct)
            #TODO: matching this against trigger objects would be better
            if len(event.selectedMuons["tight"])>0:
                event.selectedMuons["weights"]["trigger"]*=self.trackSF.Eval(math.fabs(event.selectedMuons["tight"][0].eta))
        
        self.out.fillBranch("nTightMuons",len(event.selectedMuons["tight"]))
        self.out.fillBranch("nLooseMuons",len(event.selectedMuons["loose"]))
        if not self.isData:
            self.out.fillBranch("muon_trigger_weight",event.selectedMuons["weights"]["trigger"])
            self.out.fillBranch("muon_id_weight",event.selectedMuons["weights"]["id"])
            self.out.fillBranch("muon_iso_weight",event.selectedMuons["weights"]["iso"])
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
                "mht":0.0
            }
            vecsum = ROOT.TLorentzVector()
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
                    event.selectedJets[group]["ht"]+=jet.pt
                    vecsum += jet.p4()
            event.selectedJets[group]["mht"] = vecsum.Pt()
                    
                        
            self.out.fillBranch("nSelectedJets_"+group,len(event.selectedJets[group]["loose"]))
            self.out.fillBranch("ht_"+group,event.selectedJets[group]["ht"])
            self.out.fillBranch("mht_"+group,event.selectedJets[group]["mht"])
        return True
        
class JetTagging(Module):
    def __init__(self,isData=True,getJetCollection=lambda x:None):
        self.isData=isData
        self.getJetCollection = getJetCollection
        self.tagGroups = {
            "looseB":lambda jet: jet.isB>0.9
        }
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
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
        
        if not self.isData:
            event.jetTag = {
                "nTruePU":0,
                "nTrueB":0,
                "nTrueC":0,
                "nTrueUDS":0,
                "nTrueG":0,
                "nTrueLLP":0,
            }
            for jet in jets:
                if jet.genJetIdx<0:
                    event.jetTag["nTruePU"]+=1 
                if abs(jet.partonFlavour)==9:
                    event.jetTag["nTrueLLP"]+=1 
                elif abs(jet.hadronFlavour)==5:
                    event.jetTag["nTrueB"]+=1
                elif abs(jet.hadronFlavour)==4:
                    event.jetTag["nTrueC"]+=1
                elif abs(jet.partonFlavour)>0 and abs(jet.partonFlavour)<4:
                    event.jetTag["nTrueUDS"]+=1
                elif abs(jet.partonFlavour)==0:
                    event.jetTag["nTrueG"]+=1
                    
            self.out.fillBranch("nTruePU",event.jetTag["nTruePU"])
            self.out.fillBranch("nTrueB",event.jetTag["nTrueB"])
            self.out.fillBranch("nTrueC",event.jetTag["nTrueC"])
            self.out.fillBranch("nTrueUDS",event.jetTag["nTrueUDS"])
            self.out.fillBranch("nTrueG",event.jetTag["nTrueG"])
            self.out.fillBranch("nTrueLLP",event.jetTag["nTrueLLP"])
                    
        #self.out.fillBranch("nSelectedJets",len(event.selectedJets["loose"]))
        return True
     
        

class exampleProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass",  "F");
        self.out.branch("maxLLP",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        jetsTag = Collection(event, "llpdnnx")
        eventSum = ROOT.TLorentzVector()
        for lep in muons :
            eventSum += lep.p4()
        for lep in electrons :
            eventSum += lep.p4()
            
        nB = 0
        nLLP = 0
            
        maxLLP = -1
        for ijet,jet in enumerate(jets):
            eventSum += jet.p4()
            if ijet<len(jetsTag):
                if jetsTag[ijet].isLLP>maxLLP:
                    maxLLP = jetsTag[ijet].isLLP
                if jetsTag[ijet].isB>0.9:
                    nB+=1
                if jetsTag[ijet].isLLP>0.9:
                    nLLP+=1
        event.nB = nB
        event.nLLP = nLLP
                    
        self.out.fillBranch("EventMass",eventSum.M())
        self.out.fillBranch("maxLLP",maxLLP)
        return True
        
class categoryProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("cat",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        self.out.fillBranch("cat",event.nB*10+event.nLLP)
        return True

files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOX_180425-v2/180425_183459/0000/nano_6.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/nano_6.root.friend",
    ]
]

'''
files=[
    [
    "root://gfe02.grid.hep.ph.ic.ac.uk/pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mkomm/LLP/NANOX_180425-v2/SingleMuon_Run2016B-03Feb2017_ver2-v2/SingleMuon/Run2016B-03Feb2017_ver2-v2_NANOX_180425-v2/180425_185224/0000/nano_100.root",
    "/vols/cms/mkomm/LLP/NANOX_180425-v2_eval/SingleMuon_Run2016B-03Feb2017_ver2-v2/nano_100.root"
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
p=PostProcessor(".",files,cut=None,branchsel=None,modules=[
    MuonSelection(isData=False),
    JetSelection(isData=False,getLeptonCollection=lambda event: event.selectedMuons["tight"]),
    JetTagging(isData=False,getJetCollection=lambda event: event.selectedJets["central"]["loose"])
],friend=True)
p.run()
