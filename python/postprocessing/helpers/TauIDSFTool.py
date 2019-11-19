import os
from PhysicsTools.NanoAODTools.postprocessing.tools import ensureTFile, extractTH1
datapath  = os.path.join(os.environ['CMSSW_BASE'],"src/PhysicsTools/NanoAODTools/python/postprocessing/data/tau")
campaigns = ['2016Legacy','2017ReReco','2018ReReco']


class TauIDSFTool:
    
    def __init__(self, year, id, wp='Tight', dm=False, path=datapath, verbose=False):
        """Choose the IDs and WPs for SFs. For available tau IDs and WPs, check
        https://github.com/cms-tau-pog/TauIDSFs
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html#Tau"""
        
        assert year in campaigns, "You must choose a year from %s."%(', '.join(campaigns))
        self.ID      = id
        self.WP      = wp
        self.verbose = verbose
        
        if id in ['MVAoldDM2017v2','DeepTau2017v2p1VSjet']:
          if dm:
            file = ensureTFile(os.path.join(path,"TauID_SF_dm_%s_%s.root"%(id,year)),verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.DMs = [0,1,10] if 'oldDM' in id else [0,1,10,11]
            self.getSFvsPT  = self.disabled
            self.getSFvsEta = self.disabled
          else:
            file = ensureTFile(os.path.join(path,"TauID_SF_pt_%s_%s.root"%(id,year)),verbose=verbose)
            self.func         = { }
            self.func[None]   = file.Get("%s_cent"%(wp))
            self.func['Up']   = file.Get("%s_up"%(wp))
            self.func['Down'] = file.Get("%s_down"%(wp))
            file.Close()
            self.getSFvsDM  = self.disabled
            self.getSFvsEta = self.disabled
        elif id in ['antiMu3','antiEleMVA6']:
            file = ensureTFile(os.path.join(path,"TauID_SF_eta_%s_%s.root"%(id,year)),verbose=verbose)
            self.hist = extractTH1(file,wp)
            self.hist.SetDirectory(0)
            file.Close()
            self.genmatches = [1,3] if 'ele' in id.lower() else [2,4]
            self.getSFvsPT  = self.disabled
            self.getSFvsDM  = self.disabled
        else:
          raise IOError("Did not recognize tau ID '%s'!"%id)
        
    def getSFvsPT(self, pt, genmatch=5, unc=None):
        """Get tau ID SF vs. tau pT."""
        if genmatch==5:
          if unc=='All':
            return self.func['Down'].Eval(pt), self.func[None].Eval(pt), self.func['Up'].Eval(pt)
          return self.func[unc].Eval(pt)
        return 1.0
        
    def getSFvsDM(self, pt, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau DM."""
        if dm in self.DMs or pt<40:
          if genmatch==5:
            bin = self.hist.GetXaxis().FindBin(dm)
            sf  = self.hist.GetBinContent(bin)
            if unc=='Up':
              sf += self.hist.GetBinError(bin)
            elif unc=='Down':
              sf -= self.hist.GetBinError(bin)
            elif unc=='All':
              return sf-self.hist.GetBinError(bin), sf, sf+self.hist.GetBinError(bin)
            return sf
          return 1.0
        return 0.0
        
    def getSFvsEta(self, eta, genmatch, unc=None):
        """Get tau ID SF vs. tau eta."""
        eta = abs(eta)
        if genmatch in self.genmatches:
          bin = self.hist.GetXaxis().FindBin(eta)
          sf  = self.hist.GetBinContent(bin)
          if unc=='Up':
            sf += self.hist.GetBinError(bin)
          elif unc=='Down':
            sf -= self.hist.GetBinError(bin)
          elif unc=='All':
            return sf-self.hist.GetBinError(bin), sf, sf+self.hist.GetBinError(bin)
          return sf
        return 1.0
        
    @staticmethod
    def disabled(*args,**kwargs):
        raise AttributeError("Disabled method.")
    

class TauESTool:
    
    def __init__(self, year, path=datapath):
        """Choose the IDs and WPs for SFs."""
        assert year in campaigns, "You must choose a year from %s."%(', '.join(campaigns))
        file = ensureTFile(os.path.join(datapath,"TauES_dm_%s.root"%year))
        self.hist = extractTH1(file,'tes')
        self.hist.SetDirectory(0)
        file.Close()
        
    def getTES(self, dm, genmatch=5, unc=None):
        """Get tau ID SF vs. tau DM."""
        if genmatch==5:
          bin = self.hist.GetXaxis().FindBin(dm)
          tes = self.hist.GetBinContent(bin)
          if unc=='Up':
            tes += self.hist.GetBinError(bin)
          elif unc=='Down':
            tes -= self.hist.GetBinError(bin)
          elif unc=='All':
            return tes-self.hist.GetBinError(bin), tes, tes+self.hist.GetBinError(bin)
          return tes
        return 1.0
    
