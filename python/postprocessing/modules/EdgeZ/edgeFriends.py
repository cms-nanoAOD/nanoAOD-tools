import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi

import copy
import math 


#Loading BTagplugins
ROOT.gSystem.Load("pluginRecoBTagPerformanceDBplugins.so")
def computeMT2(visaVec, visbVec, metVec):
    
    import array
    import numpy

    from ROOT.heppy import Davismt2
    davismt2 = Davismt2()    

    metVector = array.array('d',[0.,metVec.Px(), metVec.Py()])
    visaVector = array.array('d',[0.,visaVec.Px(), visaVec.Py()])
    visbVector = array.array('d',[0.,visbVec.Px(), visbVec.Py()])

    davismt2.set_momenta(visaVector,visbVector,metVector);
    davismt2.set_mn(0);

    return davismt2.get_mt2()





class edgeFriends:
    def __init__(self, label, tightLeptonSel, cleanJet):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.tightLeptonSel = tightLeptonSel
        self.cleanJet = cleanJet
        
        ###################################### This variable is not defined
        self.isMC = 1 # should be: isMC
        
        ###################################### Pile-up stuff should be included here
        #self.setPU("Run2017") 

        ###################################### B-tagging stuff to be included here
        vector = ROOT.vector('string')()
        vector.push_back("up")
        vector.push_back("down") 
        self.calib = ROOT.BTagCalibration("csvv2",os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/edge/btaggingweights/CSVv2_94XSF_V1_B_F.csv")
        self.reader_heavy = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_heavy.load(self.calib, 0, "comb") #0 means b-jets
        self.reader_c = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_c.load(self.calib, 1, "comb") #0 means b-jets
        self.reader_light = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_light.load(self.calib, 2, "incl") #0 means b-jets
        self.calibFASTSIM = ROOT.BTagCalibration("csvv2", os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/edge/btaggingweights/fastsim_csvv2_ttbar_26_1_2017.csv")
        self.reader_heavy_FASTSIM = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_heavy_FASTSIM.load(self.calibFASTSIM, 0, "fastsim") #0 means b-jets
        self.reader_c_FASTSIM = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_c_FASTSIM.load(self.calibFASTSIM, 1, "fastsim") #0 means b-jets
        self.reader_light_FASTSIM = ROOT.BTagCalibrationReader(1, "central", vector) #1 means medium point
        self.reader_light_FASTSIM.load(self.calibFASTSIM, 2, "fastsim") #0 means b-jets
        self.f_btag_eff      = ROOT.TFile(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/edge/btaggingweights/btageff__ttbar_powheg_pythia8_25ns_Moriond17.root")
        self.h_btag_eff_b    = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_b"   ))
        self.h_btag_eff_c    = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_c"   ))
        self.h_btag_eff_udsg = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_udsg"))
        self.f_btag_eff.Close()
        self.btagMediumCut =  0.4941 #DeepCSV
        self.btagLooseCut  =  0.1522 #DeepCSV

        ###################################### Scale factors for leptons



        ###################################### SUSY masses variable definition
        self.susymasslist = ['GenSusyMScan1'     , 'GenSusyMScan2'      , 'GenSusyMScan3'      , 'GenSusyMScan4'      ,
                             'GenSusyMGluino'    , 'GenSusyMGravitino'  , 'GenSusyMStop'       , 'GenSusyMSbottom'    ,
                             'GenSusyMStop2'     , 'GenSusyMSbottom2'   , 'GenSusyMSquark'     ,
                             'GenSusyMNeutralino', 'GenSusyMNeutralino2', 'GenSusyMNeutralino3', 'GenSusyMNeutralino4',
                             'GenSusyMChargino'  , 'GenSusyMChargino2']
        
        ###################################### List of triggers
        self.triggerlist = [ 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
                             'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
                             'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',
                             'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
                             'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',
                             'HLT_DoubleEle25_CaloIdL_MW',
                             'HLT_DoubleEle27_CaloIdL_MW',
                             'HLT_DoubleEle33_CaloIdL_MW',
                             'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
                             'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',
                             'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8',
                             'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8',
                             'HLT_Mu37_TkMu27',
                             'HLT_PFHT180',
                             'HLT_PFHT250',
                             'HLT_PFHT370',
                             'HLT_PFHT430',
                             'HLT_PFHT510',
                             'HLT_PFHT590',
                             'HLT_PFHT680',
                             'HLT_PFHT780',
                             'HLT_PFHT890',
                             'HLT_PFHT1050',
                             'HLT_PFMET120_PFMHT120_IDTight'
                             'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
                         ]

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        label = self.label
        self.out = wrappedOutputTree
        biglist = [ ("evt"+label, "D"),
                    ("run"+label, "I"),
                    ("lumi"+label, "I"),
                    ("nVert"+label, "I"),
                    ("nTrueInt"+label, "F"),
                    ("Flag_HBHENoiseFilter"+label, "I"),
                    ("Flag_HBHENoiseIsoFilter"+label, "I"),
                    ("Flag_EcalDeadCellTriggerPrimitiveFilter"+label, "I"),
                    ("Flag_goodVertices"+label, "I"),
                    ("Flag_eeBadScFilter"+label, "I"),
                    ("Flag_ecalBadCalibFilter"+label, "I"),
                    ("Flag_globalTightHalo2016Filter"+label, "I"),
                    ("Flag_badChargedHadronFilter"+label, "F"),
                    ("Flag_badMuonFilter"+label, "F"),
                    ("nLepTight"+label, "I"),
                    ("nLepLoose"+label, "I"),
                    ("nJetSel"+label, "I"),
                    ("nJetSel_jecUp"+label, "I"),
                    ("nJetSel_jecDn"+label, "I"),
                    ("nFatJetSel"+label, "I"),
                    ("nFatJetSel_jecUp"+label, "I"),
                    ("nFatJetSel_jecDn"+label, "I"),
                    #("nEdgeIsoTracks"+label, "I"),
                    ("rightMjj"+label, "F"),
                    ("bestMjj"+label, "F"),
                    ("minMjj"+label, "F"),
                    ("maxMjj"+label, "F"),
                    ("hardMjj"+label, "F"),
                    ("dphiMjj"+label, "F"),
                    ("dphiMjj_jecUp"+label, "F"),
                    ("dphiMjj_jecDn"+label, "F"),
                    ("drMjj"+label, "F"),
                    ("hardJJDphi"+label, "F"),
                    ("hardJJDR"+label, "F"),
                    ("j1MetDPhi"+label, "F"),
                    ("j2MetDPhi"+label, "F"),
                    ("nPairLep"+label, "I"),
                    #("iLT"+label,"I",20,"nLepTight"+label), 
                    ("iJ"+label,"I",20,"nJetSel"+label), 
                    ("iFJ"+label,"I",20,"nFatJetSel"+label),
                    #("nLepGood20"+label, "I"),
                    ("nJet35"+label, "I"),
                    ("nJet35_jecUp"+label, "I"),
                    ("nJet35_jecDn"+label, "I"),
                    ("nJet25"+label, "I"),
                    ("nJet25_jecUp"+label, "I"),
                    ("nJet25_jecDn"+label, "I"),
                    ("htJet35j"+label, "F"),
                    ("htJet35j_jecUp"+label, "F"),
                    ("htJet35j_jecDn"+label, "F"),
                    ("htJet25j"+label, "F"),
                    ("htJet25j_jecUp"+label, "F"),
                    ("htJet25j_jecDn"+label, "F"),
                    ("nBJetMedium25"+label, "I"),
                    ("nBJetMedium25_jecUp"+label , "I"),
                    ("nBJetMedium25_jecDn"+label , "I"),
                    ("nBJetLoose35"+label  , "I"),
                    ("nBJetLoose35_jecUp"+label  , "I"),
                    ("nBJetLoose35_jecDn"+label  , "I"),
                    ("nBJetMedium35"+label , "I"),
                    ("nBJetMedium35_jecUp"+label , "I"),
                    ("nBJetMedium35_jecDn"+label , "I"),
                    ("nBJetLoose25"+label  , "I"),
                    ("nBJetLoose25_jecUp"+label , "I"),
                    ("nBJetLoose25_jecDn"+label , "I"),
                    ("iL1T"+label, "I"),
                    ("iL2T"+label, "I"), 
                    ("lepsMll"+label, "F"),
                    ("lepsJZB"+label, "F"), 
                    ("lepsJZB_recoil"+label, "F"),
                    ("lepsPhi"+label, "F"),
                    ("lepsDR"+label, "F"),
                    ("lepsMETRec"+label, "F"),
                    ("lepsZPt"+label, "F"),
                    ("ptBestZ"+label, "F"),
                    ("newMet"+label, "F"),
                    ("WmT"+label, "F"),
                    ("WZ_ll_MT2"+label, "F"),
                    ("Z_ll_MT2"+label, "F"),
                    ("newMetPhi"+label, "F"),
                    ("mllBestZ"+label, "F"),
                    ("mllOtherZ"+label, "F"),
                    ("mt2BestZ"+label, "F"),
                    ("metl1DPhi"+label, "F"),
                    ("metl2DPhi"+label, "F"),
                    ("MET_pt"+label, "F"),
                    ("MET_phi"+label, "F"), 
                    ("MET_pt_jesTotalUp"+label, "F"),
                    ("MET_pt_jesTotalDown"+label, "F"),
                    ("MET_pt_unclustEnUp"+label, "F"),
                    ("MET_pt_unclustEnDown"+label, "F"),
                    ("GenMET_pt"+label, "F"),
                    ("GenMET_phi"+label,"F"),
                    ("lepsDPhi"+label, "F"),
                    ("Lep1_pt"+label, "F"), 
                    ("Lep1_eta"+label, "F"), 
                    ("Lep1_phi"+label, "F"),
                    ("Lep1_miniPFRelIso_all"+label, "F"),
                    ("Lep1_pfRelIso03_all"+label, "F"),
                    ("Lep1_pfRelIso04_all"+label, "F"),
                    ("Lep1_dxy"+label, "F"),
                    ("Lep1_dz"+label, "F"),
                    ("Lep1_sip3d"+label, "F"),
                    ("Lep1_pdgId"+label, "I"), 
                    ("Lep1_tightCharge"+label, "F"), 
                    ("Lep1_mvaFall17V1Iso"+label, "F"),
                    ("Lep1_mvaFall17V1noIso"+label, "F"),
                    ("Lep1_genPartFlav"+label, "I"), 
                    #("Lep1_minTauDR"+label, "F"),              
                    ("Lep2_pt"+label, "F"), 
                    ("Lep2_eta"+label, "F"),
                    ("Lep2_phi"+label, "F"),
                    ("Lep2_miniPFRelIso_all"+label, "F"),
                    ("Lep2_pfRelIso03_all"+label, "F"),
                    ("Lep2_pfRelIso04_all"+label, "F"),
                    ("Lep2_dxy"+label, "F"),
                    ("Lep2_dz"+label, "F"),
                    ("Lep2_sip3d"+label, "F"),
                    ("Lep2_pdgId"+label, "I"),
                    ("Lep2_tightCharge"+label, "F"),
                    ("Lep2_mvaFall17V1Iso"+label, "F"),
                    ("Lep2_mvaFall17V1noIso"+label, "F"),
                    ("Lep2_genPartFlav"+label, "I"), 
                    #("Lep2_minTauDR"+label, "F"),      
                    ("PileupW"+label, "F"), 
                    ("PileupW_Up"+label, "F"),
                    ("PileupW_Dn"+label, "F"), 
                    ("min_mlb1"+label, "F"),
                    ("min_mlb2"+label, "F"),
                    ("min_mlb1Up"+label, "F"),
                    ("min_mlb2Up"+label, "F"),
                    ("min_mlb1Dn"+label, "F"),
                    ("min_mlb2Dn"+label, "F"),
                    ("sum_mlb"+label, "F"), 
                    ("sum_mlbUp"+label, "F"),
                    ("sum_mlbDn"+label, "F"),
                    ("st"+label,"F"), 
                    #("srID"+label, "I"), 
                    ("mT_lep1"+label, "F"),
                    ("mT_lep2"+label, "F"),
                    ("mT_dilep"+label, "F"),
                    ("GENmassZZ"+label, "F"),
                    ("GENptZZ"+label, "F"),
                    ("minMT"+label, "F"),
                    ("mt2"+label, "F"),
                    ("mt2_jecUp"+label, "F"),
                    ("mt2_jecDn"+label, "F"),
                    ("mt2_unclUp"+label, "F"),
                    ("mt2_unclDn"+label, "F"),
                    ("mt2bb"+label, "F"),
                    ("mt2bb_jecUp"+label, "F"),
                    ("mt2bb_jecDn"+label, "F"),
                    ("mt2bb_unclUp"+label, "F"),
                    ("mt2bb_unclDn"+label, "F"),
                    #("weight_trigger"+label, "F"),
                    ("weight_btagsf"+label, "F"),
                    ("weight_btagsf_heavy_UP"+label, "F") ,
                    ("weight_btagsf_heavy_DN"+label, "F") ,
                    ("weight_btagsf_light_UP"+label, "F") ,
                    ("weight_btagsf_light_DN"+label, "F") ,
                    ("d3D" + label, "F"),
                    ("parPt" + label, "F"),
                    ("ortPt" + label, "F"),
                    ("dTheta" + label, "F"),
                    #('passesFilters' +label, 'I'),
                    ('genWeight' +label, 'F'),
                    ('mbb'+label, 'F'),
                    ('mbb_jecUp'+label, 'F'),
                    ('mbb_jecDn'+label, 'F'),
                    ('FS_central_jets'+label, 'F'),
                    ('FS_central_jets_jecUp'+label, 'F'),
                    ('FS_central_jets_jecDn'+label, 'F')                    
                 ]
        ################## Trigger variables  
        for trig in self.triggerlist:
            biglist.append( ( '{tn}{lab}'.format(lab=label, tn=trig),'O') )

        ################## SUSY massess  
        for mass in self.susymasslist:
            biglist.append( ( '{tn}{lab}'.format(lab=label, tn=mass),'I') )
         
        ################## IsoTrack stuff
        biglist.append(("nPFLep5"+label, 'I'))
        biglist.append(("nPFHad10"+label, 'I'))
        
        # for itfloat in "pt eta phi dxy dz pfRelIso03_chg pdgId".split():
        #     biglist.append( ("EdgeIsoTracksSel"+label+"_"+itfloat,"F",20,"nEdgeIsoTracks"+label) )
        
        ################## Selected jets
        for jfloat in "pt eta phi mass btagCSVV2 btagDeepB rawFactor pt_jecUp pt_jecDn".split():
            biglist.append( ("JetSel"+label+"_"+jfloat,"F",20,"nJetSel"+label) ) #if self.isMC:
        biglist.append( ("JetSel"+label+"_mcPt",     "F",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcPartonFlavour","I",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_genJetIdx","I",20,"nJetSel"+label) )
        ################## Selected Fat jets
        for fjfloat in "pt eta phi mass btagCSVV2 msoftdrop tau1 tau2 tau3 pt_jecUp pt_jecDn".split(): # btagDeepB  # esto tiene que volver
            biglist.append( ("FatJetSel"+label+"_"+fjfloat,"F",20,"nFatJetSel"+label) ) #if self.isMC:
        # esto tiene que volver
        #biglist.append( ("FatJetSel"+label+"_mcPt",     "F",20,"nFatJetSel"+label) )
        #biglist.append( ("FatJetSel"+label+"_mcMatchId","I",20,"nFatJetSel"+label) )
        #biglist.append( ("FatJetSel"+label+"_hadronFlavour","I",20,"nFatJetSel"+label) )


        for var in biglist:
            self.out.branch( *var ) 

        self.biglist = biglist
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):



        isData = event.isData
        ##### MC variables
        var_mcPt = 10 # mcPt
        ################## Get collections
        leps  =  [l for l in Collection(event,"LepGood","nLepGood")] # using object wrapper so p4 is uncorrected for electrons
        # removing ecorrections for electrons
        for l in leps: 
            if abs(l.pdgId) == 11: 
                l.pt = l.pt/l.eCorr



        ################### Definition of good leptons (this goes first so skim is done first)
        lepst = []
        for il,lep in enumerate(leps):
            if not _susyEdgeLoose(lep): 
                continue
            if not self.tightLeptonSel(lep): 
                continue
            lepst.append(lep)

        lepst.sort(key = lambda x : x.pt, reverse=True)
        nLepTight = len(lepst)
        
        if nLepTight < 2: return False
        self.out.fillBranch('nLepTight'        + self.label, nLepTight)


        # jet stuff 

        jetsc    = [j for j in Collection(event,"Jet","nJet")]
        fatjetsc = [fj for fj in Collection(event,"FatJet","nFatJet")] 
    
        if not isData: 
            genparts = [g for g in Collection(event,"GenPart","nGenPart")]
            genjets = [j for j in Collection(event, "GenJet", "nGenJet")] # Atencion

        if not isData: 
            jetsc_jecUp = [j for j in Collection(event,"Jet","nJet")]
            jetsc_jecDn = [j for j in Collection(event,"Jet","nJet")]        
            jetsc_jecUp = self.smearJets(jetsc_jecUp,  1.0)
            jetsc_jecDn = self.smearJets(jetsc_jecDn, -1.0)

            fatjetsc_jecUp = [fj for fj in Collection(event,"FatJet","nFatJet")] 
            fatjetsc_jecDn = [fj for fj in Collection(event,"FatJet","nFatJet")] 
            fatjetsc_jecUp = self.smearJets(fatjetsc_jecUp,  1.0)
            fatjetsc_jecDn = self.smearJets(fatjetsc_jecDn, -1.0)

            jetsc_jecUp    = [] 
            jetsc_jecDn    = []
            fatjetsc_jecUp = []
            fatjetsc_jecDn = []

        ################## Treatment of n of true events
        if not isData:
            ntrue = event.Pileup_nTrueInt

        ################## Treatment of MET
        (met, metphi)  = event.METFixEE2017_pt, event.METFixEE2017_phi #METFixEE2017
        metp4 = ROOT.TLorentzVector()
        metp4.SetPtEtaPhiM(met, 0, metphi, 0)
        metp4obj = ROOT.TLorentzVector()
        metp4obj.SetPtEtaPhiM(met, 0, metphi, 0)

        ################## Declare dictionaries
        # ret = {}
        # jetret = {}
        # fatjetret = {} 
        # lepret  = {}
        # trigret = {}
        # edgeisotrackret = {}

        ################## Starting to fill the dictionaries
        ################## Event stuff
        self.out.fillBranch('run'        + self.label, event.run)
        self.out.fillBranch('lumi'       + self.label, event.luminosityBlock)
        self.out.fillBranch('evt'        + self.label, long(event.event))
        self.out.fillBranch('nVert'      + self.label, event.PV_npvs)
        self.out.fillBranch('nTrueInt'   + self.label, -1   )
        self.out.fillBranch('genWeight'  + self.label, ( 1. if not hasattr(event, 'genWeight'         ) else getattr(event, 'genWeight') ))
        self.out.fillBranch("PileupW"    + self.label, 1 if isData else event.puWeight)
        self.out.fillBranch("PileupW_Up" + self.label, 1 if isData else event.puWeightUp)
        self.out.fillBranch("PileupW_Dn" + self.label, 1 if isData else event.puWeightDown)


        MET_pt_jesTotalUp   = 0 if isData else event.METFixEE2017_pt_jesTotalUp    
        MET_pt_jesTotalDown = 0 if isData else event.METFixEE2017_pt_jesTotalDown  
        MET_pt_unclustEnUp  = 0 if isData else event.METFixEE2017_pt_unclustEnUp   
        MET_pt_unclustEnDown= 0 if isData else event.METFixEE2017_pt_unclustEnDown 


        ################## MET stuff
        self.out.fillBranch('MET_pt'                + self.label, met                   )
        self.out.fillBranch('MET_phi'               + self.label, metphi                )
        self.out.fillBranch('MET_pt_jesTotalUp'     + self.label, MET_pt_jesTotalUp     )
        self.out.fillBranch('MET_pt_jesTotalDown'   + self.label, MET_pt_jesTotalDown   )
        self.out.fillBranch('MET_pt_unclustEnUp'    + self.label, MET_pt_unclustEnUp    )
        self.out.fillBranch('MET_pt_unclustEnDown'  + self.label, MET_pt_unclustEnDown  )
        self.out.fillBranch('GenMET_pt'             + self.label, -1                    )
        self.out.fillBranch('GenMET_phi'            + self.label, -1                    )

        ################## SUSY masses stuff
        masses = {}
        for mass in self.susymasslist:
            masses[mass] = (-1 if not hasattr(event, mass) else getattr(event, mass) )
            self.out.fillBranch(mass + self.label, masses[mass])
        self.isSMS =  (masses['GenSusyMScan1'] > 0 or masses['GenSusyMNeutralino2'] > 0)

        ################### Filters stuff
        if not self.isSMS:
            self.out.fillBranch('Flag_HBHENoiseFilter'                     + self.label ,event.Flag_HBHENoiseFilter                    )
            self.out.fillBranch('Flag_HBHENoiseIsoFilter'                  + self.label ,event.Flag_HBHENoiseIsoFilter                 )
            self.out.fillBranch('Flag_EcalDeadCellTriggerPrimitiveFilter'  + self.label ,event.Flag_EcalDeadCellTriggerPrimitiveFilter )
            self.out.fillBranch('Flag_goodVertices'                        + self.label ,event.Flag_goodVertices                       )
            self.out.fillBranch('Flag_eeBadScFilter'                       + self.label ,event.Flag_eeBadScFilter                      )
            self.out.fillBranch('Flag_ecalBadCalibFilter'                  + self.label ,event.Flag_ecalBadCalibFilter                 )
            self.out.fillBranch('Flag_globalTightHalo2016Filter'           + self.label ,event.Flag_globalTightHalo2016Filter          )
            self.out.fillBranch('Flag_badMuonFilter'                       + self.label ,event.Flag_BadPFMuonFilter                    )
            self.out.fillBranch("Flag_badChargedHadronFilter"              + self.label ,event.Flag_BadChargedCandidateFilter          )
            self.out.fillBranch("Flag_badMuonFilter"                       + self.label ,event.Flag_BadPFMuonFilter                    )
        
        ################### Isotracks stuff
        self.out.fillBranch('nPFLep5'  + self.label, event.nPFLep5 )       
        self.out.fillBranch('nPFHad10' + self.label, event.nPFHad10)


        if not isData:
            self.out.fillBranch('nTrueInt'  + self.label, event.Pileup_nTrueInt) 
            self.out.fillBranch('GenMET_pt' + self.label, event.GenMET_pt      )
            self.out.fillBranch('GenMET_phi'+ self.label, event.GenMET_phi     )
            vec = []
            ################### This is needed for ZZ NNLO/NLO k-factor which is provided as a function of gen diboson mass or pt
            for g, gen in enumerate(genparts):
                if (genparts[gen.genPartIdxMother].pdgId !=23): # Atencion, not sure if this is defined well
                    continue
                else:
                    if (abs(gen.pdgId) == 11 or abs(gen.pdgId) == 13 or abs(gen.pdgId) == 15 or abs(gen.pdgId) == 12 or abs(gen.pdgId) == 14 or abs(gen.pdgId) == 16):
                        vec.append(g)
            if len(vec) >3:
                g1 = ROOT.TLorentzVector()
                g2 = ROOT.TLorentzVector()
                g3 = ROOT.TLorentzVector()
                g4 = ROOT.TLorentzVector()
                g1.SetPtEtaPhiM(genparts[vec[0]].p4().Pt(), genparts[vec[0]].p4().Eta(),genparts[vec[0]].p4().Phi(),genparts[vec[0]].p4().M())
                g2.SetPtEtaPhiM(genparts[vec[1]].p4().Pt(), genparts[vec[1]].p4().Eta(),genparts[vec[1]].p4().Phi(),genparts[vec[1]].p4().M())
                g3.SetPtEtaPhiM(genparts[vec[2]].p4().Pt(), genparts[vec[2]].p4().Eta(),genparts[vec[2]].p4().Phi(),genparts[vec[2]].p4().M())
                g4.SetPtEtaPhiM(genparts[vec[3]].p4().Pt(), genparts[vec[3]].p4().Eta(),genparts[vec[3]].p4().Phi(),genparts[vec[3]].p4().M())
                gtotMass = (g1+g2+g3+g4).M()
                gtotPt = (g1+g2+g3+g4).Pt()
                self.out.fillBranch('GENmassZZ'+ self.label, gtotMass)
                self.out.fillBranch('GENptZZ'  + self.label,  gtotPt )       


        ################### Trigger list Atencion: Esto es preciso hacerlo aqui?
        for trig in self.triggerlist:
            self.out.fillBranch(trig+self.label, 0 if not hasattr(event, trig) else getattr(event, trig) )

 
        ################### Calculating two lepton variables for all elements of the collection
        iL1iL2 = self.getPairVariables(lepst, metp4)

        #ret['iL1T'] = ret["iLT"][ iL1iL2[0] ]  if (len(nLepTight) >=1 and iL1iL2[0] != -999) else -999 # this shouldnt happen here because we have a skim, but i keep it just in case we want to remove the skim
        #ret['iL2T'] = ret["iLT"][ iL1iL2[1] ]  if (len(nLepTight) >=2 and iL1iL2[1] != -999) else -999 
        self.out.fillBranch('lepsMll'   + self.label,   iL1iL2[2] )
        self.out.fillBranch('lepsJZB'   + self.label,   iL1iL2[3] )
        self.out.fillBranch('lepsDR'    + self.label,   iL1iL2[4] )
        self.out.fillBranch('lepsPhi'   + self.label,   iL1iL2[5] )
        self.out.fillBranch('lepsMETRec'+ self.label,   iL1iL2[6] )
        self.out.fillBranch('lepsZPt'   + self.label,   iL1iL2[7] ); lepsZPt = iL1iL2[7]
        self.out.fillBranch('lepsDPhi'  + self.label,   iL1iL2[8] )
        self.out.fillBranch('d3D'       + self.label,   iL1iL2[9] )
        self.out.fillBranch('parPt'     + self.label,   iL1iL2[10])
        self.out.fillBranch('ortPt'     + self.label,   iL1iL2[11])
        self.out.fillBranch('dTheta'    + self.label,   iL1iL2[12])


        ################### Now working with the 2 good leptons
        l1 = ROOT.TLorentzVector()
        l2 = ROOT.TLorentzVector()
        ltlvs = [l1, l2]
        lepvectors = []
        # for lfloat in 'pt eta phi miniPFRelIso_all pdgId mvaFall17V1Iso mvaFall17V1noIso dxy dz sip3d pfRelIso03_all pfRelIso04_all tightCharge'.split():
        #     # Atencion, falta mcMatchId en los dos
            
        #     if lfloat == 'pdgId':
        #         lepret["Lep1_"+lfloat+self.label] = -99
        #         lepret["Lep2_"+lfloat+self.label] = -99
        #     else:
        #         lepret["Lep1_"+lfloat+self.label] = -42.
        #         lepret["Lep2_"+lfloat+self.label] = -42.
        if nLepTight > 1: 
            nPairLep = 2
            lcount = 1
            lepret = {} 
            for lep in [lepst[0],lepst[1]]:
                for lfloat in 'pt eta phi miniPFRelIso_all pdgId mvaFall17V1Iso mvaFall17V1noIso dxy dz sip3d pfRelIso03_all pfRelIso04_all tightCharge genPartFlav'.split():
                    if lfloat == 'mcMatchId' and isData:
                        lepret["Lep"+str(lcount)+"_"+lfloat+self.label] = 1
                    else:
                        lepret["Lep"+str(lcount)+"_"+lfloat+self.label] = getattr(lep,lfloat)
                lepvectors.append(lep)
                lepret['metl'+str(lcount)+'DPhi'+self.label] = abs( deltaPhi( getattr(lep, 'phi'), metphi ))
                ltlvs[lcount-1].SetPtEtaPhiM(lep.pt, lep.eta, lep.phi, 0.0005 if lep.pdgId == 11 else 0.106)
                lcount += 1
        else:
            nPairLep = 0
        self.out.fillBranch('nPairLep' + self.label, nPairLep)
        for k,v in lepret.iteritems(): 
            self.out.fillBranch(k,v) #fullret[k] = v



        ################### Variables needed for 4l control regions
        if len(leps) < 4: 
            mllBestZ = -99; mt2BestZ = -99; ptBestZ = -99; mllOtherZ = -99; newMet = -99; newMetPhi = -99;
        else:
            l1Formt2 = ROOT.reco.Particle.LorentzVector(leps[0].p4().Px(), leps[0].p4().Py(),leps[0].p4().Pz(),leps[0].p4().Energy())
            l2Formt2 = ROOT.reco.Particle.LorentzVector(leps[1].p4().Px(), leps[1].p4().Py(),leps[1].p4().Pz(),leps[1].p4().Energy())
            l3Formt2 = ROOT.reco.Particle.LorentzVector(leps[2].p4().Px(), leps[2].p4().Py(),leps[2].p4().Pz(),leps[2].p4().Energy())
            l4Formt2 = ROOT.reco.Particle.LorentzVector(leps[3].p4().Px(), leps[3].p4().Py(),leps[3].p4().Pz(),leps[3].p4().Energy())
            l1 = ROOT.TLorentzVector()
            l2 = ROOT.TLorentzVector()
            l3 = ROOT.TLorentzVector()
            l4 = ROOT.TLorentzVector()
            newMet=  ROOT.TLorentzVector();
            l1.SetPtEtaPhiM(leps[0].p4().Pt(), leps[0].p4().Eta(),leps[0].p4().Phi(),leps[0].p4().M()) 
            l2.SetPtEtaPhiM(leps[1].p4().Pt(), leps[1].p4().Eta(),leps[1].p4().Phi(),leps[1].p4().M()) 
            l3.SetPtEtaPhiM(leps[2].p4().Pt(), leps[2].p4().Eta(),leps[2].p4().Phi(),leps[2].p4().M()) 
            l4.SetPtEtaPhiM(leps[3].p4().Pt(), leps[3].p4().Eta(),leps[3].p4().Phi(),leps[3].p4().M()) 
            lepVecs = [l1, l2, l3, l4]
            lepVecsForMT2 = [l1Formt2, l2Formt2, l3Formt2, l4Formt2]
            bestmll = 1e6
            newMT2 = -99
            for i in lepVecs:
                for j in lepVecs:
                    if j == i: continue
                    if (abs((i+j).M() - 91.1876) < abs(bestmll - 91.1876)):
                        bestmll = (i+j).M()
                        best = i+j
                        ptobj = ROOT.TLorentzVector()
                        ptobj.SetPtEtaPhiM(best.Pt(), best.Eta(), best.Phi(), best.M())
                        newMetObj = metp4obj+ptobj
                        for k in lepVecs:
                            if k == i: continue
                            if k == j: continue
                            for m in lepVecs:
                                if m == i: continue
                                if m == j: continue
                                if m == k: continue
                                otherZmll = (k+m).M()
                                newMT2 = computeMT2(lepVecsForMT2[lepVecs.index(k)], lepVecsForMT2[lepVecs.index(m)], newMetObj)
            newMet     = newMetObj.Pt()
            newMetPhi  = newMetObj.Phi()
            mt2BestZ   = newMT2
            mllBestZ   = bestmll                                                         
            mllOtherZ  = otherZmll                                                         
            ptBestZ    = best.Pt()                                                                                                                                                 
       
        self.out.fillBranch('newMet'   +self.label,newMet   )        
        self.out.fillBranch('newMetPhi'+self.label,newMetPhi)
        self.out.fillBranch('mt2BestZ' +self.label,mt2BestZ )
        self.out.fillBranch('mllBestZ' +self.label,mllBestZ )
        self.out.fillBranch('mllOtherZ'+self.label,mllOtherZ)
        self.out.fillBranch('ptBestZ'  +self.label,ptBestZ  )

        ################### Variables needed for 3l control region
        if (len(leps) < 3): 
            WmT = -99; WZ_ll_MT2 = -99; Z_ll_MT2 = -99;
        else:
            l1Formt2 = ROOT.reco.Particle.LorentzVector(leps[0].p4().Px(), leps[0].p4().Py(),leps[0].p4().Pz(),leps[0].p4().Energy())
            l2Formt2 = ROOT.reco.Particle.LorentzVector(leps[1].p4().Px(), leps[1].p4().Py(),leps[1].p4().Pz(),leps[1].p4().Energy())
            l3Formt2 = ROOT.reco.Particle.LorentzVector(leps[2].p4().Px(), leps[2].p4().Py(),leps[2].p4().Pz(),leps[2].p4().Energy())
            l1 = ROOT.TLorentzVector(); l2 = ROOT.TLorentzVector(); l3 = ROOT.TLorentzVector(); 
            l1.SetPtEtaPhiM(leps[0].p4().Pt(), leps[0].p4().Eta(),leps[0].p4().Phi(),leps[0].p4().M()) 
            l2.SetPtEtaPhiM(leps[1].p4().Pt(), leps[1].p4().Eta(),leps[1].p4().Phi(),leps[1].p4().M()) 
            l3.SetPtEtaPhiM(leps[2].p4().Pt(), leps[2].p4().Eta(),leps[2].p4().Phi(),leps[2].p4().M()) 
            lepVecs = [l1, l2, l3]
            lepVecsForMT2 = [l1Formt2, l2Formt2, l3Formt2]
            bestmll = 1e6
            #In 3 lepton cases, this function computes the MT with the lepton coming from the Z and the MT2 with a lepton from a Z and a lepton from a W
            for i in lepVecs:
                for j in lepVecs:
                    if j == i: continue
                    if (abs((i+j).M() - 91.1876) < abs(bestmll - 91.1876)):
                        bestmll = (i+j).M()
                        best = i+j
                        for k in lepVecs:
                            if k == i: continue
                            if k == j: continue
                            WmT = self.getMT(k.Pt(), metp4obj.Pt(), k.Phi(),  metp4obj.Phi()) 
                            Z_ll_MT2 = computeMT2(lepVecsForMT2[lepVecs.index(i)], lepVecsForMT2[lepVecs.index(j)], metp4)
                            if i.Pt() > j.Pt():
                                WZ_ll_MT2 = computeMT2(lepVecsForMT2[lepVecs.index(i)], lepVecsForMT2[lepVecs.index(k)], metp4)
                            else:
                                WZ_ll_MT2 = computeMT2(lepVecsForMT2[lepVecs.index(j)], lepVecsForMT2[lepVecs.index(k)], metp4)

        self.out.fillBranch('WmT'        + self.label, WmT       ) 
        self.out.fillBranch('WZ_ll_MT2'  + self.label, WZ_ll_MT2 )
        self.out.fillBranch('Z_ll_MT2'   + self.label, Z_ll_MT2  )



        ################### Jet variables
        jetsc       = self.setJetCollection(jetsc, lepst)
        jetsc_jecUp = self.setJetCollection(jetsc_jecUp, lepst)
        jetsc_jecDn = self.setJetCollection(jetsc_jecDn, lepst)
        fatjetsc    = self.setFatJetCollection(fatjetsc, jetsc, lepst)
        fatjetsc_jecUp    = self.setFatJetCollection(fatjetsc_jecUp, jetsc, lepst)
        fatjetsc_jecDn    = self.setFatJetCollection(fatjetsc_jecDn, jetsc, lepst)

        (ijlist      ,nb25      ,nbl25      ,nb35      ,nl35      ,n35      ,n25      ,ht35      ,ht25      ,theJets      ,theBJets      ,mbb      ,the25BJets) = self.countJets(jetsc)
        (ijlist_jecup,nb25_jecUp,nbl25_jecUp,nb35_jecUp,nl35_jecUp,n35_jecUp,n25_jecUp,ht35_jecUp,ht25_jecUp,theJets_jecUp,theBJets_jecUp,mbb_jecUp,the25BJets_jecUp) = self.countJets(jetsc_jecUp)
        (ijlist_jecdn,nb25_jecDn,nbl25_jecDn,nb35_jecDn,nl35_jecDn,n35_jecDn,n25_jecDn,ht35_jecDn,ht25_jecDn,theJets_jecDn,theBJets_jecDn,mbb_jecDn,the25BJets_jecDn) = self.countJets(jetsc_jecDn)
        (ifjlist) = self.countFatJets(fatjetsc)
        (ifjlist_jecUp) = self.countFatJets(fatjetsc_jecUp)
        (ifjlist_jecDn) = self.countFatJets(fatjetsc_jecDn)

        self.out.fillBranch('FS_central_jets' + self.label, self.checkJetsGenJets(jetsc))
        self.out.fillBranch('nJet35'          + self.label, n35                         )
        self.out.fillBranch('nJet25'          + self.label, n25                         )
        self.out.fillBranch('nBJetMedium25'   + self.label, nb25                        )
        self.out.fillBranch('nBJetMedium35'   + self.label, nb35                        )
        self.out.fillBranch('nBJetLoose35'    + self.label, nl35                        )
        self.out.fillBranch('nBJetLoose25'    + self.label, nbl25                       )
        self.out.fillBranch("htJet35j"        + self.label, ht35                        )
        self.out.fillBranch("htJet25j"        + self.label, ht25                        )
        self.out.fillBranch('nJet35_jecUp'              + self.label, n35_jecUp  ); self.out.fillBranch('nJet35_jecDn'       + self.label , n35_jecDn  )
        self.out.fillBranch('nJet25_jecUp'              + self.label, n25_jecUp  ); self.out.fillBranch('nJet25_jecDn'       + self.label , n25_jecDn  )
        self.out.fillBranch('nBJetMedium25_jecUp'       + self.label, nb25_jecUp ); self.out.fillBranch('nBJetMedium25_jecDn'+ self.label , nb25_jecDn )
        self.out.fillBranch('nBJetMedium35_jecUp'       + self.label, nb35_jecUp ); self.out.fillBranch('nBJetMedium35_jecDn'+ self.label , nb35_jecDn )
        self.out.fillBranch('nBJetLoose35_jecUp'        + self.label, nl35_jecUp ); self.out.fillBranch('nBJetLoose35_jecDn' + self.label , nl35_jecDn )
        self.out.fillBranch('nBJetLoose25_jecUp'        + self.label, nbl25_jecUp); self.out.fillBranch('nBJetLoose25_jecDn' + self.label , nbl25_jecDn)
        self.out.fillBranch("htJet35j_jecUp"            + self.label, ht35_jecUp ); self.out.fillBranch("htJet35j_jecDn"     + self.label , ht35_jecDn )
        self.out.fillBranch("htJet25j_jecUp"            + self.label, ht25_jecUp ); self.out.fillBranch("htJet25j_jecDn"     + self.label , ht25_jecDn ) 
        self.out.fillBranch('FS_central_jets_jecUp'     + self.label, self.checkJetsGenJets(jetsc_jecUp))
        self.out.fillBranch('FS_central_jets_jecDn'     + self.label, self.checkJetsGenJets(jetsc_jecDn))

        self.out.fillBranch('nJetSel'         + self.label, len(ijlist)       )
        self.out.fillBranch('nJetSel_jecUp'   + self.label, len(ijlist_jecup) )
        self.out.fillBranch('nJetSel_jecDn'   + self.label, len(ijlist_jecdn) )
        self.out.fillBranch('nFatJetSel'      + self.label, len(ifjlist)      )
        self.out.fillBranch('nFatJetSel_jecUp'+ self.label, len(ifjlist_jecUp))
        self.out.fillBranch('nFatJetSel_jecDn'+ self.label, len(ifjlist_jecDn))  
        self.out.fillBranch('mbb'             + self.label, mbb      )
        self.out.fillBranch('mbb_jecUp'       + self.label, mbb_jecUp)
        self.out.fillBranch('mbb_jecDn'       + self.label, mbb_jecDn)

        
        ################### MT and MT2 variables
        mT_lep1 = -1.
        mT_lep2 = -1.
        mT_dilep = -1.
        minMT = -1.
        mt2 = -1.
        mt2_jecUp = -1.
        mt2_jecDn = -1.
        mt2bb = -1.
        mt2bb_jecUp = -1.
        mt2bb_jecDn = -1.
        if nPairLep == 2:
            l1mt2 = ROOT.reco.Particle.LorentzVector(lepvectors[0].p4().Px(), lepvectors[0].p4().Py(),lepvectors[0].p4().Pz(),lepvectors[0].p4().Energy())
            l2mt2 = ROOT.reco.Particle.LorentzVector(lepvectors[1].p4().Px(), lepvectors[1].p4().Py(),lepvectors[1].p4().Pz(),lepvectors[1].p4().Energy())
            metp4 = ROOT.reco.Particle.LorentzVector(met*math.cos(metphi),met*math.sin(metphi),0,met)
            if not isData:
                metp4obj_jecUp  = ROOT.reco.Particle.LorentzVector(MET_pt_jesTotalUp*math.cos(metphi),MET_pt_jesTotalUp*math.sin(metphi),0,MET_pt_jesTotalUp)
                metp4obj_jecDn  = ROOT.reco.Particle.LorentzVector(MET_pt_jesTotalDown*math.cos(metphi),MET_pt_jesTotalDown*math.sin(metphi),0,MET_pt_jesTotalDown)
                metp4obj_unclUp = ROOT.reco.Particle.LorentzVector(MET_pt_unclustEnUp*math.cos(metphi),MET_pt_unclustEnUp*math.sin(metphi),0,MET_pt_unclustEnUp)
                metp4obj_unclDn = ROOT.reco.Particle.LorentzVector(MET_pt_unclustEnDown*math.cos(metphi),MET_pt_unclustEnDown*math.sin(metphi),0,MET_pt_unclustEnDown)
                mt2_jecUp = computeMT2(l1mt2, l2mt2, metp4obj_jecUp)
                mt2_jecDn = computeMT2(l1mt2, l2mt2, metp4obj_jecDn)
                mt2_unclUp = computeMT2(l1mt2, l2mt2, metp4obj_unclUp)
                mt2_unclDn = computeMT2(l1mt2, l2mt2, metp4obj_unclDn)    
            else:
                metp4obj_jecUp = 0                 
                metp4obj_jecDn = 0 
                metp4obj_unclUp = 0
                metp4obj_unclDn = 0
                mt2_jecUp  = - 99
                mt2_jecDn  = - 99
                mt2_unclUp = - 99
                mt2_unclDn = - 99

            mt2       = computeMT2(l1mt2, l2mt2, metp4obj)
            mT_lep1 = self.getMT(l1mt2.Pt(), metp4obj.Pt(), l1mt2.Phi(),  metp4obj.Phi())
            mT_lep2 = self.getMT(l2mt2.Pt(), metp4obj.Pt(), l2mt2.Phi(),  metp4obj.Phi())
            mT_dilep = self.getMT((l1mt2 + l2mt2).Pt(), metp4obj.Pt(), (l1mt2 + l2mt2).Phi(),  metp4obj.Phi())
            minMT = self.getMinMT(l1mt2.Pt(),l2mt2.Pt(), metp4obj.Pt(), l1mt2.Phi(),l2mt2.Phi(),  metp4obj.Phi())

            
            if nb25 != 2: 
                mt2bb = -99
                mt2bb_unclUp = -99
                mt2bb_unclDn = -99
            else: 
                b1 = ROOT.TLorentzVector(); b2 = ROOT.TLorentzVector()
                b1.SetPtEtaPhiM(the25BJets[0].pt, the25BJets[0].eta, the25BJets[0].phi, the25BJets[0].mass)
                b2.SetPtEtaPhiM(the25BJets[1].pt, the25BJets[1].eta, the25BJets[1].phi, the25BJets[1].mass)
                b10 = b1+lepvectors[0].p4(); b11 = b1+lepvectors[1].p4()
                b20 = b2+lepvectors[0].p4(); b21 = b2+lepvectors[1].p4()
                b10obj = ROOT.reco.Particle.LorentzVector(b10.Px(), b10.Py(), b10.Pz(), b10.E())
                b20obj = ROOT.reco.Particle.LorentzVector(b20.Px(), b20.Py(), b20.Pz(), b20.E())
                b11obj = ROOT.reco.Particle.LorentzVector(b11.Px(), b11.Py(), b11.Pz(), b11.E())
                b21obj = ROOT.reco.Particle.LorentzVector(b21.Px(), b21.Py(), b21.Pz(), b21.E())
                mt2bb_A = computeMT2(b10obj, b21obj, metp4obj)
                mt2bb_B = computeMT2(b11obj, b20obj, metp4obj)
                mt2bb          = min(mt2bb_A, mt2bb_B)
                if not isData:
                    mt2bb_unclUp_A = computeMT2(b10obj, b21obj, metp4obj_unclUp)
                    mt2bb_unclUp_B = computeMT2(b11obj, b20obj, metp4obj_unclUp)
                    mt2bb_unclDn_A = computeMT2(b10obj, b21obj, metp4obj_unclDn)
                    mt2bb_unclDn_B = computeMT2(b11obj, b20obj, metp4obj_unclDn)
                    mt2bb_unclUp   = min(mt2bb_unclUp_A, mt2bb_unclUp_B)
                    mt2bb_unclDn   = min(mt2bb_unclDn_A, mt2bb_unclDn_B)
                else:
                    mt2bb_unclUp   = -99
                    mt2bb_unclDn   = -99
                    
                del b10obj, b11obj, b20obj, b21obj
                
            if nb25_jecUp != 2: 
                mt2bb_jecUp = -99
            else: 
                b1 = ROOT.TLorentzVector(); b2 = ROOT.TLorentzVector()
                b1.SetPtEtaPhiM(the25BJets_jecUp[0].pt, the25BJets_jecUp[0].eta, the25BJets_jecUp[0].phi, the25BJets_jecUp[0].mass)
                b2.SetPtEtaPhiM(the25BJets_jecUp[1].pt, the25BJets_jecUp[1].eta, the25BJets_jecUp[1].phi, the25BJets_jecUp[1].mass)
                b10 = b1+lepvectors[0].p4(); b11 = b1+lepvectors[1].p4()
                b20 = b2+lepvectors[0].p4(); b21 = b2+lepvectors[1].p4()
                b10obj_jecUp = ROOT.reco.Particle.LorentzVector(b10.Px(), b10.Py(), b10.Pz(), b10.E())
                b20obj_jecUp = ROOT.reco.Particle.LorentzVector(b20.Px(), b20.Py(), b20.Pz(), b20.E())
                b11obj_jecUp = ROOT.reco.Particle.LorentzVector(b11.Px(), b11.Py(), b11.Pz(), b11.E())
                b21obj_jecUp = ROOT.reco.Particle.LorentzVector(b21.Px(), b21.Py(), b21.Pz(), b21.E())
                mt2bb_A = computeMT2(b10obj_jecUp, b21obj_jecUp, metp4obj_jecUp)
                mt2bb_B = computeMT2(b11obj_jecUp, b20obj_jecUp, metp4obj_jecUp)
                mt2bb_jecUp   = min(mt2bb_A, mt2bb_B)
                del b10obj_jecUp, b11obj_jecUp, b20obj_jecUp, b21obj_jecUp

            if nb25_jecDn != 2: 
                mt2bb_jecDn = -99
            else: 
                b1 = ROOT.TLorentzVector(); b2 = ROOT.TLorentzVector()
                b1.SetPtEtaPhiM(the25BJets_jecDn[0].pt, the25BJets_jecDn[0].eta, the25BJets_jecDn[0].phi, the25BJets_jecDn[0].mass)
                b2.SetPtEtaPhiM(the25BJets_jecDn[1].pt, the25BJets_jecDn[1].eta, the25BJets_jecDn[1].phi, the25BJets_jecDn[1].mass)
                b10 = b1+lepvectors[0].p4(); b11 = b1+lepvectors[1].p4()
                b20 = b2+lepvectors[0].p4(); b21 = b2+lepvectors[1].p4()
                b10obj_jecDn = ROOT.reco.Particle.LorentzVector(b10.Px(), b10.Py(), b10.Pz(), b10.E())
                b20obj_jecDn = ROOT.reco.Particle.LorentzVector(b20.Px(), b20.Py(), b20.Pz(), b20.E())
                b11obj_jecDn = ROOT.reco.Particle.LorentzVector(b11.Px(), b11.Py(), b11.Pz(), b11.E())
                b21obj_jecDn = ROOT.reco.Particle.LorentzVector(b21.Px(), b21.Py(), b21.Pz(), b21.E())
                mt2bb_A = computeMT2(b10obj_jecDn, b21obj_jecDn, metp4obj_jecDn)
                mt2bb_B = computeMT2(b11obj_jecDn, b20obj_jecDn, metp4obj_jecDn)
                mt2bb_jecDn   = min(mt2bb_A, mt2bb_B)
                del b10obj_jecDn, b11obj_jecDn, b20obj_jecDn, b21obj_jecDn                

            del metp4obj, metp4obj_jecUp, metp4obj_jecDn, metp4obj_unclUp, metp4obj_unclDn


        self.out.fillBranch('mT_lep1'      + self.label , mT_lep1      )
        self.out.fillBranch('mT_lep2'      + self.label , mT_lep2      )
        self.out.fillBranch('mT_dilep'     + self.label , mT_dilep     )
        self.out.fillBranch('minMT'        + self.label , minMT        )
        self.out.fillBranch('mt2'          + self.label , mt2          )
        self.out.fillBranch('mt2_jecUp'    + self.label , mt2_jecUp    )
        self.out.fillBranch('mt2_jecDn'    + self.label , mt2_jecDn    )
        self.out.fillBranch('mt2_unclUp'   + self.label , mt2_unclUp   )
        self.out.fillBranch('mt2_unclDn'   + self.label , mt2_unclDn   )
        self.out.fillBranch('mt2bb'        + self.label , mt2bb        )   
        self.out.fillBranch('mt2bb_jecUp'  + self.label , mt2bb_jecUp  )
        self.out.fillBranch('mt2bb_jecDn'  + self.label , mt2bb_jecDn  )
        self.out.fillBranch('mt2bb_unclUp' + self.label , mt2bb_unclUp )
        self.out.fillBranch('mt2bb_unclDn' + self.label , mt2bb_unclDn )
        
        ################### Sort jets by pt
        ijlist.sort(key = lambda idx : jetsc[idx].pt, reverse = True)
        ijlist_jecup.sort(key = lambda idx : jetsc_jecUp[idx].pt, reverse = True)
        ijlist_jecdn.sort(key = lambda idx : jetsc_jecDn[idx].pt, reverse = True)
        ifjlist.sort(key = lambda idx : fatjetsc[idx].pt, reverse = True)
        ifjlist_jecUp.sort(key = lambda idx : fatjetsc_jecUp[idx].pt, reverse = True)
        ifjlist_jecDn.sort(key = lambda idx : fatjetsc_jecDn[idx].pt, reverse = True)


        ################### Compute jet and fatjet variables Atencion
        jetret = {} 
        for jfloat in "pt eta phi mass btagCSVV2 btagDeepB rawFactor pt_jecUp pt_jecDn".split():
            jetret[jfloat] = []
        if not isData:
            for jmc in "mcPt mcPartonFlavour genJetIdx".split():
                #mcPt mcFlavour mcMatchId hadronFlavour
                jetret[jmc] = []

        for idx in ijlist:
            jet = jetsc[idx] 
            for jfloat in "pt eta phi mass btagCSVV2 btagDeepB rawFactor".split():
                jetret[jfloat].append( getattr(jet,jfloat) )

            jetret['pt_jecUp'].append( jetsc_jecUp[idx] if idx < len(jetsc_jecUp) else -99)
            jetret['pt_jecDn'].append( jetsc_jecDn[idx] if idx < len(jetsc_jecUp) else -99)

            if not isData: # Atencion
                jetret["genJetIdx"].append( getattr(jet, "genJetIdx") if not isData else -1.)
                if getattr(jet, "genJetIdx") == -1 or len(genjets)<=jet.genJetIdx:
                    jetret["mcPartonFlavour"].append(-1)
                    jetret["mcPt"].append(-1)
                else:
                    gjet = genjets[getattr(jet, "genJetIdx")] 
                    jetret["mcPartonFlavour"].append( getattr(gjet, "partonFlavour") if not isData else -1)
                    jetret["mcPt"].append( getattr(gjet, "pt") if not isData else -1.)

                #for jmc in "mcPt mcFlavour hadronFlavour".split(): # Atencion: Esto es lo que habia antes
                    #mcPt mcFlavour mcMatchId
                    #jetret[jmc].append( getattr(jet,jmc) if not isData else -1.)

        for k,v in jetret.iteritems(): 
            self.out.fillBranch("JetSel%s_%s" % (self.label,k),v) # fullret["JetSel%s_%s" % (self.label,k)] = v


        ## Variables of fatjets
        fatjetret = {} 
        for fjfloat in "pt eta phi mass btagCSVV2 tau1 tau2 tau3 msoftdrop pt_jecUp pt_jecDn".split(): # 
            fatjetret[fjfloat] = []
#        if not isData:
#            for fjmc in "mcPt mcMatchId hadronFlavour".split():  # mcFlavour 
#                fatjetret[fjmc] = []
        
            
        for idx in ifjlist:
            fatjet = fatjetsc[idx]
            for fjfloat in "pt eta phi mass tau1 btagCSVV2 tau2 tau3 msoftdrop".split():#     ".split(): 
                fatjetret[fjfloat].append( getattr(fatjet,fjfloat) )
            fatjetret['pt_jecUp'].append( fatjetsc_jecUp[idx] if idx < len(fatjetsc_jecUp) else -99) 
            fatjetret['pt_jecDn'].append( fatjetsc_jecDn[idx] if idx < len(fatjetsc_jecDn) else -99) 

        #     if not isData:  
        #         for fjmc in "mcPt mcMatchId hadronFlavour".split():  #  mcFlavour
        #             fatjetret[fjmc].append( -1 ) # getattr(fatjet,fjmc) if not isData or not hasattr(fatjet,jfmc) else -1.)
        for k,v in fatjetret.iteritems(): 
            self.out.fillBranch("FatJetSel%s_%s" % (self.label,k),v) #fullret["FatJetSel%s_%s" % (self.label,k)] = v


        ################### Compute isotrack variables
        #ret["nEdgeIsoTracks"] = event.nEdgeIsoTracks
        # for itfloat in "pt eta phi dz dxy pfRelIso03_chg pdgId".split():
        #     edgeisotrackret[itfloat] = []
        # for  it, track in enumerate(edgeisotracks):
        #     for itfloat in "pt eta phi dz dxy pfRelIso03_chg pdgId".split():
        #         edgeisotrackret[itfloat].append( getattr(track, itfloat) )
        

        ################### Compute the recoil of the jets
        totalRecoil = ROOT.TLorentzVector()
        for j in theJets:
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)
            totalRecoil = totalRecoil + jet
            
        ################### Compute the invariant mass of the jets under several conditions
        theJets  = sorted(theJets , key = lambda j : j.pt, reverse = True)
        theBJets = sorted(theBJets, key = lambda j : j.pt, reverse = True)
        theJets_jecUp = sorted(theJets_jecUp , key = lambda j : j.pt, reverse = True)
        theJets_jecDn = sorted(theJets_jecDn , key = lambda j : j.pt, reverse = True)

        self.out.fillBranch('lepsJZB_recoil' + self.label, totalRecoil.Pt() - lepsZPt)
        self.out.fillBranch('rightMjj'       + self.label, self.getRightMjj(theJets)        )
        self.out.fillBranch('bestMjj'        + self.label, self.getBestMjj(theJets)         )
        self.out.fillBranch('dphiMjj'        + self.label, self.getDPhiMjj(theJets)         )
        self.out.fillBranch('dphiMjj_jecUp'  + self.label, self.getDPhiMjj(theJets_jecUp)   )
        self.out.fillBranch('dphiMjj_jecDn'  + self.label, self.getDPhiMjj(theJets_jecDn)   )  
        
        self.out.fillBranch('drMjj'      + self.label, self.getDRMjj(theJets))
        self.out.fillBranch('minMjj'     + self.label, self.getMinMjj(theJets))
        self.out.fillBranch('maxMjj'     + self.label, self.getMaxMjj(theJets))
        self.out.fillBranch('hardMjj'    + self.label, self.getHardMjj(theJets))
        self.out.fillBranch('hardJJDphi' + self.label, self.getHardMjj(theJets, True))
        self.out.fillBranch('hardJJDR'   + self.label, self.getHardMjj(theJets, True, True))
        self.out.fillBranch('j1MetDPhi'  + self.label, deltaPhi(metphi, theJets[0].phi) if len(theJets) > 0 else -99.)
        self.out.fillBranch('j2MetDPhi'  + self.label, deltaPhi(metphi, theJets[1].phi) if len(theJets) > 1 else -99.)
         
        [wtbtag, wtbtagUp_heavy, wtbtagUp_light, wtbtagDown_heavy, wtbtagDown_light] = (self.getWeightBtag(theJets) if not isData else [1., 1., 1., 1., 1.])

        ################### Applying the trigger weights
        # we can apply these guys on the fly :) 
        #ret['weight_trigger'] = 1.
        #if not isData:
        #    if abs(lepret["Lep1_pdgId"+self.label] * lepret["Lep2_pdgId"+self.label]) == 169: ret['weight_trigger'] = 0.94
        #    if abs(lepret["Lep1_pdgId"+self.label] * lepret["Lep2_pdgId"+self.label]) == 143: ret['weight_trigger'] = 0.89
        #    if abs(lepret["Lep1_pdgId"+self.label] * lepret["Lep2_pdgId"+self.label]) == 121: ret['weight_trigger'] = 0.97

        ################### Applying the b-tagging weights
        self.out.fillBranch('weight_btagsf'          + self.label, wtbtag          )
        self.out.fillBranch('weight_btagsf_heavy_UP' + self.label, wtbtagUp_heavy  )
        self.out.fillBranch('weight_btagsf_heavy_DN' + self.label, wtbtagDown_heavy)
        self.out.fillBranch('weight_btagsf_light_UP' + self.label, wtbtagUp_light  )
        self.out.fillBranch('weight_btagsf_light_DN' + self.label, wtbtagDown_light)

        ################### MLB calculation
        jet = ROOT.TLorentzVector()
        min_mlb = 1e6
        max_mlb = 1e6
        _lmin, _jmin = -1, -1
        _lmax, _jmax = -1, -1
        leplist = [l1, l2]
        for jec in ['', 'Up' ,'Dn']:
            theBJetsForMLB = theBJets if len(jec) == 0 else theBJets_jecUp if 'Up' in jec else theBJets_jecDn
            theJetsForMLB  = theJets  if len(jec) == 0 else theJets_jecUp  if 'Up' in jec else theJets_jecDn
            jet1coll = (theBJets if len(theBJetsForMLB) >= 1 else theJetsForMLB)
            jet2coll = (theBJets if len(theBJetsForMLB) >= 2 else theJetsForMLB)
            if nLepTight > 1:
                for _il,lep in enumerate(leplist):
                    for _ij,j in enumerate(jet1coll):
                        jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)           
                        tmp_mlb = (lep+jet).M()
                        if tmp_mlb < min_mlb:
                            min_mlb = tmp_mlb
                            _lmin = _il
                            _jmin = _ij
                for _il,lep in enumerate(leplist):
                    if _il == _lmin: continue
                    for _ij,j in enumerate(jet2coll):
                        if len(theBJets) == 1 and j.btagDeepB >= self.btagMediumCut:
                            continue
                        if (len(theBJets) == 0 or len(theBJets) >= 2) and _ij == _jmin: continue
                        jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)           
                        tmp_mlb = (lep+jet).M()
                        if tmp_mlb < max_mlb:
                            max_mlb = tmp_mlb
                            _lmax = _il
                            _jmax = _ij
                    
                            
            min_mlb = min_mlb if min_mlb < 1e6  else -1.
            max_mlb = max_mlb if max_mlb < 1e6  else -1.
            
            self.out.fillBranch("min_mlb1%s"%jec + self.label, min_mlb)
            self.out.fillBranch("min_mlb2%s"%jec + self.label, max_mlb)
            self.out.fillBranch("sum_mlb%s"%jec  + self.label, (min_mlb + max_mlb) if min_mlb > 0. and max_mlb> 0. else -1.)
       

        self.out.fillBranch("st" + self.label,  met+lepst[0].pt+lepst[1].pt)


