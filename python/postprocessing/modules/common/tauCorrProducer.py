# Source: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV
import os
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from postprocessors.tauTriggerSFTool import TauTriggerSFTool
ROOT.PyConfig.IgnoreCommandLineOptions = True



class TauCorrectionsProducer(Module):
    
    def __init__(self, year, id='MVAoldDM2017v2', WPs=['tight'],
                             antiEleID='MVAV6',   antiEleWPs=['vloose','tight'],
                             antiMuID='V3',       antiMuWPs=['loose','tight'],
                             triggers=None,       eTauTriggerWPs=['tight'], muTauTriggerWPs=['tight'], diTauTriggerWPs=['tight'],
                             tes=True, tesSys=True):
        """Choose the IDs and WPs for SFs. For available tau IDs and WPs, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau"""
        
        assert year in [2016,2017,2018], "You must choose a year from 2016, 2017, or 2018."
        if isinstance(WPs,str):             WPs             = [WPs]
        if isinstance(antiEleWPs,str):      antiEleWPs      = [antiEleWPs]
        if isinstance(antiMuWPs,str):       antiMuWPs       = [antiMuWPs]
        if isinstance(eTauTriggerWPs,str):  eTauTriggerWPs  = [eTauTriggerWPs]
        if isinstance(muTauTriggerWPs,str): muTauTriggerWPs = [muTauTriggerWPs]
        if isinstance(diTauTriggerWPs,str): diTauTriggerWPs = [diTauTriggerWPs]
        
        # TAU ANTI-JET ID (a.k.a. tau isolation, tau ID)
        antiJetID   = id
        antiJetWPs  = WPs
        antiJetSFs  = { }
        antiJetBits = { }
        if antiJetWPs:
          antiJetSFs_all = {
            2016: {
              'MVAoldDM2017v2': {
                'vvloose': 0.90, 'vloose': 0.90, 'loose': 0.86, 'medium': 0.88, 'tight': 0.87, 'vtight': 0.86, 'vvtight': 0.86 },
            },
            2017: {
              'MVAoldDM2017v2': {
                'vvloose': 0.89, 'vloose': 0.88, 'loose': 0.89, 'medium': 0.89, 'tight': 0.89, 'vtight': 0.86, 'vvtight': 0.84 },
            },
            2018: {
              'MVAoldDM2017v2': {
                'vvloose': 0.86, 'vloose': 0.90, 'loose': 0.90, 'medium': 0.90, 'tight': 0.90, 'vtight': 0.89, 'vvtight': 0.89 },
            },
          }
          antiJetBits_all = {
            'MVAoldDM2017v2': { 'vvloose': 1, 'vloose': 2, 'loose': 4, 'medium': 8, 'tight': 16, 'vtight': 32, 'vvtight': 64 },
          }
          assert year in antiJetSFs_all, "You must choose a year from %s"%(antiJetSFs_all.keys())
          assert antiJetID in antiJetSFs_all[year], "You must choose a tau ID from %s"%(antiJetSFs_all[year].keys())
          for wp in antiJetWPs:
            assert wp in antiJetSFs_all[year][antiJetID], "You must choose a %s WP from %s"%(antiJetID,antiJetSFs_all[year][antiJetID].keys())
            assert wp in antiJetBits_all[antiJetID], "Did not find bit for the %s %s WP, available WPs: %s"%(antiJetID,wp,antiJetBits_all[antiJetID].keys())
            ###if wp not in antiJetSFs_all[year][antiJetID]: continue
            antiJetBits[wp] = antiJetBits_all[antiJetID][wp]
            antiJetSFs[wp]  = antiJetSFs_all[year][antiJetID][wp]
        
        # ANTI ELECTRON ID
        antiEleSFs = { }
        if not antiEleID:
          antiEleWPs = [ ]
        elif antiEleWPs:
          for wp in antiEleWPs:
            antiEleSFs[wp] = antiEleSFTool(year,id=antiEleID,wp=wp)
        
        # ANTI MUON ID
        antiMuSFs = { }
        if not antiMuID:
          antiMuWPs = [ ]
        elif antiMuWPs:
          for wp in antiMuWPs:
            antiMuSFs[wp] = antiMuSFTool(year,id=antiMuID,wp=wp)
        
        # TAU TRIGGER
        triggerSFs = { }
        triggerId  = 'MVAv2'
        for trigger, triggerWPs in [('etau',eTauTriggerWPs),('mutau',muTauTriggerWPs),('ditau',diTauTriggerWPs)]:
          if trigger in triggers:
            triggerkey = trigger.replace('e','Ele').replace('mu','Mu').replace('di','Di').replace('tau','Tau')
            triggerSFs[triggerkey] = { }
            for wp in triggerWPs:
              triggerSFs[triggerkey][wp] = TauTriggerSFTool(trigger,wpType=triggerId,tauWP=wp,year=year)
        
        # TAU ENERGY SCALE
        tes_vals = { }
        if tes:
          tes_vals = { # units of percentage
            2016: { 0: (-0.6,1.0), 1: (-0.5,0.9), 10: ( 0.0,1.1), },
            2017: { 0: ( 0.7,0.8), 1: (-0.2,0.8), 10: ( 0.1,0.9), 11: (-0.1,1.0), },
            2018: { 0: (-1.3,1.1), 1: (-0.5,0.9), 10: (-1.2,0.8), },
          }
          assert year in tes_vals, "You must choose a year from %s"%(tes_vals.keys())
          tes_vals = tes_vals[year]
        
        self.antiJetID   = antiJetID
        self.antiJetBit  = "id"+antiJetID # branch with WP bit
        self.antiJetBits = antiJetBits
        self.antiJetSFs  = antiJetSFs
        self.antiEleID   = antiEleID
        self.antiEleSFs  = antiEleSFs
        self.antiMuID    = antiMuID
        self.antiMuSFs   = antiMuSFs
        self.triggerSFs  = triggerSFs
        self.triggers    = triggers
        self.doTES       = tes
        self.doTESSys    = tesSys and tes
        self.tes_vals    = tes_vals
    
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """Create branches in output tree."""
        self.out = wrappedOutputTree
        
        for wp in self.antiJetSFs:
          self.out.branch("Tau_sf%s_%s"%(self.antiJetID,wp), 'F', lenVar='nTau', title="scale factor for the %s WP of the %s ID"%(wp,self.antiJetID))
        for wp in self.antiEleSFs:
          self.out.branch("Tau_sfAntiEle_%s"%wp, 'F', lenVar='nTau', title="scale factor for the %s WP of the anti-electron discriminator"%wp)
        for wp in self.antiMuSFs:
          self.out.branch("Tau_sfAntiMu_%s"%wp,  'F', lenVar='nTau', title="scale factor for the %s WP of the anti-muon discriminator"%wp)
        for trigger in self.triggerSFs:
          for wp in self.triggerSFs[trigger]:
            self.out.branch("Tau_sf%sTrig_%s"%(trigger,wp), 'F', lenVar='nTau', title="scale factor for the %s WP of the anti-muon discriminator"%wp)
        
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
        taus_antiJetSF_corr    = { wp: [ 1. ]*event.nTau for wp in self.antiJetSFs }
        taus_antiEleSF_corr    = { wp: [ 1. ]*event.nTau for wp in self.antiEleSFs }
        taus_antiMuSF_corr     = { wp: [ 1. ]*event.nTau for wp in self.antiMuSFs  }
        taus_triggerSF_corr    = { tr: { wp: [ 1. ]*event.nTau for wp in self.triggerSFs[tr] } for tr in self.triggerSFs }
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
          dm = tau.decayMode
          
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
            for wp in taus_antiJetSF_corr:
              if self.antiJetBits[wp]<getattr(tau,self.antiJetBit):
                taus_antiJetSF_corr[wp][i] = self.antiJetSFs[wp]
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
          
          # ELECTRON -> TAU FAKE
          elif tau.genPartFlav in [1,3]:
            for wp in taus_antiEleSF_corr:
              taus_antiEleSF_corr[wp][i] = self.antiEleSFs[wp].getSF(tau)
          
          # MUON -> TAU FAKE
          elif tau.genPartFlav in [2,4]:
            for wp in taus_antiMuSF_corr:
              taus_antiMuSF_corr[wp][i] = self.antiMuSFs[wp].getSF(tau)
          
          # TRIGGER SF
          if dm in [0,1,10]:
            for trigger in self.triggerSFs:
              for wp in self.triggerSFs[trigger]:
                taus_triggerSF_corr[trigger][wp][i] = self.triggerSFs[trigger][wp].getTriggerScaleFactor(tau.pt,tau.eta,tau.phi,dm)
        
        # FILL BRANCHES
        for wp in taus_antiJetSF_corr:
          self.out.fillBranch("Tau_sf%s_%s"%(self.antiJetID,wp), taus_antiJetSF_corr[wp])
        for wp in taus_antiEleSF_corr:
          self.out.fillBranch("Tau_sfAntiEle_%s"%wp, taus_antiEleSF_corr[wp])
        for wp in taus_antiMuSF_corr:
          self.out.fillBranch("Tau_sfAntiMu_%s"%wp,  taus_antiMuSF_corr[wp])
        for trigger in self.triggerSFs:
          for wp in self.triggerSFs[trigger]:
            self.out.fillBranch("Tau_sf%sTrig_%s"%(trigger,wp), taus_triggerSF_corr[trigger][wp])
        if self.doTES:
          self.out.fillBranch("Tau_pt_corr",         taus_pt_corr)
          self.out.fillBranch("Tau_mass_corr",       taus_mass_corr)
          if self.doTESSys:
            self.out.fillBranch("Tau_pt_corrUp",     taus_pt_corrUp)
            self.out.fillBranch("Tau_pt_corrDown",   taus_pt_corrDown)
            self.out.fillBranch("Tau_mass_corrUp",   taus_mass_corrUp)
            self.out.fillBranch("Tau_mass_corrDown", taus_mass_corrDown)
        
        return True
    


