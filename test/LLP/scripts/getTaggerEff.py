import ROOT
import numpy
import random
import math
import os
import re
import json
import uproot

fileList = []

filePath = "/vols/cms/mkomm/LLP/NANOX_SR"


extensions = {
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8":"WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8_ext3":"WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext1":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext2":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8_ext3":"WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
    
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4":"DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",

    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4":"DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",

    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":"DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1":"DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",    

}

xsecs = {

    # Drell-Yan + jets
    # NLO
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z
    "DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":169.9*1.23,
    "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":147.40*1.23,
    "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":40.99*1.23,
    "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":5.678*1.23,
    "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1.367*1.23,
    "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.6304*1.23,
    "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.1514*1.23,
    "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":0.003565*1.23,
    
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":18610,
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":1921.8*3,
    
    # QCD (multijet)
    # LO
    "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":27990000.,
    "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1712000.,
    "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":347700.,
    "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":32100.,
    "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":6831.,
    "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":1207.,
    "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":119.9,
    "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":25.24,
    
    #https://cms-pdmv.cern.ch/mcm/requests?page=-1&dataset_name=QCD_Pt_*to*_TuneCUETP8M1_13TeV_pythia8&member_of_campaign=RunIIFall14GS
    "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8":140932000,
    "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8":19204300,
    "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8":2762530,
    "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8":471100,
    "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8":117276,
    "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8":7823,
    "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8":648.2,
    "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8":186.9,
    "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8":32.293,
    "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8":9.4183,
    "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8":0.84265,
    "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8":0.114943,
    "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8":0.00682981,
    "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8":0.000165445,
    
    
    # Single-top
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_t_channel_cross_secti
    # NLO
    "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": 10.32,
    "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1": 80.95,
    "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1": 136.02,
    "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": 71.7/2.,
    "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": 71.7/2.,
    
    # TTbar
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (mtop=172.5 GeV)
    # missing
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-evtgen": 831.76,
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8": 831.76,
    # NLO
    "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76,
    # LO
    "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 831.76,
    "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 2.666535,
    "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1.098082,
    "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.198748, 
    "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.002368413,
    "TTJets_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76*0.5*(1-3*0.1086)*(3*0.1086)*2,
    "TTJets_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8": 831.76*0.5*(1-3*0.1086)*(3*0.1086)*2,

    # W->l nu + jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    # NLO
    "WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1319,#*1.21, 
    "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1345,#*1.21, 
    "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 359.7,#*1.21, 
    "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 48.91,#*1.21, 
    "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 12.05,#*1.21, 
    "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 5.501,#*1.21, 
    "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 1.329,#*1.21, 
    "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.03216,#*1.21, 
    
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8": 49670.,
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8": 8264.,
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8": 3226.,
    
    # Z -> nu nu + jets
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    # LO
    "ZJetsToNuNu_HT-100To200_13TeV-madgraph": 280.35*1.23 ,
    "ZJetsToNuNu_HT-200To400_13TeV-madgraph": 77.67*1.23 ,
    "ZJetsToNuNu_HT-400To600_13TeV-madgraph": 10.73*1.23 ,
    "ZJetsToNuNu_HT-600To800_13TeV-madgraph": 2.559*1.23 ,
    "ZJetsToNuNu_HT-800to1200_13TeV-madgraph": 1.1796*1.23 ,
    "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph": 0.28833*1.23 ,
    "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph": 0.006945*1.23 ,
    
    # Z -> nu nu + jets
    # MCM
    # NLO
    "DYJetsToNuNu_Zpt-0To50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 3483.*3,
    "DYJetsToNuNu_PtZ-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 593.9*3,
    "DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 55.03*3,
    "DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 2.082*3,
    "DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 0.2816*3,
    "DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 0.02639*3,
    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
    # NNLO
    "WW_TuneCUETP8M1_13TeV-pythia8": 118.7,
    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    # NLO
    "WZ_TuneCUETP8M1_13TeV-pythia8": 47.13,
    "ZZ_TuneCUETP8M1_13TeV-pythia8": 16.523,
}

with open('eventyields.json',) as f:
    genweights = json.load(f)
    
processDict = {}