#        for k,v in trigret.iteritems(): 
#            self.out.fillBranch(k+self.label,v) # fullret[k+self.label] = v
            #returned.append(k+self.label)
        # for k,v in edgeisotrackret.iteritems():
        #     fullret["EdgeIsoTracksSel%s_%s" % (self.label,k)] = v
        


        return True
#        for k,v in fullret.iteritems():
            

            
    def setJetCollection(self, jetcoll, lepst):
        for j in jetcoll:
            j._clean = True
            if abs(j.eta) > 2.4 or j.pt < 25.: # Marius change, previus 25 # Now changed to 25 again
                j._clean = False
                continue
            if j.pt < 25 and j.btagDeepB < self.btagMediumCut: 
                j._clean = False
                continue
            for l in lepst:
                #lep = leps[l]
                if deltaR(l,j) < 0.4:
                    j._clean = False
            if j.jetId == 0: j._clean = False
        return jetcoll                                                
    #################################################################################################################
    ######## Atenttion how to do this.                                                                      
    def setFatJetCollection(self, fatjetcoll, jetcoll, lepst):
        ret = []
        for f in fatjetcoll:
            f._clean = True
            #if abs(f.eta) > 2.4 or f.pt < 25.:
            #    f._clean = False
            #    continue
            for l in lepst:
                if deltaR(l,f) < 0.4:
                    f._clean = False
            if f._clean:
                ret.append(f)
        return ret 

    #################################################################################################################

    def checkJetsGenJets(self, coll1):
        flag = True
        if not self.isSMS: return True
        for j in coll1:
            if abs(j.eta) > 2.5 or j.pt < 20: continue # not central
            #if j.mcMatchId != 0:              continue # its matched with a gen jet DeltaR < 0.3

            # Atencion
            var_mcPt = 10.
            if var_mcPt > 8.:              continue # taken from RA5/7 people (ask Nacho)
            if j.chHEF  > 0.1:            continue # charged franction > 0.1
            flag = False # both conditions have failed
        return flag
    #################################################################################################################

    def countJets(self, coll1):
        nb25 = 0; nb25 = 0; nbl25 = 0; nb35 = 0; ht35 = 0.; ht25 = 0; nl35 = 0; n35 = 0; n25 = 0
        thejets = []; thejets25 = []; thebjets = []; thebjets25 = [] ; 
        retlist = []
        for ijc,j in enumerate(coll1):
            if not j._clean: continue
            bt = j.btagDeepB
            pt = j.pt
            if pt > 25 and bt > self.btagMediumCut: 
                nb25 += 1
                thebjets25.append(j)                   
            if pt > 25 and bt > self.btagLooseCut: 
                nbl25 += 1
            if pt > 25:
                n25 += 1 ; ht25 += pt
            if pt > 35:
                thejets.append(j)
                n35 += 1; ht35 += pt
                retlist.append(ijc)          
                if bt > self.btagMediumCut:
                    nb35 += 1
                    thebjets.append(j)
                if bt > self.btagLooseCut:
                    nl35 += 1
        if nb25 == 2: 
            b1 = ROOT.TLorentzVector(); b2 = ROOT.TLorentzVector()
            b1.SetPtEtaPhiM(thebjets25[0].pt, thebjets25[0].eta, thebjets25[0].phi, thebjets25[0].mass)
            b2.SetPtEtaPhiM(thebjets25[1].pt, thebjets25[1].eta, thebjets25[1].phi, thebjets25[1].mass)
            mbb = (b1+b2).M()
        else: mbb = -99
        return retlist, nb25, nbl25,  nb35, nl35, n35, n25, ht35, ht25, thejets, thebjets, mbb, thebjets25                       
    #################################################################################################################

    def countFatJets(self, coll1):
        fatretlist = []
        for ijc,j in enumerate(coll1):
            pt = j.pt
            if pt > 175: 
                fatretlist.append(ijc)          
        return fatretlist 
    #################################################################################################################

    def getMT(self, pt1, pt2, phi1, phi2):
        return math.sqrt(2*pt1*pt2*(1-math.cos(phi1-phi2)))
    #################################################################################################################

    def getMinMT(self, l1, l2, met, lphi1, lphi2, metphi):
        mT1 = math.sqrt(2*l1*met*(1-math.cos(lphi1-metphi)))
        mT2 = math.sqrt(2*l2*met*(1-math.cos(lphi2-metphi)))
        return min(mT1, mT2)
    #################################################################################################################

    def getMll_JZB(self, l1, l2, met):
        metrecoil = (met + l1 + l2).Pt()
        zpt = (l1 + l2).Pt()
        jzb = metrecoil - zpt
        v1 = l1.Vect()
        v2 = l2.Vect()
        return ((l1+l2).M(), jzb, l1.DeltaR(l2), (l1+l2).Phi(), metrecoil, zpt, abs( deltaPhi( l1.Phi(), l2.Phi() )) , v1.Angle(v2))
    #################################################################################################################

    def getParOrtPt(self, l1, l2):
        if l1.Pt() > l2.Pt():
            v1 = l1.Vect()
            v2 = l2.Vect()
        else:
            v1 = l2.Vect()
            v2 = l1.Vect()
        u1 = v1.Unit()                              # direction of the harder lepton
        p1 = math.cos(v1.Angle(v2)) * v2.Mag() * u1 # projection of the softer lepton onto the harder
        o1 = v1 - p1                                # orthogonal to the projection of the softer onto the harder
        return  (p1.Perp(), o1.Perp())
    #################################################################################################################

    def getPairVariables(self,lepst, metp4):
        ret = (-999,-999,-99., -9000.,-99., -99., -99., -99.,-99.,-99.,-99.,-99.,-99.)
        if len(lepst) >= 2:
            [mll, jzb, dr, phi, metrec, zpt, dphi, d3D] = self.getMll_JZB(lepst[0].p4(), lepst[1].p4(), metp4)
            [parPt, ortPt] = self.getParOrtPt(lepst[0].p4(),lepst[1].p4())
            ret = (0, 1, mll, jzb, dr, phi, metrec, zpt, dphi, d3D, parPt, ortPt, lepst[0].p4().Theta() - lepst[1].p4().Theta())
        return ret


    #################################################################################################################

    #def getMllandZptUncorrected(self, lepst):
    #ret = (-99., -99.) # default values
    #if len(lepst) >= 2:
        # Compute new mll and zpt
         

    #return ret                                                                                                                        
    #################################################################################################################

    def getRightMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        return (jetsel[0].p4() + jetsel[1].p4()).M()

    #################################################################################################################

    def getBestMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        bestmjj = 1e6
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if abs(dijetmass - 80.385) < abs(bestmjj - 80.385):
                    bestmjj = dijetmass
        return bestmjj                                                         
    #################################################################################################################

    def getMinMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        minmjj = 1e6
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if dijetmass < minmjj:
                    minmjj = dijetmass
        return minmjj
    #################################################################################################################

    def getMaxMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        maxmjj = -99.
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if dijetmass > maxmjj:
                    maxmjj = dijetmass
        return maxmjj
    #################################################################################################################

    def smearJets(self, jetcol, syst):
	
        for j in jetcol:
            quot = 1.0-getattr(j, "rawFactor") #getattr(j, "CorrFactor_L1L2L3Res") if getattr(j, "CorrFactor_L1L2L3Res") > 0 else getattr(j, "CorrFactor_L1L2L3")
            if syst > 0: 
                j.pt = j.pt_jesTotalUp
            else:
                j.pt = j.pt_jesTotalDown
        return jetcol
    #################################################################################################################

    def getHardMjj(self, jetsel, _dphi = False, _dr = False):
        if len(jetsel) < 2: return -99.
        if not _dphi:
            jet1 = ROOT.TLorentzVector()
            jet2 = ROOT.TLorentzVector()
            jet1.SetPtEtaPhiM(jetsel[0].pt, jetsel[0].eta, jetsel[0].phi, jetsel[0].mass)
            jet2.SetPtEtaPhiM(jetsel[1].pt, jetsel[1].eta, jetsel[1].phi, jetsel[1].mass)
            retval = (jet1+jet2).M()
        else:         
            if not _dr: retval = deltaPhi( jetsel[0].phi, jetsel[1].phi)
            else:       retval = deltaR(jetsel[0], jetsel[1])
        return retval
    #################################################################################################################

    def getDPhiMjj(self, jetsel):                                                               
        if len(jetsel) < 2: return -99.
        dphimjj = 1e6
        dphi = 3.2
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                dphijets = abs(deltaPhi(jeti.phi, jetj.phi)) 
                if dphijets < dphi:   
                    dphi = dphijets
                    jet1 = ROOT.TLorentzVector()
                    jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                    jet2 = ROOT.TLorentzVector()
                    jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                    dijetmass = (jet1+jet2).M()
                    dphimjj = dijetmass
        return dphimjj                                                                       
    #################################################################################################################
            
    def getDRMjj(self, jetsel):                                                    
        if len(jetsel) < 2: return -99.
        drmjj = 1e6
        dr = 1000
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                drjets = abs(deltaR(jeti, jetj)) 
                if drjets < dr:   
                    dr = drjets
                    dijetmass = (jet1+jet2).M()
                    drmjj = dijetmass
        return drmjj  
    #################################################################################################################
  
    def get_SF_btag(self, pt, eta, mcFlavour):

       flavour = 2
       if abs(mcFlavour) == 5: flavour = 0
       elif abs(mcFlavour)==4: flavour = 1

       pt_cutoff  = max(20. ,  pt)
       eta_cutoff = min(2.39, abs(eta))

       if flavour == 2:
          SF = self.reader_light.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFup = self.reader_light.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdown = self.reader_light.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)
          SFcorr = self.reader_light_FASTSIM.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFupcorr = self.reader_light_FASTSIM.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdowncorr = self.reader_light_FASTSIM.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)
       elif flavour == 1:
          SF = self.reader_c.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFup = self.reader_c.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdown = self.reader_c.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)
          SFcorr = self.reader_c_FASTSIM.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFupcorr = self.reader_c_FASTSIM.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdowncorr = self.reader_c_FASTSIM.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)
       else:
          SF = self.reader_heavy.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFup = self.reader_heavy.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdown = self.reader_heavy.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)
          SFcorr = self.reader_heavy_FASTSIM.eval_auto_bounds("central", flavour, eta_cutoff, pt_cutoff)
          SFupcorr = self.reader_heavy_FASTSIM.eval_auto_bounds("up", flavour, eta_cutoff, pt_cutoff)
          SFdowncorr = self.reader_heavy_FASTSIM.eval_auto_bounds("down", flavour, eta_cutoff, pt_cutoff)

       if self.isSMS:
          return [SFcorr, SFupcorr, SFdowncorr]
       else:
          return [SF, SFup, SFdown]
    #################################################################################################################
 
    def getBtagEffFromFile(self, pt, eta, mcFlavour):

       pt_cutoff = max(20.,min(399., pt))
       if (abs(mcFlavour) == 5):
           h = self.h_btag_eff_b
           #use pt bins up to 600 GeV for b
           pt_cutoff = max(20.,min(599., pt))
       elif (abs(mcFlavour) == 4):
           h = self.h_btag_eff_c
       else:
           h = self.h_btag_eff_udsg

       binx = h.GetXaxis().FindBin(pt_cutoff)
       biny = h.GetYaxis().FindBin(abs(eta))

       return h.GetBinContent(binx,biny)
    #################################################################################################################

    def getWeightBtag(self, jets):

        mcTag = 1.
        mcNoTag = 1.
        dataTag = 1.
        dataNoTag = 1.
        errHup   = 0
        errHdown = 0
        errLup   = 0
        errLdown = 0

        for jet in jets:

            csv = jet.btagDeepB
            mcFlavor = (jet.hadronFlavour if hasattr(jet, 'hadronFlavour') else jet.mcFlavour)
            eta = jet.eta
            pt = jet.pt

            if(abs(eta) > 2.5): continue
            if(pt < 20): continue
            eff = self.getBtagEffFromFile(pt, eta, mcFlavor)

            istag = csv > self.btagMediumCut and abs(eta) < 2.5 and pt > 20
            SF = self.get_SF_btag(pt, eta, mcFlavor)
            if(istag):
                 mcTag = mcTag * eff
                 dataTag = dataTag * eff * SF[0]
                 if(mcFlavor == 5 or mcFlavor ==4):
                     errHup  = errHup + (SF[1] - SF[0]  )/SF[0]
                     errHdown = errHdown + (SF[0] - SF[2])/SF[0]
                 else:
                     errLup = errLup + (SF[1] - SF[0])/SF[0]
                     errLdown = errLdown + (SF[0] - SF[2])/SF[0]
            else:
                 mcNoTag = mcNoTag * (1 - eff)
                 dataNoTag = dataNoTag * (1 - eff*SF[0])
                 if mcFlavor==5 or mcFlavor==4:
                     errHup = errHup - eff*(SF[1] - SF[0]  )/(1-eff*SF[0])
                     errHdown = errHdown - eff*(SF[0] - SF[2])/(1-eff*SF[0])
                 else:
                     errLup = errLup - eff*(SF[1] - SF[0])/(1-eff*SF[0])
                     errLdown = errLdown - eff*(SF[0] - SF[2])/(1-eff*SF[0]);


        wtbtag = (dataNoTag * dataTag ) / ( mcNoTag * mcTag )
        wtbtagUp_heavy   = wtbtag*( 1 + errHup   )
        wtbtagUp_light   = wtbtag*( 1 + errLup   )
        wtbtagDown_heavy = wtbtag*( 1 - errHdown )
        wtbtagDown_light = wtbtag*( 1 - errLdown )

        return [wtbtag, wtbtagUp_heavy, wtbtagUp_light, wtbtagDown_heavy, wtbtagDown_light]
    #################################################################################################################

    def selfNewMediumMuonId(self, muon):
        
        #Atencion 
        var_LepGood_globalTrackChi2 = 1 # LepGood_globalTrackChi2
        var_LepGood_chi2LocalPosition = 1 # LepGood_chi2LocalPosition
        var_LepGood_trkKink = 1 # LepGood_trkKink
        var_LepGood_innerTrackValidHitFraction = 1 # LepGood_innerTrackValidhitFraction

        if not hasattr(muon, 'isGlobal'):
            return (muon.mediumId == 1)
        goodGlob = (muon.isGlobal and 
                    var_LepGood_globalTrackChi2 < 3 and
                    var_LepGood_chi2LocalPosition < 12 and
                    var_LepGood_trkKink < 20)
        isMedium = (var_LepGood_innerTrackValidHitFraction > 0.8 and
                    muon.segmentComp > (0.303 if goodGlob else  0.451) )
        return isMedium
        #muon.segmentCompatibility < 0.49: return False
    #################################################################################################################

         
    #################################################################################################################