class antiMuSFTool:
    
    def __init__(self, year, wp='tight', id='anitMuV3'):
        """Initialize tool to get anti-muon discriminator SFs."""
        etabins      = ( 0.4, 0.8, 1.2, 1.7, 2.3 )
        antiMuWP_all = {
          2016: {
            'V3': { 'loose': (1.146, 1.084, 1.218, 1.490, 2.008),
                    'tight': (1.470, 1.367, 1.251, 1.770, 1.713), },
          },
          2017: {
            'V3': { 'loose': (1.061, 1.022, 1.097, 1.030, 1.941),
                    'tight': (1.170, 1.290, 1.140, 0.930, 1.610), },
          },
          2018: {
            'V3': { 'loose': (1.05,  0.96,  1.06,  1.45,  1.75 ),
                    'tight': (1.23,  1.37,  1.12,  1.84,  2.01 ), },
          },
        }
        antiMuWP_bits = {
          'V3': { 'loose': 1, 'tight': 2 },
        }
        assert year in antiMuWP_all, "You must choose a year from %s"%(antiMuWP_all.keys())
        assert id in antiMuWP_all[year], "You must choose an antiMu ID from %s"%(antiMuWP_all[year].keys())
        assert wp in antiMuWP_all[year][id], "You must choose an antiMu %s %s WP from %s"%(id,wp,antiMuWP_all[year][id].keys())
        assert id in antiMuWP_bits and wp in antiMuWP_bits[id], "No bit found for antiMu %s %s WP!"%(id,wp)
        assert len(etabins)==len(antiMuWP_all[year][id][wp]),\
          "Number of bins (%s) must be the same as the number of SFs (%s)."%(len(etabins),len(antiMuWP_all[year][id][wp]))
        
        self.etabins = etabins
        self.SFs     = antiMuWP_all[year][id][wp]
        self.WP      = wp
        self.bit     = "idAntiMu" if id=='V3' else "id"+id
        self.wpbit   = antiMuWP_bits[id][wp]
    
    def getSF(self,tau):
      """Get the SF for a given eta."""
      abseta = abs(tau.eta)
      if getattr(tau,self.bit)<self.wpbit:
        return 0.0
      for etamax, sf in zip(self.etabins,self.SFs):
        if abseta < etamax:
          return sf
      return 1.
    


