import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
import itertools

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools     import deltaR
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionSkimmer   import CollectionSkimmer
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger_v2 import CollectionMerger


class ObjectCleaning(Module):
    def __init__(self,
                 looseLeptonSelection      ,
                 FOLeptonSelection         , 
                 FOTauSelection            ,
                 jetSelection              ,
                 conePt,
                 cleanElectronsWithMuons   = 0.3,
                 cleanTausWithLooseLeptons = 0.3,
                 cleanJetsWithFOLeps       = True,
                 cleanJetsWithFOTaus       = True
                 ):
        self.looseLeptonSelection      = looseLeptonSelection     
        self.FOLeptonSelection         = FOLeptonSelection        
        self.FOTauSelection            = FOTauSelection           
        self.jetSelection              = jetSelection             
        self.cleanElectronsWithMuons   = cleanElectronsWithMuons  
        self.cleanTausWithLooseLeptons = cleanTausWithLooseLeptons
        self.cleanJetsWithFOLeps       = cleanJetsWithFOLeps      
        self.cleanJetsWithFOTaus       = cleanJetsWithFOTaus      
        self.conePt                    = conePt


        #self._helper_muonFO    = CollectionSkimmer("MuonFO","Muon", maxSize=20)
        #self._helper_elecFO    = CollectionSkimmer("ElecFO","Electron", maxSize=20)
        #self._helper_muonLoose = CollectionSkimmer("MuonLoose","Muon", maxSize=20)
        #self._helper_elecLoose = CollectionSkimmer("ElecLoose","Electron", maxSize=20)

        self._helper_lepFO    = CollectionMerger("LepFO","Electron","Muon", maxSize=20)
        self._helper_tausFO    = CollectionSkimmer("TausFO","Tau", maxSize=20)
        self._helper_jetsSelec = CollectionSkimmer("JetSel","Jet", maxSize=20)
        self._helper_lepLoose = CollectionMerger("ElecLoose","Electron","Muon", maxSize=20)

        self._helpers = [ #self._helper_muonFO,
                          #self._helper_elecFO,
                          #self._helper_muonLoose,
                          #self._helper_elecLoose
                          self._helper_tausFO,
                          self._helper_jetsSelec,
                          self._helper_lepFO,
                          self._helper_lepLoose
                          ] 

    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        for x in self._helpers: 
            x.initInputTree(inputTree)
            x.initOutputTree(wrappedOutputTree)

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        for x in self._helpers: 
            x.initEvent(event)

        muon   = [ o for o in Collection(event, 'Muon')     ]
        elec   = [ o for o in Collection(event, 'Electron') ]
        taus   = [ o for o in Collection(event, 'Tau')      ]
        jets   = [ o for o in Collection(event, 'Jet')      ]

        muonLoose = filter(self.looseLeptonSelection, muon)
        elecLoose = filter(self.looseLeptonSelection, elec)
        
        # this could be external to the code somehow
        for lep in muonLoose+elecLoose:
            setattr(lep, 'conept', self.conePt(lep))
            setattr(lep, 'jetBTagDeepCSV', 0 if lep.jetIdx < 0 else jets[lep.jetIdx].btagDeepB)
        
        # clean loose electrons with loose muons
        if self.cleanElectronsWithMuons: 
            for el in elecLoose:
                for mu in muonLoose:
                    if deltaR(el,mu) < self.cleanElectronsWithMuons: elecLoose.remove(el)
            

        # we define FOs on top of loose leptons
        muonFO    = filter(self.FOLeptonSelection, muonLoose)
        elecFO    = filter(self.FOLeptonSelection, elecLoose)
        tausFO    = filter(self.FOTauSelection,    taus)
        jetsSelec = filter(self.jetSelection,   jets)

        if len(muonFO)+len(elecFO) < 2: return False

        # we clean taus from loose leptons
        if self.cleanTausWithLooseLeptons:
            for tau in tausFO:
                for lep in elecLoose+muonLoose:
                    if deltaR(tau,lep) < self.cleanTausWithLooseLeptons: 
                        tausFO.remove(tau)
                        break

        # we clean jets from FO taus and leps. Here no deltaR but using the matching
        if self.cleanJetsWithFOTaus:
            for tau in tausFO:
                if tau.jetIdx > -1 and jets[tau.jetIdx] in jetsSelec:
                    jetsSelec.remove( jets[tau.jetIdx] ) 

        # we clean jets from FO taus and leps. Here no deltaR but using the matching
        if self.cleanJetsWithFOLeps:
            for jet in jetsSelec:
                for i in range(1,3):
                    if getattr(jet,'electronIdx%d'%i) > -1:
                        if elec[getattr(jet,'electronIdx%d'%i)] in elecFO: 
                            jetsSelec.remove( jet ) 
                            break
                    if getattr(jet,'muonIdx%d'%i) > -1:
                        if muon[getattr(jet,'muonIdx%d'%i)] in muonFO: 
                            jetsSelec.remove( jet ) 
                            break

        # writing out taus and jets
        for x in tausFO:    self._helper_tausFO   ._impl.push_back(taus.index(x))
        for x in jetsSelec: self._helper_jetsSelec._impl.push_back(jets.index(x))

        # moving into tuples of (Collection index, pt, index). 
        muonFO_idx = [(1, x.pt, muon.index(x)) for x in muonFO]
        elecFO_idx = [(0, x.pt, elec.index(x)) for x in elecFO]

        muonLoose_idx = []; elecLoose_idx = [] 
        for x in  muonLoose:
            if x not in muonFO: muonLoose_idx.append( (1, x.pt, muon.index(x)) )
        for x in  elecLoose:
            if x not in elecFO: elecLoose_idx.append( (0, x.pt, elec.index(x)) )

        lepFO_idx    = muonFO_idx + elecFO_idx      ; lepFO_idx.sort(key = lambda x : x[1], reverse=True)
        lepLoose_idx = muonLoose_idx + elecLoose_idx; lepLoose_idx.sort(key = lambda x : x[1], reverse=True)

        for x in lepFO_idx    : self._helper_lepFO   ._impl.push_back(x[2],x[0])
        for x in lepLoose_idx : self._helper_lepLoose._impl.push_back(x[2],x[0])

        return True
