import ROOT
import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR


class HggSelector(Module):
    def __init__(self, data, year="2016"):
        self.data = data
        self.year = year
        
        ### ref link useful later on
        ### reduced JES uncertainties (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECUncertaintySources#Run_2_reduced_set_of_uncertainty)
       
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("passedGoodPhotons","B")
        self.out.branch("passedHPhotons","B")        
        self.out.branch("passedOneTAGHPhotons","B")
        self.out.branch("passedDigammaPair","B")
        self.out.branch("passedDigammaMass","B")
        
        self.out.branch("gHidx",  "I", 2);    
        self.out.branch("gTAGidx",  "I");  
        self.out.branch("gPROBEidx",  "I");  
        self.out.branch("gg_mass", "F");  
        self.out.branch("gg_pt",   "F"); 
        self.out.branch("gg_eta",  "F"); 
        self.out.branch("gg_phi",  "F"); 

        self.out.branch("gHidxNP",  "I", 2);    
        self.out.branch("gg_massNP", "F");  
        self.out.branch("gg_ptNP",   "F"); 
        self.out.branch("gg_etaNP",  "F"); 
        self.out.branch("gg_phiNP",  "F"); 
        
        self.out.branch("probe_Pho_r9",     "F"); 
        self.out.branch("probe_sc_abseta",  "F"); 
        self.out.branch("pair_mass",        "F"); 
        self.out.branch("passingPresel",    "I"); 
        
        self.out.branch("totWeight",    "F");
                
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def useLowR9(self, photon, rho, isEB):
        if (isEB):        
            if ( (photon.sieie >= 0.015) ): 
                return False     
            if ( (photon.trkSumPtHollowConeDR03 >= 6.0) ): 
                return False     
            if ( (photon.pfPhoIso03 - 0.16544*rho >= 4.0) ): 
                return False      
        else:
            if ( (photon.sieie >= 0.035) ): 
                return False;       
            if ( (photon.trkSumPtHollowConeDR03 >= 6.0) ): 
                return False      
            if ( (photon.pfPhoIso03 - 0.13212*rho >= 4.0) ): 
                return False       

        # 0.16544 and 0.13212 are copied from flashggPreselectedDiPhotons_cfi.py
        return True

    
    def analyze(self, event):
        
        """process event, return True (go to next module) or False (fail, go to next event)"""

        photons = list(Collection(event, "Photon"))  
        trigObj = list(Collection(event, "TrigObj"))  
        
        rho = getattr(event, "fixedGridRhoFastjetAll") # fixedGridRhoAll
        
        HLT=1
        if(self.year==2017):
          HLT = getattr(event, "HLT_Ele32_WPTight_Gsf_L1DoubleEG")
        elif(self.year==2016):
          HLT = getattr(event, "HLT_Ele32_eta2p1_WPTight_Gsf")
        elif(self.year==2018):
          HLT = getattr(event, "HLT_Ele32_WPTight_Gsf_L1DoubleEG")
        #rho = getattr(event, "Rho_fixedGridRhoFastjetAll")

        genweight=1
        if (self.data==False):
           genweight = getattr(event, "genWeight")
        signgw=int(genweight>0)-int(genweight<0)
        
        v1 = ROOT.TLorentzVector()
        v2 = ROOT.TLorentzVector()
        
        passedGoodPhotons=False
        passedHPhotons=False
        passedOneTAGHPhotons=False
        passedDigammaPair=False
        passedDigammaMass=False
        
        gHidx=[-1,-1]
        ggMass=-1
        ggPt=-1
        ggEta=-1
        ggPhi=-1     
        gTAGidx=-1
        gPROBEidx=-1
        
        gHidxNP=[-1,-1]
        ggMassNP=-1
        ggPtNP=-1
        ggEtaNP=-1
        ggPhiNP=-1        
                
        photons_sorted=sorted(photons, key=lambda x : x.pt, reverse=True)
        photons_sorted=photons_sorted[0:2]
        
        if (len(photons_sorted)>1):        
            gHidxNP[0]=photons.index(photons_sorted[0])
            gHidxNP[1]=photons.index(photons_sorted[1])
            v1.SetPtEtaPhiM(photons[gHidxNP[0]].pt,photons[gHidxNP[0]].eta,photons[gHidxNP[0]].phi,0)
            v2.SetPtEtaPhiM(photons[gHidxNP[1]].pt,photons[gHidxNP[1]].eta,photons[gHidxNP[1]].phi,0)
            ggMassNP=(v1+v2).M()
            ggPtNP=(v1+v2).Pt()
            ggEtaNP=(v1+v2).Eta()
            ggPhiNP=(v1+v2).Phi()
        
        
        pho_EB_highR9 = lambda x : (abs(x.eta) < 1.5 and x.r9 > 0.85)
        pho_EE_highR9 = lambda x : (abs(x.eta) > 1.5 and x.r9 > 0.9)
        pho_EB_lowR9 = lambda x : (abs(x.eta) < 1.5 and x.r9 < 0.85 and x.r9 > 0.5 and self.useLowR9(x,rho,True))
        pho_EE_lowR9 = lambda x : (abs(x.eta) > 1.5 and x.r9 < 0.9 and x.r9 > 0.8 and self.useLowR9(x,rho,False))

        photonsGood = [ph for ph in photons_sorted if (ph.electronVeto<0.5 and (pho_EB_highR9(ph) or pho_EE_highR9(ph) or pho_EB_lowR9(ph) or pho_EE_lowR9(ph)))]
        if (len(photonsGood)>1):
            passedGoodPhotons=True
        
        #same as in analysis (I added mvaID wrt to latest postproc)
        photonsForHiggs = [ph for ph in photonsGood if (ph.mvaID>-0.7 and ph.hoe<0.08 and abs(ph.eta)<2.5 and (abs(ph.eta)<1.442 or abs(ph.eta)>1.566)  and (ph.r9>0.8 or ph.chargedHadronIso<20 or ph.chargedHadronIso/ph.pt<0.3) )]
        photonsForHiggs=sorted(photonsForHiggs, key=lambda x : x.pt, reverse=True)
        if (len(photonsForHiggs)>1):
            passedHPhotons=True            
            
        ##### now add TAG definition
        ###(abs(superCluster.eta)<=2.1) && !(1.4442<=abs(superCluster.eta)<=1.566) && pt > 40. && full5x5_r9 > 0.8 && pfChgIso03WrtVtx0 < 20.0 && (pfChgIso03WrtVtx0/pt)<=0.3
        #tag selection and matched to HLT object by dR < 0.3
        photonsForTAG = [ph for ph in photonsForHiggs if ( (abs(ph.eta)<2.1)  and (ph.r9>0.8 and  ph.chargedHadronIso<20 and ph.chargedHadronIso/ph.pt<0.3) and ph.pt>40 )]
        photonsForTAG_tMacth=[]
        for ph in photonsForTAG:
          for obj in trigObj:
            if deltaR(obj,ph)<0.3:
              photonsForTAG_tMacth.append(ph)
        if (len(photonsForTAG_tMacth)>0):
            passedOneTAGHPhotons=True
        
        idtag=-1
        indices=[photons.index(photonsForHiggs[i]) for i in range(len(photonsForHiggs))]
        #print indices
        if (passedOneTAGHPhotons):
          idtag=photons.index(photonsForTAG_tMacth[0])
          if (idtag==indices[0] or idtag==indices[1]):
            indices=indices[0:2]
          else:
            indices=[indices[0],idtag]
        #print indices,idtag
        #digamma pair
        
        #for ind in indices:
          #print photons[ind].pt, "-",
        #print ""
        #for ph in photonsForHiggs:
          #print ph.pt, "+",
        #print ""
        
        if (len(photonsForHiggs)>1 and photons[indices[0]].pt >30 and photons[indices[1]].pt>20  ):
            passedDigammaPair=True
            gHidx[0]=indices[0]
            gHidx[1]=indices[1]
            gTAGidx=idtag
            gPROBEidx= gHidx[1] if gTAGidx==gHidx[0] else gHidx[0]
            
            
        if (gHidx[0]>=0 and gHidx[1]>=0):
            v1.SetPtEtaPhiM(photons[gHidx[0]].pt,photons[gHidx[0]].eta,photons[gHidx[0]].phi,0)
            v2.SetPtEtaPhiM(photons[gHidx[1]].pt,photons[gHidx[1]].eta,photons[gHidx[1]].phi,0)
            ggMass=(v1+v2).M()
            ggPt=(v1+v2).Pt()
            ggEta=(v1+v2).Eta()
            ggPhi=(v1+v2).Phi()
            
        if(ggMass>60 and ggMass<120):
          passedDigammaMass=True

        self.out.fillBranch("gg_massNP",ggMassNP)
        self.out.fillBranch("gg_ptNP",ggPtNP)
        self.out.fillBranch("gg_etaNP",ggEtaNP)
        self.out.fillBranch("gg_phiNP",ggPhiNP)
        self.out.fillBranch("gHidxNP",gHidxNP)
        
        self.out.fillBranch("gg_mass",ggMass)
        self.out.fillBranch("gg_pt",ggPt)
        self.out.fillBranch("gg_eta",ggEta)
        self.out.fillBranch("gg_phi",ggPhi)
        
        self.out.fillBranch("passedGoodPhotons",passedGoodPhotons)
        self.out.fillBranch("passedHPhotons",passedHPhotons)
        self.out.fillBranch("passedDigammaPair",passedDigammaPair)
        self.out.fillBranch("passedOneTAGHPhotons",passedOneTAGHPhotons and HLT>0 )
        self.out.fillBranch("passedDigammaMass",passedDigammaMass)
        self.out.fillBranch("gTAGidx",gTAGidx)
        self.out.fillBranch("gPROBEidx",gPROBEidx)
        self.out.fillBranch("gHidx",gHidx)
        
        
        self.out.fillBranch("pair_mass",ggMassNP)
        self.out.fillBranch("probe_sc_abseta",abs(photons[gPROBEidx].eta))
        self.out.fillBranch("probe_Pho_r9",photons[gPROBEidx].r9)
        self.out.fillBranch("passingPresel",passedDigammaPair and HLT>0)
        
        self.out.fillBranch("totWeight",signgw)
        
        #default
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