for processFolder in os.listdir(filePath):
    print "reading ",processFolder,"...",
    processName = processFolder
    if extensions.has_key(processFolder):
        processName = extensions[processFolder]
        
    if not processDict.has_key(processName):
        processDict[processName] = {
            "files":[],
            "weight":"weightnotfound",
            "xsec":0,
            "integral":0
        }
    for f in os.listdir(os.path.join(filePath,processFolder)):
        fullFilePath = os.path.join(filePath,processFolder,f)
        '''
        if not f.endswith(".root"):
            continue
        
        rootFile = ROOT.TFile(fullFilePath)
        if not rootFile:
            continue
        tree = rootFile.Get("Friends")
        if not tree:
            continue
        '''
        
        
        processDict[processName]["files"].append(fullFilePath)
        '''
        if tree.FindBranch("genweight"):
            h = ROOT.TH1F("nevents"+processFolder+f,"",1,-1,1)
            tree.Project(h.GetName(),"0","genweight")
            processDict[processFolder]["nevents"]+=tree.GetEntries()
            processDict[processFolder]["integral"]+=h.Integral()
        else:
            processDict[processFolder]["nevents"]+=tree.GetEntries()
            processDict[processFolder]["integral"]+=tree.GetEntries()
        rootFile.Close()
        #break
        '''
    print len(processDict[processName]["files"]),
   
    #if xsecs.has_key(processFolder) and genweights.has_key(processFolder):
    if xsecs.has_key(processName):
        print genweights[processFolder]["sum"],genweights[processFolder]["weighted"]
        processDict[processName]["xsec"] = xsecs[processName]
        processDict[processName]["integral"] += genweights[processFolder]["weighted"]
    else: 
        print 'noxsec'
    
for processName in sorted(processDict.keys()):
    if processDict[processName]["integral"]>0:
        processDict[processName]["weight"] = str(processDict[processName]["xsec"]/processDict[processName]["integral"])
    print processName,len(processDict[processName]["files"]),processDict[processName]["weight"]
         
    
class Chain(object):
    def __init__(self,fileList,treeName="Friends"):
        self._fileList = fileList
        self._treeName = treeName
        self._nEvents = []
        
        self._currentFile = None
        self._currentTree = None
        self._currentEntry = 0
        self._currentOffset = 0
        self._buffer = {}
        
        self._fileEventPairs = []
        for i,f in enumerate(self._fileList):
            
            #print i,'/',len(self._fileList),'...',f
            rootFile = uproot.open(f)#,localsource=uproot.FileSource.defaults)
            tree = rootFile[self._treeName]
            nevents = len(tree)
            self._fileEventPairs.append([f,nevents])
            
                
        self._sumEvents = sum(map(lambda x:x[1],self._fileEventPairs))
            
    def GetEntries(self):
        return self._sumEvents
            
    def GetEntry(self,i):
        if i<0:
            print "Error - event entry negative: ",i
            i=0
        if self._currentTree!=None and (i-self._currentOffset)<len(self._currentTree) and (i-self._currentOffset)>=0:
            self._currentEntry = i-self._currentOffset
        else:
            del self._currentTree
            self._currentTree = None
            del self._buffer
            self._buffer = {}
            s = 0
            i = i%self._sumEvents #loop
            for e in range(len(self._fileEventPairs)):
                if s<=i and (s+self._fileEventPairs[e][1])>i:
                    #print "opening",self._fileEventPairs[e][0]
                    self._currentFile = uproot.open(self._fileEventPairs[e][0])#,localsource=uproot.FileSource.defaults)
                    self._currentTree = self._currentFile[self._treeName]
                    self._currentOffset = s
                    self._currentEntry = i-self._currentOffset
                    break
                s+=self._fileEventPairs[e][1]
                    
    def __getattr__(self,k):
        #print sorted(self._currentTree.keys())
        #if not self._currentTree.has_key(k):
        #    print "Error - cannot find element '"+k+"' in tree: ",sorted(self._currentTree.keys())
        if k not in self._buffer:
            self._buffer[k] = self._currentTree[k].array()
            #print "loading branch ",k," with entries ",len(self._buffer[k])," and shape ",self._buffer[k][self._currentEntry].shape,", (tree len=",len(self._currentTree),")"
        if self._currentEntry>=len(self._buffer[k]):
            print "Error - buffer for branch '",k,"' only ",len(self._buffer[k])," but requested entry ",self._currentEntry," (tree len=",len(self._currentTree),")"
            return 0
        return self._buffer[k][self._currentEntry]



