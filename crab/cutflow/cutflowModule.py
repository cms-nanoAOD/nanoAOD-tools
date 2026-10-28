#!/usr/bin/env python
import os, sys
import ROOT
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
sys.path.insert(0, '../minitree/')
from Mc_prob_cal_forBweght import *
from scaleFactor import * 

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import gzip
#import itertools as IT
from correctionlib import _core
#import itertools

class cutflow(Module):
    def __init__(self,Total_Njets,BTag_Njets,Isolation,lepflavour,isMC,dataYear,MCsample=None):
        self.writeHistFile=True
        self.Total_Njets = Total_Njets
        self.BTag_Njets = BTag_Njets
        self.Isolation = Isolation
        self.lepflavour = lepflavour
        self.isMC = isMC
        self.dataYear = dataYear
        self.MCsample = MCsample 
        if(self.isMC):
             PATH = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/" % os.environ['CMSSW_BASE']
             JetPUJetID_effi_file={
             'UL2016preVFP'  :  PATH+"jmar_PUID_UL2016preVFP.json.gz",
             'UL2016postVFP' :  PATH+"jmar_PUID_UL2016postVFP.json.gz",
             'UL2017'        :  PATH+"jmar_PUID_UL2017.json.gz",
             'UL2018'        :  PATH+"jmar_PUID_UL2018.json.gz"}

             if JetPUJetID_effi_file[self.dataYear].endswith(".json.gz"):
                with gzip.open(JetPUJetID_effi_file[self.dataYear],'rt') as file:
                        data = file.read().strip()
                        self.evaluator = _core.CorrectionSet.from_string(data)
             else:
                        self.evaluator = _core.CorrectionSet.from_file(JetPUJetID_effi_file[self.dataYear])

        self.TotalLumi = {  '2016' : 35882.5,
                            '2017' : 41529.5,
                            '2018' : None,
                            'UL2016preVFP' :  19521,
                            'UL2016postVFP' : 16812,
                            'UL2017' : 41529,
                            'UL2018' : 59222}

        if(self.isMC == True):
            from Xsec_Nevent import MCsample_Nevent_Xsec
            x_sec = float(MCsample_Nevent_Xsec[self.dataYear][self.MCsample][1])
            NEvents = float(MCsample_Nevent_Xsec[self.dataYear][self.MCsample][0])
            self.Xsec_wgt = (x_sec*self.TotalLumi[self.dataYear])/NEvents
        self.Tight_b_tag_crite={
                        '2016' : 0.7527, 
                        '2017' : 0.8001,
                        '2018' : None,
                        'UL2016preVFP' : 0.6502, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                        'UL2016postVFP' : 0.6377, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
                        'UL2017' : 0.7476, # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
                        'UL2018' : 0.7100} # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation106XUL18
        if(self.lepflavour=="mu"):
            self.trigger_selection={
                '2016' : ['HLT_IsoMu24','HLT_IsoTkMu24'],
                '2017' : ['HLT_IsoMu27'],
                '2018' : None,
                'UL2016preVFP' : ['HLT_IsoMu24','HLT_IsoTkMu24'],
                'UL2016postVFP' : ['HLT_IsoMu24','HLT_IsoTkMu24'],
                'UL2017' : ['HLT_IsoMu27'],
                'UL2018' : ['HLT_IsoMu24']}
            self.pt_Thes={
                '2016' : 26,
                '2017' : 30,
                '2018' : None,
                'UL2016preVFP' : 26,
                'UL2016postVFP' : 26,
                'UL2017' : 30,
                'UL2018' : 26}
        if(self.lepflavour=="el"):
            self.trigger_selection={
                '2016' : ['HLT_Ele32_eta2p1_WPTight_Gsf'],
                '2017' : ['HLT_Ele35_WPTight_Gsf','HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned'],
                '2018' : None,
                'UL2016preVFP' : ['HLT_Ele32_eta2p1_WPTight_Gsf'],
                'UL2016postVFP' : ['HLT_Ele32_eta2p1_WPTight_Gsf'],
                'UL2017' : ['HLT_Ele32_WPTight_Gsf_L1DoubleEG'],#'TrigObj_filterBits','TrigObj_id' ] imbded in the code  
                'UL2018' : ['HLT_Ele32_WPTight_Gsf']}
            self.pt_Thes={
                '2016' : 35,
                '2017' : 37,
                '2018' : None,
                'UL2016preVFP' : 35,
                'UL2016postVFP' : 35,
                'UL2017' : 35,
                'UL2018' : 35}


    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)

        self.Nocut_npvs=ROOT.TH1F('Nocut_npvs','Nocut_npvs', 100, 0, 1000)
        self.trig_sel_npvs=ROOT.TH1F('trig_sel_npvs','trig_sel_npvs', 100, 0, 1000)
        self.tight_lep_sel_npvs=ROOT.TH1F('tight_lep_sel_npvs','tight_lep_sel_npvs', 100, 0, 1000)
        self.losse_lep_veto_npvs=ROOT.TH1F('losse_lep_veto_npvs','losse_lep_veto_npvs', 100, 0, 1000)
        self.sec_lep_veto_npvs=ROOT.TH1F('sec_lep_veto_npvs','sec_lep_veto_npvs',100,0,1000)
        #self.ttbar_barrel_4jet_npvs=ROOT.TH1F('ttbar_barrel_4jet_npvs','ttbar_barrel_4jet_npvs',100,0,1000)
        self.jet_sel_npvs=ROOT.TH1F('jet_sel_npvs','jet_sel_npvs',100,0,1000)
        self.b_tag_jet_sel_npvs=ROOT.TH1F('b_tag_jet_sel_npvs','b_tag_jet_sel_npvs',100,0,1000)
        self.MET_filter_npvs=ROOT.TH1F('MET_filter_npvs','MET_filter_npvs',100,0,1000)
        self.wightSum_WO_bWeight=ROOT.TH1F('wightSum_WO_bWeight','wightSum_WO_bWeight',25,0,25)
        self.wightSum_W_bWeight=ROOT.TH1F('wightSum_W_bWeight','wightSum_W_bWeight',25,0,25)
        self.N_jets=ROOT.TH1F('N_jets','N_jets',25,0,25)
        self.N_b_jets=ROOT.TH1F('N_b_jets','N_b_jets',25,0,25)
        self.addObject(self.Nocut_npvs)
        self.addObject(self.trig_sel_npvs)
        self.addObject(self.tight_lep_sel_npvs)
        self.addObject(self.losse_lep_veto_npvs)
        self.addObject(self.sec_lep_veto_npvs)
        #self.addObject(self.ttbar_barrel_4jet_npvs)
        self.addObject(self.jet_sel_npvs)
        self.addObject(self.b_tag_jet_sel_npvs)
        self.addObject(self.MET_filter_npvs)
        self.addObject(self.wightSum_WO_bWeight)
        self.addObject(self.wightSum_W_bWeight)
        self.addObject(self.N_jets)
        self.addObject(self.N_b_jets)


    def analyze(self, event):
        try:
            LHEWeightSign = getattr(event,'LHEWeight_originalXWGTUP')/abs(getattr(event,'LHEWeight_originalXWGTUP'))
        except:
                LHEWeightSign = 1  
        if(self.isMC == True):
            PuWeight = getattr(event,'puWeight') 
        PreFireWeight = getattr(event,'L1PreFiringWeight_Nom')
        PV_npvs = getattr(event, "PV_npvs")
        if(self.isMC == True):self.Nocut_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
        else:self.Nocut_npvs.Fill(PV_npvs*PreFireWeight)
        #print "Xsec_wgt = ", self.Xsec_wgt
        #print "PuWeight = ", PuWeight
        #print "PreFireWeight = ",PreFireWeight
