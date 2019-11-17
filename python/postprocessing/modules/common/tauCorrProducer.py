import os
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.helpers.TauIDSFTool import TauIDSFTool
ROOT.PyConfig.IgnoreCommandLineOptions = True
#datapath = os.environ['CMSSW_BASE']+"/src/PhysicsTools/NanoAODTools/data/tau/"


class TauCorrectionsProducer(Module):
    
    def __init__(self, year, antiJetID='MVAoldDM2017v2', antiJetWPs=['tight'],
                             antiEleID='antiEleMVA6',    antiEleWPs=['vloose','tight'],
                             antiMuID='antiMu3',         antiMuWPs=['loose','tight'],
                             tes=True, tesSys=True, antiJetPerDM=False):
        """Choose the IDs and WPs for SFs. For available tau IDs, WPs and corrections, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau"""
        
        years = ['2016Legacy','2017ReReco','2018ReReco']
        assert year in years, "You must choose a year from %s."%(', '.join(years))
        if isinstance(antiJetWPs,str): WPs        = [WPs]
        if isinstance(antiEleWPs,str): antiEleWPs = [antiEleWPs]
        if isinstance(antiMuWPs,str):  antiMuWPs  = [antiMuWPs]
        
        antiJetSFs = [ ]
        antiEleSFs = [ ]
        antiMuSFs  = [ ]
        for wp in antiJetWPs:
          antiJetSFs.append(TauIDSFTool(year,antiJetID,wp,dm=antiJetPerDM))
        for wp in antiEleWPs:
          antiEleSFs.append(TauIDSFTool(year,antiEleID,wp))
        for wp in antiMuWPs:
          antiMuSFs.append(TauIDSFTool(year,antiMuID,wp))
        
        # TAU ENERGY SCALE
        # TODO: read from files as well
        tes_vals = { }
        if tes:
          tes_vals = { # units of percentage
            2016: { 0: (-0.6,1.0), 1: (-0.5,0.9), 10: ( 0.0,1.1), },
            2017: { 0: ( 0.7,0.8), 1: (-0.2,0.8), 10: ( 0.1,0.9), 11: (-0.1,1.0), },
            2018: { 0: (-1.3,1.1), 1: (-0.5,0.9), 10: (-1.2,0.8), },
          }
          assert year in tes_vals, "You must choose a year from %s"%(tes_vals.keys())
          tes_vals = tes_vals[year]
        
        self.antiJetID  = antiJetID
        self.antiJetSFs = antiJetSFs
        self.antiEleID  = antiEleID
        self.antiEleSFs = antiEleSFs
        self.antiMuID   = antiMuID
        self.antiMuSFs  = antiMuSFs
        self.doTES      = tes
        self.doTESSys   = tesSys and tes
        self.tes_vals   = tes_vals
    
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """Create branches in output tree."""
        self.out = wrappedOutputTree
        
        for tool in self.antiJetSFs:
          self.out.branch("Tau_sf%s_%s"%(tool.ID,tool.WP), 'F', lenVar='nTau', title="scale factor for the %s WP of the %s ID"%(tool.WP,tool.ID))
        for tool in self.antiEleSFs:
          self.out.branch("Tau_sf%s_%s"%(tool.ID,tool.WP), 'F', lenVar='nTau', title="scale factor for the %s WP of the %s discriminator"%(tool.WP,tool.ID))
        for tool in self.antiMuSFs:
          self.out.branch("Tau_sf%s_%s"%(tool.ID,tool.WP), 'F', lenVar='nTau', title="scale factor for the %s WP of the %s discriminator"%(tool.WP,tool.ID))
        
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
        taus_antiJetSFs         = { t: [ 1. ]*event.nTau for t in self.antiJetSFs }
        taus_antiEleSFs         = { t: [ 1. ]*event.nTau for t in self.antiEleSFs }
        taus_antiMuSFs          = { t: [ 1. ]*event.nTau for t in self.antiMuSFs  }
        if self.doTES:
          taus_pt_corr         = [ ]
          taus_mass_corr       = [ ]
          if self.doTESSys:
            taus_pt_corrUp     = [ ]
            taus_pt_corrDown   = [ ]
            taus_mass_corrUp   = [ ]
            taus_mass_corrDown = [ ]
        
        # LOOP over TAUS
        taus = Collection(event, 'Tau')
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
            for tool in taus_antiJetSFs:
              taus_antiJetSFs[tool][i] = tool.getSFvsPT(tau.pt)
            if self.doTES and dm in self.tes_vals:
              tes                      = 1. + self.tes_vals[dm][0]/100.
              taus_pt_corr[i]         *= tes
              taus_mass_corr[i]       *= tes
              if self.doTESSys:
                tesUp, tesDown         = tes + self.tes_vals[dm][1]/100., tes - self.tes_vals[dm][1]/100.
                taus_pt_corrUp[i]     *= tesUp
                taus_pt_corrDown[i]   *= tesDown
                taus_mass_corrUp[i]   *= tesUp
                taus_mass_corrDown[i] *= tesDown
          
          # ELECTRON -> TAU
          elif tau.genPartFlav in [1,3]:
            for tool in taus_antiEleSFs:
              taus_antiEleSFs[wp][i] = self.antiEleSFs[wp].getSF(tau.eta,tau.genPartFlav)
          
          # MUON -> TAU
          elif tau.genPartFlav in [2,4]:
            for tool in taus_antiMuSFs:
              taus_antiMuSFs[wp][i] = tool.getSFvsEta(tau.eta,tau.genPartFlav)
        
        # FILL BRANCHES
        for tool in taus_antiJetSFs:
          self.out.fillBranch("Tau_sf%s_%s"%(tool.ID,tool.WP),taus_antiJetSFs[tool])
        for tool in taus_antiEleSFs:
          self.out.fillBranch("Tau_sf%s_%s"%(tool.ID,tool.WP),taus_antiEleSFs[tool])
        for tool in taus_antiMuSFs:
          self.out.fillBranch("Tau_sf%s_%s"%(tool.ID,tool.WP),taus_antiMuSFs[tool])
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