TnP2016 = lambda : HggSelector(data = False, year="2016") 
TnP2017 = lambda : HggSelector(data = False, year="2017")     
TnP2018 = lambda : HggSelector(data = False, year="2018")    

TnPData2016 = lambda : HggSelector(data = True, year="2016")       
TnPData2017 = lambda : HggSelector(data = True, year="2017")
TnPData2018 = lambda : HggSelector(data = True, year="2018") 


    #myoptions['TnPPATHS']              = cms.vstring("HLT_Ele32_WPTight_Gsf_L1DoubleEG_v*") #HLT_Ele32_WPTight_Gsf_L1DoubleEG_v* for 2017 #HLT_Ele27_WPTight_Gsf_v* for Moriond17
    #myoptions['TnPHLTTagFilters']      = cms.vstring("hltEle32L1DoubleEGWPTightGsfTrackIsoFilter","hltEGL1SingleEGOrFilter")  


#:HLT_Ele32_WPTight_Gsf_L1DoubleEG


#Error in <TTreeFormula::Compile>:  Empty String
#***********************************************************************************************
#*    Row   * Instance *           * TrigObj_p * TrigObj_e * TrigObj_p * TrigObj_i * TrigObj_f *
#***********************************************************************************************
#*        0 *        0 *           *  52.59375 * 1.4716796 * 2.0429687 *        11 *      7199 *
#*        0 *        1 *           * 56.085937 * 1.5771484 * -1.079589 *        11 *      7199 *
#*        0 *        2 *           * 63.421875 * 1.5776367 * -1.083007 *        15 *        22 *
#*        0 *        3 *           * 55.390625 * 1.4731445 * 2.0566406 *        15 *        23 *
#*        0 *        4 *           * 63.257812 * 1.5776367 * -1.083496 *        15 *        23 *
#*        1 *        0 *           *           *           *           *           *           *
#*        2 *        0 *           *  34.09375 * -0.860595 * -2.617187 *        11 *      4113 *
#*        2 *        1 *           * 48.476562 * -1.472656 * 0.5009765 *        11 *      5143 *
#*        3 *        0 *           * 56.960937 * 1.9179687 * -1.605957 *        11 *      7191 *
#*        4 *        0 *           * 47.234375 * 2.1044921 * -0.168518 *        11 *      5143 *
#*        4 *        1 *           * 35.578125 * 2.1064453 * 2.8662109 *        11 *      5143 *
#*        5 *        0 *           *           *           *           *           *           *
#*        6 *        0 *           * 36.585937 * 0.1784057 * -2.877929 *        13 *        58 *
#*        6 *        1 *           *   38.5625 * -1.020019 * 0.2039794 *        13 *        58 *
#*        7 *        0 *           * 38.203125 * -2.397460 * 1.9970703 *        13 *       314 *
#*        7 *        1 *           * 9.2207031 * -0.739746 * -1.232421 *        13 *       272 *
#*        7 *        2 *           * 38.203125 * -2.397460 * 1.9970703 *        15 *         2 *
#*        8 *        0 *           *           *           *           *           *           *
#*        9 *        0 *           *           *           *           *           *           *
#*       10 *        0 *           *  47.71875 * 0.7868652 * -0.403320 *        13 *        58 *
#*       10 *        1 *           * 14.832031 * 1.1762695 * 2.9609375 *        13 *        16 *
#*       10 *        2 *           *  47.71875 * 0.7868652 * -0.403320 *        15 *         2 *
#*       10 *        3 *           * 41.539062 * 1.2119140 * 2.9892578 *        15 *         2 *