selectedEvents = {"tagger1":[],"tagger2":[],"weights":[],"ht":[],"truth":[]}
'''
for backgroundSample in [
    "ZJetsToNuNu_HT-100To200_13TeV-madgraph",
    "ZJetsToNuNu_HT-200To400_13TeV-madgraph",
    "ZJetsToNuNu_HT-400To600_13TeV-madgraph",
    "ZJetsToNuNu_HT-600To800_13TeV-madgraph",
    "ZJetsToNuNu_HT-800to1200_13TeV-madgraph",
    "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
    "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
    "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    "WToLNu_0J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_1J_13TeV-amcatnloFXFX-pythia8",
    "WToLNu_2J_13TeV-amcatnloFXFX-pythia8",
]:
    chain = Chain(processDict[backgroundSample]["files"])
    weight = processDict[backgroundSample]["weight"]
    print "processing ... ",backgroundSample
    for entry in range(0,chain.GetEntries(),1):
        chain.GetEntry(entry)
        if chain.nselectedJets_nominal<3:
            continue
        if chain.nominal_mht<300:
            continue
        if chain.nominal_mht/chain.nominal_met>1.25:
            continue
        if chain.nominal_minPhi<0.2:
            continue
        selectedEvents["tagger1"].append(numpy.array([
            chain.llpdnnx_da_nominal_0p001_LLP_min0,
            chain.llpdnnx_da_nominal_0p01_LLP_min0,
            chain.llpdnnx_da_nominal_0p1_LLP_min0,
            chain.llpdnnx_da_nominal_0_LLP_min0,
            chain.llpdnnx_da_nominal_10_LLP_min0,
            chain.llpdnnx_da_nominal_100_LLP_min0,
            chain.llpdnnx_da_nominal_1000_LLP_min0,
            chain.llpdnnx_da_nominal_10000_LLP_min0,
        ]))
        selectedEvents["tagger2"].append(numpy.array([
            chain.llpdnnx_da_nominal_0p001_LLP_min1,
            chain.llpdnnx_da_nominal_0p01_LLP_min1,
            chain.llpdnnx_da_nominal_0p1_LLP_min1,
            chain.llpdnnx_da_nominal_0_LLP_min1,
            chain.llpdnnx_da_nominal_10_LLP_min1,
            chain.llpdnnx_da_nominal_100_LLP_min1,
            chain.llpdnnx_da_nominal_1000_LLP_min1,
            chain.llpdnnx_da_nominal_10000_LLP_min1,
        ]))
        selectedEvents["ht"].append(
            chain.nominal_ht
        )
        selectedEvents["weights"].append(
            chain.genweight*weight
        )
        selectedEvents["truth"].append(0)
'''

efficiencies = {}

samples = {
    "0p001":[
        "SMS-T1qqqq_ctau-0p001_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-0p001_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "0p01":[
        "SMS-T1qqqq_ctau-0p01_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-0p01_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "0p1":[
        "SMS-T1qqqq_ctau-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "0":[
        "SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "10":[
        "SMS-T1qqqq_ctau-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "100":[
        "SMS-T1qqqq_ctau-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "1000":[
        "SMS-T1qqqq_ctau-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ],
    "10000":[
        "SMS-T1qqqq_ctau-10000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "SMS-T1qqqq_ctau-10000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extra",
    ]
}

efficiencies = {}

for ctau in samples.keys():
    efficiencies[ctau] = {}
    for sampleName in samples[ctau]:
        chain = Chain(processDict[sampleName]["files"])
        print "processing ... ",sampleName
        for entry in range(0,chain.GetEntries(),1):
            chain.GetEntry(entry)
            if chain.nselectedJets_nominal<3:
                continue
            if chain.nominal_mht<300:
                continue
            if chain.nominal_mht/chain.nominal_met>1.25:
                continue
            if chain.nominal_minPhi<0.2:
                continue
            if not efficiencies[ctau].has_key("%s"%chain.llp):
                efficiencies[ctau]["%s"%chain.llp] = {}
            if not efficiencies[ctau]["%s"%chain.llp].has_key("%s"%chain.lsp):
                efficiencies[ctau]["%s"%chain.llp]["%s"%chain.lsp] = {"total":0,"tagged":0}
            efficiencies[ctau]["%s"%chain.llp]["%s"%chain.lsp]["total"]+=getattr(
                chain,
                "llpdnnx_da_nominal_%s_nLLPTrue"%ctau
            )
            efficiencies[ctau]["%s"%chain.llp]["%s"%chain.lsp]["tagged"]+=getattr(
                chain,
                "llpdnnx_da_nominal_%s_nLLPTrueTaggedLLP"%ctau
            )
        
for ctau in efficiencies.keys():
    for llp in efficiencies[ctau].keys():
        for lsp in efficiencies[ctau][llp].keys():
            print "%6s: llp=%s, lsp=%s, eff=%.3f%%"%(
                ctau,llp,lsp,100.*efficiencies[ctau][llp][lsp]["tagged"]/(10**-2+efficiencies[ctau][llp][lsp]["total"])
            )
        
with open('llpEfficiency.json', 'w') as outfile:
    json.dump(efficiencies, outfile,ensure_ascii=True,indent=2,sort_keys=True)    