def newMediumMuonId(muon):

    #Atencion 
    var_LepGood_globalTrackChi2 = 1 # LepGood_globalTrackChi2
    var_LepGood_chi2LocalPosition = 1 # LepGood_chi2LocalPosition
    var_LepGood_trkKink = 1 # LepGood_trkKink
    var_LepGood_innerTrackValidHitFraction = 1 # LepGood_innerTrackValidhitFraction


    if not hasattr(muon, 'isGlobal'):
        return (muon.mediumId == 1)
    goodGlob = (muon.isGlobal and 
                var_LepGood_globalTrackChi2 < 3 and
                var_LepGood_chi2LocalPosition < 12 and
                var_LepGood_trkKink < 20)
    isMedium = (var_LepGood_innerTrackValidHitFraction > 0.8 and
                muon.segmentComp > (0.303 if goodGlob else  0.451) )
    return isMedium
    #muon.segmentCompatibility < 0.49: return False
    #################################################################################################################


def _susyEdgeLoose(lep):
    
    leppt = lep.pt # /lep.eCorr if hasattr(lep,'eCorr') and not lep.eCorr == 0   else lep.pt# eCorr are dis-applied by default
        #leppt = lep.pt # If energy corrections applied

    if leppt <= 5.: return False # Atencion before 10.
    if abs(lep.dxy) > 0.2: return False
    if abs(lep.dz ) > 0.5: return False
    if lep.sip3d > 8: return False
    lepeta = abs(lep.eta)
    if lep.miniPFRelIso_all > 0.4: return False
    ## muons
    if abs(lep.pdgId) == 13:
        if lepeta > 2.4: return False
            #if lep.mediumMuonId != 1: return False
        if not lep.mediumId: return False
    ## electrons
    if abs(lep.pdgId) == 11:
        if lepeta > 2.4: return False
        if (lep.convVeto == 0) or (lep.lostHits == 1): return False
            
        # MVA definition:
        lepeta = abs(lep.eta + lep.deltaEtaSC) # Using supercluster Eta for electrons
        if lepeta < 0.8:
            if leppt>5. and leppt<10.:
                if not lep.mvaFall17V1noIso > 0.488: return False
            if leppt>10. and leppt<25.:
                if not lep.mvaFall17V1noIso > (-0.788 + (0.148/15.)*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > -0.64: return False

        if lepeta > 0.8 and lepeta < 1.479:
            if leppt>5. and leppt<10.:
                if not lep.mvaFall17V1noIso > -0.045: return False
            if leppt>10. and leppt<25.:
                if not lep.mvaFall17V1noIso > (-0.85 + (0.075/15.)*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > -0.775: return False

        if lepeta > 1.479 and lepeta < 2.4:
            if leppt>5. and leppt<10.:
                if not lep.mvaFall17V1noIso > 0.176: return False
            if leppt>10. and leppt<25.:
                if not lep.mvaFall17V1noIso > (-0.81 + (0.077/15.)*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > -0.733: return False

          #  A = -0.86+(-0.85+0.86)*(abs(lep.eta)>0.8)+(-0.81+0.86)*(abs(lep.eta)>1.479)
          #  B = -0.96+(-0.96+0.96)*(abs(lep.eta)>0.8)+(-0.95+0.96)*(abs(lep.eta)>1.479)    
          #  if lep.pt > 10:
                # Atencion delete line below and decomment second line
          #      if not lep.mvaFall17V1Iso: return False
                #if not lep.mvaIdSpring16GP > min( A , max( B , A+(B-A)/10*(lep.pt-15) ) ): return False

          # if (lepeta < 0.8   and lep.mvaIdSpring15 < -0.70) : return False
          # if (lepeta > 0.8   and lepeta < 1.479 and lep.mvaIdSpring15 < -0.83) : return False
          # if (lepeta > 1.479 and lep.mvaIdSpring15 < -0.92) : return False
          #if hasattr(lep, 'idEmuTTH'):
          #  if lep.idEmuTTH == 0: return False
    return True                                                                                  

def _susyEdgeTight(lep):

    leppt = lep.pt # /lep.eCorr if not lep.eCorr == 0 and lep.doCorrections == False else lep.pt# If not energy corrections applied 
    #leppt = lep.pt # If energy corrections applied

    if leppt < 20.: return False
    eta = abs(lep.eta)
    if eta          > 2.4: return False
    if abs(lep.dxy) > 0.05: return False
    if abs(lep.dz ) > 0.10: return False
    if lep.sip3d > 8: return False
    if eta > 1.4 and eta < 1.6: return False
    if abs(lep.pdgId) == 13:
        ## old medium ID if lep.mediumMuonId != 1: return False
        if not lep.mediumId: return False
        if lep.miniPFRelIso_all >= 0.2: return False
        ##if not lep.tightId: return False # Atencion
    if abs(lep.pdgId) == 11:
        # MVA definition:
        etatest = abs(lep.eta + lep.deltaEtaSC) # Using supercluster Eta for electrons
        #etatest = (abs(lep.etaSc) if hasattr(lep, 'etaSc') else abs(lep.eta))
        if (etatest > 1.4442 and etatest < 1.566) : return False

        if (lep.convVeto == 0) or (lep.lostHits > 0) : return False
        #if leppt < 10.: return False
        if lep.miniPFRelIso_all >= 0.1: return False
        if etatest < 0.8:
            if leppt<25:
                if not lep.mvaFall17V1noIso > (0.2 + 0.032*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > 0.68: return False

        if etatest > 0.8 and etatest < 1.479:
            if leppt<25.:                  
                if not lep.mvaFall17V1noIso > (0.1 + 0.025*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > 0.475: return False

        if etatest > 1.479 and etatest < 2.4:
            if leppt<25.:              
                if not lep.mvaFall17V1noIso > (-0.1 + 0.028*(leppt -10.)): return False
            if leppt>=25.:
                if not lep.mvaFall17V1noIso > 0.32: return False



        #A = 0.77+(0.56-0.77)*(abs(lep.eta)>0.8)+(0.48-0.56)*(abs(lep.eta)>1.479)
        #B = 0.52+(0.11-0.52)*(abs(lep.eta)>0.8)+(-0.01-0.11)*(abs(lep.eta)>1.479)    
        #if lep.pt > 10.:
            # Atencion delete line below and decomment second line
        #    if not lep.mvaFall17V1Iso: return False
            #if not (lep.mvaIdSpring16GP > min( A , max( B , A+(B-A)/10*(lep.pt-15) ) )): return False
        #else: return False

        #if lep.miniPFRelIso_all > 0.1: return False
    return True