##################################
#trigger selection	--0--
###################################
        trigger=0
        TrigObjs = Collection(event, "TrigObj")
        if(self.lepflavour=="mu"):
            #print(self.trigger_selection[self.dataYear])
            for value in self.trigger_selection[self.dataYear]: trigger=trigger+getattr(event,value)
            if(trigger != 0):
                if(self.isMC == True):self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
                else:self.trig_sel_npvs.Fill(PV_npvs*PreFireWeight)
                del trigger
            else:
                return True
        elif(self.lepflavour=="el"):
            for value in self.trigger_selection[self.dataYear]: trigger=trigger+getattr(event,value)
            if(self.dataYear=="UL2017"): #spacial emulated trigger
                emulated_trigger = 0
                if(trigger != 0):
                    for TrigObj in TrigObjs:
                         #print(TrigObj.filterBits,TrigObj.id)
                         if((TrigObj.filterBits & 1024)!=0 and (TrigObj.id==11)):
                             emulated_trigger=emulated_trigger+1
                #print("emulated_trigger",emulated_trigger)
                trigger = trigger*emulated_trigger
                del emulated_trigger
                #del TrigObj_filterBits, TrigObj_ids,list_TrigObj_filterBits, list_TrigObj_ids, updated_trigger
            if(trigger != 0):
                #print(TrigObj_filterBits,TrigObj_ids)
                if(self.isMC == True):
                    self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
                else:
                    self.trig_sel_npvs.Fill(PV_npvs)
            else:
                return True
        #print("---------------------------------trigger selection      --0------------")
        ##################################
        #one tight lepon selection-1-      
        ###################################
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        if(self.lepflavour=="mu"):
            muons_id=[]
            one_T_mu_ID = None
            #print len(muons)
            for lep in muons:
                #print self.Isolation, " ", lep.pt, " ", lep.eta , " ", lep.pfRelIso04_all ," " , lep.tightIdi
                #print 'loose ID = ',lep.looseId, ' pt = ',lep.pt , ' eta = ', lep.eta, 'iso = ',lep.pfRelIso04_all #' phi =', lep.phi, ' mass = ',lep.mass
                if((self.Isolation==1) and lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.06 and lep.tightId==1):
                        muons_id.append(lep)
                elif((self.Isolation==0) and lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all>0.2 and lep.tightId==1): 
                        muons_id.append(lep)
                else: 
                        continue
            if(len(muons_id)==1):
                muSF = 0
                if(self.isMC == True):
                        for muon in muons_id:
                            muSF=create_muSF(self.dataYear,muon.pt,muon.eta,muon.pfRelIso04_all,self.TotalLumi[self.dataYear],"noSyst")
                            self.tight_lep_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
                        #print "muSF : ",muSF," weight : " , (self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF, " Integral : ", self.tight_lep_sel_npvs.Integral(), " LHEweight : ",LHEWeightSign
                else:self.tight_lep_sel_npvs.Fill(PV_npvs)
            else:
                    #print "ione tight muon selection-1- "
                    return True
        elif(self.lepflavour=="el"):
            electron_id=[]
            for lep in electrons:
                if((self.Isolation==True) and not(lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased==4 and not(abs(lep.EtaSC)<1.5660 and abs(lep.EtaSC)>1.4442) )): continue 
                elif((self.Isolation==False) and not(lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased!=4 and lep.cutBased>=1 and not(abs(lep.EtaSC)<1.5660 and abs(lep.EtaSC)>1.4442) )): continue
                if(abs(lep.EtaSC)<=1.479 and not(abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05)): continue
                if(abs(lep.EtaSC)> 1.479 and not(abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)): continue
                electron_id.append(lep)
            if (len(electron_id)==1):
                elSF=0
                if(self.isMC == True):
                    for electron in electron_id:
                        if(self.Isolation==True):elSF = create_elSF(self.dataYear,electron.pt,electron.EtaSC,"Tight","noSyst")
                        elif(self.Isolation==False):elSF = create_elSF(self.dataYear,electron.pt,electron.EtaSC,"Veto","noSyst")
                        self.tight_lep_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
                #print "elSF : ",elSF, "Integral : ",self.tight_lep_sel_npvs.Integral()," weight : " , (self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF," LHE : " , LHEWeightSign
                if(self.isMC == False):
                    self.tight_lep_sel_npvs.Fill(PV_npvs)
            else:
                #print "one tight muon selection-1- "
                return True
            #print '---------------------------------one tight lep selection-1----------------'


        ###################################
        #losse lepton veto --2--
        ###################################


        if(self.lepflavour=="mu"):
            muons_losse_size=0
            for lep in muons:
                #print 'pt = %s eta = %s pfRelIso04_all = %s '%(lep.pt,lep.eta,lep.pfRelIso04_all)
                if(lep==muons_id[0]): continue
                if(lep.looseId==1 and lep.pt>10 and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.2): 
                    #print 'pt = %s eta = %s pfRelIso04_all = %s '%(lep.pt,lep.eta,lep.pfRelIso04_all)
                        muons_losse_size += 1
                if(muons_losse_size>0): break
            if(muons_losse_size==0):
                if(self.isMC == True):self.losse_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
                if(self.isMC == False):self.losse_lep_veto_npvs.Fill(PV_npvs)
            else:
                #print "losse muon veto --2--"
                return True
                #print 'muons_losse_size = ' ,muons_losse_size
        if(self.lepflavour=="el"):
            electron_vid_size=0
            for lep in electrons:
                if(lep==electron_id[0]): continue	
                if(abs(lep.EtaSC)<=1.479 and not(abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05)): continue
                if(abs(lep.EtaSC)> 1.479 and not(abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)): continue
                if(lep.cutBased>=1 and lep.pt>15 and abs(lep.eta)<2.5): electron_vid_size+=1
                if(electron_vid_size>0):
                    break
            if(electron_vid_size==0):
                if(self.isMC == True):self.losse_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
                if(self.isMC == False):self.losse_lep_veto_npvs.Fill(PV_npvs)
            else:
                return True
        #print '---------------------------------------------losse lep veto --2---------------


        ################################## 
        #second lepton veto  --3--
        ##################################


        if(self.lepflavour=="mu"):
            electron_vid_size=0
            for lep in electrons:
                if(lep.cutBased ==1 and lep.pt>15 and abs(lep.eta)<2.5  and (abs(lep.eta) < 1.4442 or abs(lep.eta) > 1.566)):
                    electron_vid_size += 1
                if(electron_vid_size>0): break
            if(electron_vid_size==0):
                if(self.isMC == True):self.sec_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
                if(self.isMC == False):self.sec_lep_veto_npvs.Fill(PV_npvs)
            else:
                    #print "ione tight muon selection-1- "
                return True

        if(self.lepflavour=="el"):
            muons_losse_size=0
            for muon in muons:
                if(muon.looseId==1 and muon.pt>10 and abs(muon.eta)<2.4 and muon.pfRelIso04_all<0.2): 
                    muons_losse_size+=1
                if(muons_losse_size>0): 
                    break
            if(muons_losse_size==0):
                if(self.isMC == True):self.sec_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
                if(self.isMC == False):self.sec_lep_veto_npvs.Fill(PV_npvs)
            else:
                    #print "second lepton veto  --3--"
                    return True
        #print '--------------------------------------------------another lepton veto  --3------------'


        ##################################
        #jet selection  --4--
        ##################################  


        
        jets = Collection(event, "Jet")
        muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
        electron4v = ROOT.TLorentzVector(0.,0.,0.,0.)
        if(self.lepflavour=="mu"):
            for muon in muons_id:
                    muon4v=muon.p4()
        if(self.lepflavour=="el"):
            for electron in electron_id:
                electron4v = electron.p4()

        """#######################
        #ttbar check
        #######################
        jet_id_ttbar = []
        jetid_for_N_jets_ttbar = []

        for jet in jets:
            #print jet.jetId
            islossepF_ttbar=False
            if(jet.pt>40 and abs(jet.eta)<2.4 and jet.jetId!=0 and jet.puId!=0):
                islossepF_ttbar = True
                jetid_for_N_jets_ttbar.append(jet)
                #print "jet.pt = ",jet.pt," jet.eta = ",abs(jet.eta), " jet.jetId = ",jet.jetId, "lossepF = ", lossepF
            else: continue
            njet4v_ttbar = ROOT.TLorentzVector(0.,0.,0.,0.)    
            njet4v_ttbar = jet.p4()
            if(self.lepflavour=="mu" and islossepF_ttbar==True and muon4v.DeltaR(njet4v_ttbar)>0.4):
                jet_id_ttbar.append(jet)#and muon4v.DeltaR(njet4v)>0.4):jet_id.append(jet)
                #print "deltaR =",muon4v.DeltaR(njet4v)," jetdeltaRiso = ",jet.dR_Ljet_Isomu," jetdeltaRantiiso = ",jet.dR_Ljet_AntiIsomu
                #print "Jet Pt =%s ; Jet eta =%s ; jet ID =%s ;DeltaR =%s" % (jet.pt,jet.eta,jet.jetId,muon4v.DeltaR(njet4v)) 
            elif(self.lepflavour=="el" and islossepF_ttbar==True and electron4v.DeltaR(njet4v_ttbar)>0.4): 
                jet_id_ttbar.append(jet)
            else: continue

        JetPUJetID_SF_ttbar = 1.0
        if(len(jet_id_ttbar)==4):
            if(self.isMC==True):
                for jet in jet_id_ttbar:
                    if(jet.pt<50):
                        JetPUJetID_SF_ttbar = JetPUJetID_SF_ttbar*self.evaluator["PUJetID_eff"].evaluate(abs(jet.eta), jet.pt, "nom","L")

            if(self.lepflavour=="mu" and self.isMC == True): self.ttbar_barrel_4jet_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF_ttbar)
            elif(self.lepflavour=="el" and self.isMC == True): self.ttbar_barrel_4jet_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF_ttbar)
            elif(self.lepflavour=="mu" and self.isMC == False): self.ttbar_barrel_4jet_npvs.Fill(PV_npvs)
            elif(self.lepflavour=="el" and self.isMC == False): self.ttbar_barrel_4jet_npvs.Fill(PV_npvs)"""

        ########################
        ## Analysis requirement
        ########################

        jet_id = []
        jetid_for_N_jets = []
        
        
        N_b_jets=0
        for jet in jets:
            #print jet.jetId
            islossepF=False
            puId_loose_bit = 1 if self.dataYear.startswith('UL2016') else 4
            if(jet.pt>40 and abs(jet.eta)<4.7 and jet.jetId!=0 and jet.jetVetoed==0 and (jet.pt>=50 or (jet.puId & puId_loose_bit)!=0)):
                islossepF = True
                jetid_for_N_jets.append(jet)
                #print "jet.pt = ",jet.pt," jet.eta = ",abs(jet.eta), " jet.jetId = ",jet.jetId, "lossepF = ", lossepF
            else: continue
            njet4v = ROOT.TLorentzVector(0.,0.,0.,0.)    
            njet4v = jet.p4()
            if(self.lepflavour=="mu" and islossepF==True and muon4v.DeltaR(njet4v)>0.4):
                jet_id.append(jet)#and muon4v.DeltaR(njet4v)>0.4):jet_id.append(jet)
                #print "deltaR =",muon4v.DeltaR(njet4v)," jetdeltaRiso = ",jet.dR_Ljet_Isomu," jetdeltaRantiiso = ",jet.dR_Ljet_AntiIsomu
                #print "Jet Pt =%s ; Jet eta =%s ; jet ID =%s ;DeltaR =%s" % (jet.pt,jet.eta,jet.jetId,muon4v.DeltaR(njet4v)) 
            elif(self.lepflavour=="el" and islossepF==True and electron4v.DeltaR(njet4v)>0.4): jet_id.append(jet)
            else: continue
        #  print "jet_id = ",jet_id
                
        if(self.isMC == True): bweight_for_N_b_jets = Get_B_tagging_sys_sf("Central",jetid_for_N_jets)
        JetPUJetID_SF = 1.0
        if(self.isMC==True):
            for jet in jetid_for_N_jets:
                if(jet.pt<50):
                    JetPUJetID_SF = JetPUJetID_SF*self.evaluator["PUJetID_eff"].evaluate(abs(jet.eta), jet.pt, "nom","L")
        if(self.lepflavour=="mu" and self.isMC == True):
            self.N_jets.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF)
            self.wightSum_WO_bWeight.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF)
            self.wightSum_W_bWeight.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF*bweight_for_N_b_jets)
        if(self.lepflavour=="el" and self.isMC == True):
            self.N_jets.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF)
            self.wightSum_WO_bWeight.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF)
            self.wightSum_W_bWeight.Fill(len(jetid_for_N_jets),(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF*bweight_for_N_b_jets)
        if(self.lepflavour=="mu" and self.isMC == False):
            self.N_jets.Fill(len(jetid_for_N_jets),PreFireWeight)
        if(self.lepflavour=="el" and self.isMC == False):
            self.N_jets.Fill(len(jetid_for_N_jets),PreFireWeight)

        for jet in jetid_for_N_jets:
            if(abs(jet.eta)<2.4 and jet.btagDeepFlavB>self.Tight_b_tag_crite[self.dataYear]):
                N_b_jets=N_b_jets+1
            
        del jetid_for_N_jets
        if(self.lepflavour=="mu" and self.isMC == True):self.N_b_jets.Fill(N_b_jets,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF*bweight_for_N_b_jets)
        if(self.lepflavour=="el" and self.isMC == True):self.N_b_jets.Fill(N_b_jets,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF*bweight_for_N_b_jets)
        if(self.lepflavour=="mu" and self.isMC == False):self.N_b_jets.Fill(N_b_jets,PreFireWeight)
        if(self.lepflavour=="el" and self.isMC == False):self.N_b_jets.Fill(N_b_jets,PreFireWeight)
        if(self.isMC == True): del bweight_for_N_b_jets
        del N_b_jets
        del JetPUJetID_SF

        JetPUJetID_SF = 1.0
        if(len(jet_id)==self.Total_Njets):
                
            if(self.isMC==True):
                for jet in jet_id:
                    if(jet.pt<50):
                        JetPUJetID_SF = JetPUJetID_SF*self.evaluator["PUJetID_eff"].evaluate(abs(jet.eta), jet.pt, "nom","L")

            if(self.lepflavour=="mu" and self.isMC == True): self.jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF)
            elif(self.lepflavour=="el" and self.isMC == True): self.jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF)
            elif(self.lepflavour=="mu" and self.isMC == False): self.jet_sel_npvs.Fill(PV_npvs)
            elif(self.lepflavour=="el" and self.isMC == False): self.jet_sel_npvs.Fill(PV_npvs)
        
        else:
            #print "jet selection  --4--"
            return True
        #print '---------------------------------------------------------------jet selection  --4--
        
        ##################################
        # MET filter  --5--
        ##################################
        MET_filetr_flag = 1
        Met_filter_UL16 = ['Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter' , 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter' , 'Flag_BadPFMuonDzFilter', 'Flag_eeBadScFilter']
        Met_filter_UL17_UL18 = ['Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter' , 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter', 'Flag_BadPFMuonDzFilter', 'Flag_eeBadScFilter', 'Flag_ecalBadCalibFilter']
        if(self.dataYear in ['UL2016preVFP', 'UL2016postVFP']):
            for filter in Met_filter_UL16:
                MET_filetr_flag = MET_filetr_flag*getattr(event,filter)
        elif(self.dataYear in ['UL2017', 'UL2018']):
            for filter in Met_filter_UL17_UL18:
                MET_filetr_flag = MET_filetr_flag*getattr(event,filter) 
        if(MET_filetr_flag==1 and self.isMC == False):
            if(self.lepflavour=="mu"): self.MET_filter_npvs.Fill(PV_npvs)
            if(self.lepflavour=="el"): self.MET_filter_npvs.Fill(PV_npvs)
        elif(MET_filetr_flag==1 and self.isMC == True):
            if(self.lepflavour=="mu"): self.MET_filter_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF)
            if(self.lepflavour=="el"): self.MET_filter_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF)
        else:
            return True
        
        ##################################
        #b tag jet  --6--
        ##################################

        btagjet_id = []
        for jet in jet_id:
            if(abs(jet.eta)<2.4 and jet.btagDeepFlavB>self.Tight_b_tag_crite[self.dataYear]): 
                btagjet_id.append(jet)
        if(len(btagjet_id)==self.BTag_Njets):
            if(self.isMC == True):
                #print(getattr(event,'event'))
                bweight = Get_B_tagging_sys_sf("Central",jet_id)	
                if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF*bweight)
                if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF*bweight)
            #print "bweight = ",bweight
            if(self.isMC == False):
                if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs)
                if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs)
        else:
            #print "b tag jet  --5--"
            return True
        #print '---------------------------------------------------------------------------b tag jet  --5--'


        return True

cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP =   lambda MCsample : cutflow(2,1,True,"mu",True,'UL2016preVFP',MCsample)
cutflowModuleConstr_2J1T1_mu_data_UL2016preVFP =   lambda : cutflow(2,1,True,"mu",False,'UL2016preVFP')
cutflowModuleConstr_2J1T1_el_mc_UL2016preVFP =   lambda MCsample : cutflow(2,1,True,"el",True,'UL2016preVFP',MCsample)
cutflowModuleConstr_2J1T1_el_data_UL2016preVFP =   lambda : cutflow(2,1,True,"el",False,'UL2016preVFP')

cutflowModuleConstr_2J1T1_mu_mc_UL2016postVFP =   lambda MCsample : cutflow(2,1,True,"mu",True,'UL2016postVFP',MCsample)
cutflowModuleConstr_2J1T1_mu_data_UL2016postVFP =   lambda : cutflow(2,1,True,"mu",False,'UL2016postVFP')
cutflowModuleConstr_2J1T1_el_mc_UL2016postVFP =   lambda MCsample : cutflow(2,1,True,"el",True,'UL2016postVFP',MCsample)
cutflowModuleConstr_2J1T1_el_data_UL2016postVFP =   lambda : cutflow(2,1,True,"el",False,'UL2016postVFP')