class antiEleSFTool:
    
    def __init__(self, year, wp='tight', id='MVAV6'):
        """Initialize tool to get anti-electron discriminator SFs."""
        etabins   = ( 1.460, 1.558 )
        antiEleWP_all = {
          2016: {
            'MVAV6': { 'vloose': ( 1.317,  1.547 ),
                       'loose':  ( 1.466,  1.719 ),
                       'medium': ( 1.502,  1.594 ),
                       'tight':  ( 1.486,  1.560 ),
                       'vtight': ( 1.601,  1.401 ), },
          },
          2017: {
            'MVAV6': { 'vloose': ( 1.09,   1.19  ),
                       'loose':  ( 1.17,   1.25  ),
                       'medium': ( 1.40,   1.21  ),
                       'tight':  ( 1.80,   1.53  ),
                       'vtight': ( 1.96,   1.66  ), },
          },
          2018: {
            'MVAV6': { 'vloose': ( 1.130,  1.003 ), # PRELIMINARY
                       'loose':  ( 1.229,  0.926 ),
                       'medium': ( 1.360,  0.910 ),
                       'tight':  ( 1.460,  1.020 ),
                       'vtight': ( 1.560,  1.030 ), },
          },
        }
        antiEleWP_bits = {
          'MVAV6': { 'vloose': 1, 'loose': 2, 'medium': 4, 'tight': 8, 'vtight': 16 },
        }
        assert year in antiEleWP_all, "You must choose a year from %s"%(antiEleWP_all.keys())
        assert id in antiEleWP_all[year], "You must choose an antiEle ID from %s"%(antiEleWP_all[year].keys())
        assert wp in antiEleWP_all[year][id], "You must choose an antiEle %s %s WP from %s"%(id,wp,antiEleWP_all[year][id].keys())
        assert id in antiEleWP_bits and wp in antiEleWP_bits[id], "No bit found for antiEle %s %s WP!"%(id,wp)
        assert len(etabins)==len(antiEleWP_all[year][id][wp]),\
          "Number of bins (%s) must be the same as the number of SFs (%s)."%(len(etabins),len(antiEleWP_all[year][id][wp]))
        
        self.etabins = etabins
        self.SFs     = antiEleWP_all[year][id][wp]
        self.WP      = wp
        self.bit     = "idAntiEle" if id=='MVAV6' else "id"+id
        self.wpbit   = antiEleWP_bits[id][wp]
    
    def getSF(self,tau):
      """Get the SF for a given eta."""
      abseta = abs(tau.eta)
      if getattr(tau,self.bit)<self.wpbit:
        return 0.0
      if abseta < self.etabins[0]:
        return self.SFs[0]
      elif abseta > self.etabins[1]:
        return self.SFs[1]
      return 1.
    


# DEFINE modules to avoid having them loaded when not needed
tauCorrs2016 = lambda: TauCorrectionsProducer(2016)
tauCorrs2017 = lambda: TauCorrectionsProducer(2017)
tauCorrs2018 = lambda: TauCorrectionsProducer(2018)
