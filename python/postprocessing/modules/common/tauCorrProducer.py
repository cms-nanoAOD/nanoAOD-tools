import os
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.helpers.TauIDSFTool import TauIDSFTool, TauESTool
from PhysicsTools.NanoAODTools.postprocessing.tools import ensureTFile, extractTH1
ROOT.PyConfig.IgnoreCommandLineOptions = True
datapath = os.path.join(os.environ['CMSSW_BASE'],"src/PhysicsTools/NanoAODTools/python/postprocessing/data/tau")


class TauCorrectionsProducer(Module):
    
    def __init__(self, year, antiJetID='MVAoldDM2017v2', antiJetWPs=['Tight'],
                             antiEleID='antiEleMVA6',    antiEleWPs=['VLoose','Tight'],
                             antiMuID='antiMu3',         antiMuWPs=['Loose','Tight'],
                             antiJetPerDM=False, sys=True,
                             tes=True, tesSys=True, verbose=True):
        """Choose the IDs and WPs for SFs. For available tau IDs, WPs and corrections, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau"""
        
        if isinstance(antiJetWPs,str): WPs        = [WPs]
        if isinstance(antiEleWPs,str): antiEleWPs = [antiEleWPs]
        if isinstance(antiMuWPs,str):  antiMuWPs  = [antiMuWPs]
        
        # TAU DISCRIMINATOR SFs
        antiJetSFs = [ ]
        antiEleSFs = [ ]
        antiMuSFs  = [ ]
        if antiJetID:
          for wp in antiJetWPs:
            antiJetSFs.append(TauIDSFTool(year,antiJetID,wp,dm=antiJetPerDM,path=datapath,verbose=verbose))
        if antiEleID:
          for wp in antiEleWPs:
            antiEleSFs.append(TauIDSFTool(year,antiEleID,wp,path=datapath,verbose=verbose))
        if antiMuID:
          for wp in antiMuWPs:
            antiMuSFs.append(TauIDSFTool(year,antiMuID,wp,path=datapath,verbose=verbose))
        
        # TAU ENERGY SCALE
        testool = None
        if tes:
          testool = TauESTool(year)
        
        self.antiJetID  = antiJetID
        self.antiJetSFs = antiJetSFs
        self.antiEleID  = antiEleID
        self.antiEleSFs = antiEleSFs
        self.antiMuID   = antiMuID
        self.antiMuSFs  = antiMuSFs
        self.doSys      = sys
        self.doTES      = tes
        self.doTESSys   = tes and tesSys
        self.testool    = testool
        self.verbose    = verbose
    
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """Create branches in output tree."""
        self.out = wrappedOutputTree
        
        cap = lambda s: s[0].upper()+s[1:]
        for tool in self.antiJetSFs+self.antiEleSFs+self.antiMuSFs:
          tool.branchname = "Tau_sf%s_%s"%(cap(tool.ID),tool.WP)
          self.out.branch(tool.branchname,'F',lenVar='nTau',title="scale factor for the %s WP of the %s discriminator"%(tool.WP,tool.ID))
          if self.doSys:
            self.out.branch(tool.branchname+'Up',  'F',lenVar='nTau',title="scale factor for the %s WP of the %s discriminator, up variation"%(tool.WP,tool.ID))
            self.out.branch(tool.branchname+'Down','F',lenVar='nTau',title="scale factor for the %s WP of the %s discriminator, down variation"%(tool.WP,tool.ID))
        
        if self.doTES:
          self.out.branch("Tau_pt_corr",         'F', lenVar='nTau', title="tau pT, corrected with the tau energy scale")
          self.out.branch("Tau_mass_corr",       'F', lenVar='nTau', title="tau mass, corrected with the tau energy scale")
          if self.doTESSys:
            self.out.branch("Tau_pt_corrUp",     'F', lenVar='nTau', title="tau pT, corrected with the tau energy scale, up variation")
            self.out.branch("Tau_mass_corrUp",   'F', lenVar='nTau', title="tau mass, corrected with the tau energy scale, up variation")
            self.out.branch("Tau_pt_corrDown",   'F', lenVar='nTau', title="tau pT, corrected with the tau energy scale, down variation")
            self.out.branch("Tau_mass_corrDown", 'F', lenVar='nTau', title="tau mass, corrected with the tau energy scale, down variation")
    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """Process event, return True (pass, go to next module) or False (fail, go to next event)."""
        
        # BRANCH VALUES
        if self.doSys:
          tau_sfs = {
            'antiJet': { t: ([1.]*event.nTau,[1.]*event.nTau,[1.]*event.nTau) for t in self.antiJetSFs },
            'antiEle': { t: ([1.]*event.nTau,[1.]*event.nTau,[1.]*event.nTau) for t in self.antiEleSFs },
            'antiMu':  { t: ([1.]*event.nTau,[1.]*event.nTau,[1.]*event.nTau) for t in self.antiMuSFs  },
          }      
        else:
          tau_sfs = {
            'antiJet': { t: [1.]*event.nTau for t in self.antiJetSFs },
            'antiEle': { t: [1.]*event.nTau for t in self.antiEleSFs },
            'antiMu':  { t: [1.]*event.nTau for t in self.antiMuSFs  },
          }
        if self.doTES:
          taus_pt_corr         = [ ]
          taus_mass_corr       = [ ]
          if self.doTESSys:
            taus_pt_corrUp     = [ ]
            taus_pt_corrDown   = [ ]
            taus_mass_corrUp   = [ ]
            taus_mass_corrDown = [ ]
        
        # LOOP over TAUS
        taus = Collection(event,'Tau')
        for i, tau in enumerate(taus):
          
          # UNCORRECTED PT / MASS
          if self.doTES:
            taus_pt_corr.append(tau.pt)
            taus_mass_corr.append(tau.mass)
            if self.doTESSys:
              taus_pt_corrUp.append(tau.pt)
              taus_pt_corrDown.append(tau.pt)
              taus_mass_corrUp.append(tau.mass)
              taus_mass_corrDown.append(tau.mass)
          
          # REAL TAU
          if tau.genPartFlav==5:
            dm = tau.decayMode
            for tool in tau_sfs['antiJet']:
              if self.doSys:
                tau_sfs['antiJet'][tool][0][i], tau_sfs['antiJet'][tool][1][i], tau_sfs['antiJet'][tool][2][i] \
                                            = tool.getSFvsPT(tau.pt,unc='All')
              else:
                tau_sfs['antiJet'][tool][i] = tool.getSFvsPT(tau.pt)
            if self.doTES:
              if self.doTESSys:
                tesDown, tes, tesUp    = self.testool.getTES(dm,unc='All')
                taus_pt_corr[i]       *= tes
                taus_pt_corrUp[i]     *= tesUp
                taus_pt_corrDown[i]   *= tesDown
                taus_mass_corr[i]     *= tes
                taus_mass_corrUp[i]   *= tesUp
                taus_mass_corrDown[i] *= tesDown
              else:
                tes                    = self.testool.getTES(dm)
                taus_pt_corr[i]       *= tes
                taus_mass_corr[i]     *= tes
          
          # ELECTRON -> TAU
          elif tau.genPartFlav in [1,3]:
            for tool in tau_sfs['antiEle']:
              if self.doSys:
                tau_sfs['antiEle'][tool][0][i], tau_sfs['antiEle'][tool][1][i], tau_sfs['antiEle'][tool][2][i] \
                                            = tool.getSFvsEta(tau.eta,tau.genPartFlav,unc='All')
              else:
                tau_sfs['antiEle'][tool][i] = tool.getSFvsEta(tau.eta,tau.genPartFlav)
          
          # MUON -> TAU
          elif tau.genPartFlav in [2,4]:
            for tool in tau_sfs['antiMu']:
              if self.doSys:
                tau_sfs['antiMu'][tool][0][i], tau_sfs['antiMu'][tool][1][i], tau_sfs['antiMu'][tool][2][i] \
                                           = tool.getSFvsEta(tau.eta,tau.genPartFlav,unc='All')
              else:
                tau_sfs['antiMu'][tool][i] = tool.getSFvsEta(tau.eta,tau.genPartFlav)
        
        # FILL BRANCHES
        if self.doSys:
          for key, toolSFs in tau_sfs.iteritems():
            for tool, sfs in toolSFs.iteritems():
              self.out.fillBranch(tool.branchname+'Down',sfs[0])
              self.out.fillBranch(tool.branchname,       sfs[1])
              self.out.fillBranch(tool.branchname+'Up',  sfs[2])
        else:
          for key, toolSFs in tau_sfs.iteritems():
            for tool, sfs in toolSFs.iteritems():
              self.out.fillBranch(tool.branchname,sfs)
        if self.doTES:
          self.out.fillBranch("Tau_pt_corr",         taus_pt_corr)
          self.out.fillBranch("Tau_mass_corr",       taus_mass_corr)
          if self.doTESSys:
            self.out.fillBranch("Tau_pt_corrUp",     taus_pt_corrUp)
            self.out.fillBranch("Tau_pt_corrDown",   taus_pt_corrDown)
            self.out.fillBranch("Tau_mass_corrUp",   taus_mass_corrUp)
            self.out.fillBranch("Tau_mass_corrDown", taus_mass_corrDown)
        
        return True
    


# DEFINE modules to avoid having them loaded when not needed
tauCorrs2016Legacy = lambda: TauCorrectionsProducer('2016Legacy')
tauCorrs2017ReReco = lambda: TauCorrectionsProducer('2017ReReco')
tauCorrs2018ReReco = lambda: TauCorrectionsProducer('2018ReReco')