cutflowModuleConstr_2J1T0_mu_mc_UL2016preVFP =   lambda MCsample : cutflow(2,1,False,"mu",True,'UL2016preVFP',MCsample)
cutflowModuleConstr_2J1T0_mu_data_UL2016preVFP =   lambda : cutflow(2,1,False,"mu",False,'UL2016preVFP')
cutflowModuleConstr_2J1T0_el_mc_UL2016preVFP =   lambda MCsample : cutflow(2,1,False,"el",True,'UL2016preVFP',MCsample)
cutflowModuleConstr_2J1T0_el_data_UL2016preVFP =   lambda : cutflow(2,1,False,"el",False,'UL2016preVFP')

cutflowModuleConstr_2J1T0_mu_mc_UL2016postVFP =   lambda MCsample : cutflow(2,1,False,"mu",True,'UL2016postVFP',MCsample)
cutflowModuleConstr_2J1T0_mu_data_UL2016postVFP =   lambda : cutflow(2,1,False,"mu",False,'UL2016postVFP')
cutflowModuleConstr_2J1T0_el_mc_UL2016postVFP =   lambda MCsample : cutflow(2,1,False,"el",True,'UL2016postVFP',MCsample)
cutflowModuleConstr_2J1T0_el_data_UL2016postVFP =   lambda : cutflow(2,1,False,"el",False,'UL2016postVFP')