#:HLT_Ele32_WPTight_Gsf_L1DoubleEG

##root [8] fitter_tree->Print("pair*")
##******************************************************************************
##*Tree    :fitter_tree: fitter_tree                                            *
##*Entries : 14863305 : Total =      5784943968 bytes  File  Size = 3700011734 *
##*        :          : Tree compression factor =   1.56                       *
##******************************************************************************
##*Br    0 :pair_abseta : pair_abseta/F                                        *
##*Entries : 14863305 : Total  Size=   59632049 bytes  File Size  =   45757237 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=   1.30     *
##*............................................................................*
##*Br    1 :pair_eta  : pair_eta/F                                             *
##*Entries : 14863305 : Total  Size=   59626937 bytes  File Size  =   47042732 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=   1.27     *
##*............................................................................*
##*Br    2 :pair_mass : pair_mass/F                                            *
##*Entries : 14863305 : Total  Size=   59628641 bytes  File Size  =   41623868 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=   1.43     *
##*............................................................................*
##*Br    3 :pair_pt   : pair_pt/F                                              *
##*Entries : 14863305 : Total  Size=   59625233 bytes  File Size  =   46363711 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=   1.29     *
##*............................................................................*
##*Br    4 :pair_mass60to120 : pair_mass60to120/I                              *
##*Entries : 14863305 : Total  Size=   59640569 bytes  File Size  =    1171178 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=  50.89     *
##*............................................................................*

