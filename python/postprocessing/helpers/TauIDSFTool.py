# Author: Izaak Neutelings (July 2019)
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
# Source: https://github.com/cms-tau-pog/TauIDSFs
from __future__ import print_function
import os
from math import sqrt
from PhysicsTools.NanoAODTools.postprocessing.tools import ensureTFile, extractTH1
datapath  = os.path.join(os.environ.get('CMSSW_BASE','CMSSW_BASE'),"src/PhysicsTools/NanoAODTools/python/postprocessing/data/tau")
campaigns = [
  '2016Legacy','2017ReReco','2018ReReco',
  'UL2016_preVFP', 'UL2016_postVFP', 'UL2017', 'UL2018',
]


class TauIDSFTool:
    
    def __init__(self, year, id, wp='Tight', dm=False, emb=False,
                 otherVSlepWP=False, path=datapath, verbose=False):
        """Choose the IDs and WPs for SFs. For available tau IDs and WPs, check
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau
        Options:
          dm:           use decay mode-dependent SFs
          emb:          use SFs for embedded samples
          otherVSlepWP: extra uncertainty if you are using a different DeepTauVSe/mu WP than used in the measurement
        """
        if "UL" in year and "VSmu" in id:
          print(">>> TauIDSFTool: Warning! Using pre-UL (%r) SFs for %s..."%(year,id))
          year = '2016Legacy' if '2016' in year else '2017ReReco' if '2017' in year else '2018ReReco'
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        self.ID       = id
        self.WP       = wp
        self.verbose  = verbose
        self.extraUnc = None
        
        if id in ['MVAoldDM2017v2','DeepTau2017v2p1VSjet']:
          if dm: # DM-dependent SFs
            if emb:
              if 'oldDM' in id:
                raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
              else:
                file = ensureTFile(os.path.join(path,"TauID_SF_dm_%s_%s_EMB.root"%(id,year)),verbose=verbose)
            else:
              file = ensureTFile(os.path.join(path,"TauID_SF_dm_%s_%s.root"%(id,year)),verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.DMs = [0,1,10] if 'oldDM' in id else [0,1,10,11]
            self.getSFvsPT  = self.disabled
            self.getSFvsEta = self.disabled
            if otherVSlepWP:
              if emb:
                self.extraUnc = 0.05
              else:
                self.extraUnc = 0.03
          else: # pT-dependent SFs
            if emb:
              if 'oldDM' in id:
                raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
              else:
                file = ensureTFile(os.path.join(path, "TauID_SF_pt_%s_%s_EMB.root"%(id,year)),verbose=verbose)
            else:
              file = ensureTFile(os.path.join(path,"TauID_SF_pt_%s_%s.root"%(id,year)),verbose=verbose)
            self.func         = { }
            self.func[None]   = file.Get("%s_cent"%(wp))
            self.func['Up']   = file.Get("%s_up"%(wp))
            self.func['Down'] = file.Get("%s_down"%(wp))
            file.Close()
            self.getSFvsDM  = self.disabled
            self.getSFvsEta = self.disabled
            if otherVSlepWP:
              if emb:
                self.extraUnc = lambda pt: (0.05 if pt<100 else 0.15)
              else:
                self.extraUnc = lambda pt: (0.03 if pt<100 else 0.15)
        elif id in ['antiMu3','antiEleMVA6','DeepTau2017v2p1VSmu','DeepTau2017v2p1VSe']:
            if emb:
              raise IOError("Scale factors for embedded samples not available for ID '%s'!"%id)
            else:
              file = ensureTFile(os.path.join(path,"TauID_SF_eta_%s_%s.root"%(id,year)),verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.genmatches = [1,3] if any(s in id.lower() for s in ['ele','vse']) else [2,4]
            self.getSFvsPT  = self.disabled
            self.getSFvsDM  = self.disabled
        else:
          raise IOError("Did not recognize tau ID '%s'!"%id)
    
    def getSFvsPT(self, pt, genmatch=5, unc=None):
        """Get tau ID SF vs. tau pT."""
        if genmatch==5:
          if self.extraUnc:
            sf       = self.func[None].Eval(pt)
            extraUnc = self.extraUnc(pt)
            errDown  = sqrt( (sf-self.func['Down'].Eval(pt))**2 + (sf*extraUnc)**2 )
            errUp    = sqrt( (sf-self.func['Up'  ].Eval(pt))**2 + (sf*extraUnc)**2 )
            if unc=='All':
              return sf-errDown, sf, sf+errUp
            elif unc=='Up':
              return sf+errUp
            elif unc=='Down':
              sfDown = (sf-errDown) if errDown<sf else 0.0 # prevent negative SF
              return sfDown
          else:
            if unc=='All':
              return self.func['Down'].Eval(pt), self.func[None].Eval(pt), self.func['Up'].Eval(pt)
          return self.func[unc].Eval(pt)
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    def getSFvsDM(self, pt, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau DM."""
        if genmatch==5 and dm in self.DMs and pt>40:
          bin = self.hist.GetXaxis().FindBin(dm)
          sf  = self.hist.GetBinContent(bin)
          err = self.hist.GetBinError(bin)
          if self.extraUnc:
            err = sqrt( err**2 + (sf*self.extraUnc)**2 )
          if unc=='Up':
            sf += err
          elif unc=='Down':
            sf = (sf-err) if err<sf else 0.0 # prevent negative SF
          elif unc=='All':
            sfDown = (sf-err) if err<sf else 0.0 # prevent negative SF
            return sfDown, sf, sf+err
          return sf
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    def getSFvsEta(self, eta, genmatch, unc=None):
        """Get tau ID SF vs. tau eta."""
        eta = abs(eta)
        if genmatch in self.genmatches:
          bin = self.hist.GetXaxis().FindBin(eta)
          sf  = self.hist.GetBinContent(bin)
          err = self.hist.GetBinError(bin)
          if self.extraUnc:
            err = sqrt( err**2 + (sf*self.extraUnc)**2 )
          if unc=='Up':
            sf += err
          elif unc=='Down':
            sf = (sf-err) if err<sf else 0.0 # prevent negative SF
          elif unc=='All':
            sfDown = (sf-err) if err<sf else 0.0 # prevent negative SF
            return sfDown, sf, sf+err
          return sf
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    @staticmethod
    def disabled(*args,**kwargs):
        raise AttributeError("Disabled method.")
    

class TauESTool:
    def __init__(self, year, id='DeepTau2017v2p1VSjet', path=datapath):
        """Choose the IDs and WPs for SFs."""
        if "UL" in year:
          print(">>> TauESTool: Warning! Using pre-UL (%r) TESs at high pT (for uncertainties only)..."%(year))
          year_highpt = '2016Legacy' if '2016' in year else '2017ReReco' if '2017' in year else '2018ReReco'
        else:
          year_highpt = year
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        assert year_highpt in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year_highpt)
        file_lowpt  = ensureTFile(os.path.join(path,"TauES_dm_%s_%s.root"%(id,year)))
        file_highpt = ensureTFile(os.path.join(path,"TauES_dm_%s_%s_ptgt100.root"%(id,year_highpt)))
        self.hist_lowpt  = extractTH1(file_lowpt,'tes')
        self.hist_highpt = extractTH1(file_highpt,'tes')
        self.hist_lowpt.SetDirectory(0)
        self.hist_highpt.SetDirectory(0)
        self.pt_low  = 34  # average pT in Z -> tautau measurement (incl. in DM)
        self.pt_high = 170 # average pT in W* -> taunu measurement (incl. in DM)
        self.DMs     = [0,1,10] if "oldDM" in id else [0,1,10,11]
        file_lowpt.Close()
        file_highpt.Close()
    
    def getTES(self, pt, dm, genmatch=5, unc=None):
        """Get tau ES vs. tau DM."""
        if genmatch==5 and dm in self.DMs:
          bin = self.hist_lowpt.GetXaxis().FindBin(dm)
          tes = self.hist_lowpt.GetBinContent(bin)
          if unc!=None:
            if pt>=self.pt_high: # high pT
              bin_high = self.hist_highpt.GetXaxis().FindBin(dm)
              err      = self.hist_highpt.GetBinError(bin_high)
            elif pt>self.pt_low: # linearly interpolate between low and high pT
              bin_high = self.hist_highpt.GetXaxis().FindBin(dm)
              err_high = self.hist_highpt.GetBinError(bin_high)
              err_low  = self.hist_lowpt.GetBinError(bin)
              err      = err_low + (err_high-err_low)/(self.pt_high-self.pt_low)*(pt-self.pt_low)
            else: # low pT
              err      = self.hist_lowpt.GetBinError(bin)
            if unc=='Up':
              tes += err
            elif unc=='Down':
              tes = (tes-err) if err<tes else 0.0 # prevent negative TES
            elif unc=='All':
              tesDown = (tes-err) if err<tes else 0.0 # prevent negative TES
              return tesDown, tes, tes+err
          return tes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
    def getTES_highpt(self, dm, genmatch=5, unc=None):
        """Get tau ES vs. tau DM for pt > 100 GeV"""
        if genmatch==5 and dm in self.DMs:
          bin = self.hist_highpt.GetXaxis().FindBin(dm)
          tes = self.hist_highpt.GetBinContent(bin)
          err = self.hist_highpt.GetBinError(bin)
          if unc=='Up':
            tes += err
          elif unc=='Down':
            tes = (tes-err) if err<tes else 0.0 # prevent negative TES
          elif unc=='All':
            tesDown = (tes-err) if err<tes else 0.0 # prevent negative TES
            return tesDown, tes, tes+err
          return tes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    

class TauFESTool:
    
    def __init__(self, year, id='DeepTau2017v2p1VSe', path=datapath):
        """Choose the IDs and WPs for SFs."""
        if "UL" in year:
          print(">>> TauFESTool: Warning! Using pre-UL (%r) energy scales for e -> tau fakes..."%(year))
          year = '2016Legacy' if '2016' in year else '2017ReReco' if '2017' in year else '2018ReReco'
        assert year in campaigns, "You must choose a year from %s! Got %r."%(', '.join(campaigns),year)
        file  = ensureTFile(os.path.join(path,"TauFES_eta-dm_%s_%s.root"%(id,year)))
        graph = file.Get('fes')
        FESs  = { 'barrel':  { }, 'endcap': { } }
        DMs   = [0,1]
        i     = 0
        for region in ['barrel','endcap']:
          for dm in DMs:
            y    = graph.GetY()[i]
            yup  = graph.GetErrorYhigh(i)
            ylow = graph.GetErrorYlow(i)
            FESs[region][dm] = (max(0,y-ylow),y,y+yup) # prevent negative FES
            i += 1
        file.Close()
        self.FESs       = FESs
        self.DMs        = [0,1]
        self.genmatches = [1,3]
    
    def getFES(self, eta, dm, genmatch=1, unc=None):
        """Get electron -> tau FES vs. tau DM."""
        if dm in self.DMs and genmatch in self.genmatches:
          region = 'barrel' if abs(eta)<1.5 else 'endcap'
          fes    = self.FESs[region][dm]
          if unc=='Up':
            fes = fes[2]
          elif unc=='Down':
            fes = fes[0]
          elif unc!='All':
            fes = fes[1]
          return fes
        elif unc=='All':
          return 1.0, 1.0, 1.0
        return 1.0
    