cutflowModuleConstr_2J1T1_mu_mc_UL2017 =   lambda MCsample : cutflow(2,1,True,"mu",True,'UL2017',MCsample)
cutflowModuleConstr_2J1T1_mu_data_UL2017 =   lambda : cutflow(2,1,True,"mu",False,'UL2017')
cutflowModuleConstr_2J1T1_el_mc_UL2017 =   lambda MCsample : cutflow(2,1,True,"el",True,'UL2017',MCsample)
cutflowModuleConstr_2J1T1_el_data_UL2017 =   lambda : cutflow(2,1,True,"el",False,'UL2017')

cutflowModuleConstr_2J1T0_mu_mc_UL2017 =   lambda MCsample : cutflow(2,1,False,"mu",True,'UL2017',MCsample)
cutflowModuleConstr_2J1T0_mu_data_UL2017 =   lambda : cutflow(2,1,False,"mu",False,'UL2017')
cutflowModuleConstr_2J1T0_el_mc_UL2017 =   lambda MCsample : cutflow(2,1,False,"el",True,'UL2017',MCsample)
cutflowModuleConstr_2J1T0_el_data_UL2017 =   lambda : cutflow(2,1,False,"el",False,'UL2017')

cutflowModuleConstr_2J1T1_mu_mc_UL2018 =   lambda MCsample : cutflow(2,1,True,"mu",True,'UL2018',MCsample)
cutflowModuleConstr_2J1T1_mu_data_UL2018 =   lambda : cutflow(2,1,True,"mu",False,'UL2018')
cutflowModuleConstr_2J1T1_el_mc_UL2018 =   lambda MCsample : cutflow(2,1,True,"el",True,'UL2018',MCsample)
cutflowModuleConstr_2J1T1_el_data_UL2018 =   lambda : cutflow(2,1,True,"el",False,'UL2018')

cutflowModuleConstr_2J1T0_mu_mc_UL2018 =   lambda MCsample : cutflow(2,1,False,"mu",True,'UL2018',MCsample)
cutflowModuleConstr_2J1T0_mu_data_UL2018 =   lambda : cutflow(2,1,False,"mu",False,'UL2018')
cutflowModuleConstr_2J1T0_el_mc_UL2018 =   lambda MCsample : cutflow(2,1,False,"el",True,'UL2018',MCsample)
cutflowModuleConstr_2J1T0_el_data_UL2018 =   lambda : cutflow(2,1,False,"el",False,'UL2018')