##******************************************************************************
##*Tree    :fitter_tree: fitter_tree                                            *
##*Entries : 14863305 : Total =      5784943968 bytes  File  Size = 3700011734 *
##*        :          : Tree compression factor =   1.56                       *
##******************************************************************************
##*Br    0 :passingIDMVA : passingIDMVA/I                                      *
##*Entries : 14863305 : Total  Size=   59633753 bytes  File Size  =    1870571 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=  31.86     *
##*............................................................................*
##*Br    1 :passingPresel : passingPresel/I                                    *
##*Entries : 14863305 : Total  Size=   59635457 bytes  File Size  =    4070852 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=  14.64     *
##*............................................................................*


##******************************************************************************
##*Tree    :fitter_tree: fitter_tree                                            *
##*Entries : 14863305 : Total =      5784943968 bytes  File  Size = 3700011734 *
##*        :          : Tree compression factor =   1.56                       *
##******************************************************************************
##*Br    0 :passingIDMVA : passingIDMVA/I                                      *
##*Entries : 14863305 : Total  Size=   59633753 bytes  File Size  =    1870571 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=  31.86     *
##*............................................................................*
##*Br    1 :passingPresel : passingPresel/I                                    *
##*Entries : 14863305 : Total  Size=   59635457 bytes  File Size  =    4070852 *
##*Baskets :     1700 : Basket Size=     512000 bytes  Compression=  14.64     *
##*............................................................................*

##for EB
#if isEB:
    #biningDef = [
        #{ 'var' : 'probe_sc_abseta' , 'type': 'float', 'bins': [ 0.0, 1.4442] },
        #{ 'var' : 'probe_Pho_r9' , 'type': 'float', 'bins': [0.5,0.85,999.0] },
        #]
#else:
    ##for EE
    #biningDef = [
        #{ 'var' : 'probe_sc_abseta' , 'type': 'float', 'bins': [ 1.566,2.5] },
        #{ 'var' : 'probe_Pho_r9' , 'type': 'float', 'bins': [0.9,999.0] },     # for legacy 2016 high R9 category only in EE
        #]

