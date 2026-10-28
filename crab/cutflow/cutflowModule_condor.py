import ROOT
import numpy as np
import sys
#import argparse as arg
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from Mc_prob_cal_forBweght import *
from scaleFactor import *
import gzip
from correctionlib import _core

#parser = arg.ArgumentParser(description='discription for inputs')
#parser.add_argument('-f', '--inputFile', dest='InFile', default=['MVA_results/Inputfile_after_traing.root'], type=str, nargs=1, help="Input File after the training ")
#args = parser.parse_args()

#InFile = args.InFile[0]

#if(InFile==None):
#   print "provide input file cutflow.py -f inputfile.root"
#   sys.exit()


class cutflow:
    def __init__(self,Total_Njets,BTag_Njets,Isolation,lepflavour,isMC,dataYear):
		self.writeHistFile=True
        self.Total_Njets = Total_Njets
        self.BTag_Njets = BTag_Njets
        self.Isolation = Isolation
        self.lepflavour = lepflavour
        self.isMC = isMC
        self.dataYear = dataYear
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

        self.TotalLumi = {
            '2016' : 35882.5,
            '2017' : 41529.5,
            '2018' : None,
            'UL2016preVFP' :  19521,
            'UL2016postVFP' : 16812,
            'UL2017' : 41529,
            'UL2018' : 59222}
        if(self.isMC == True):
                x_sec = 87.33
                #Lumi = lumi[self.dataYear]
                NEvents = 37202073
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
                'UL2017' : ['HLT_Ele35_WPTight_Gsf','HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned'],
                'UL2018' : ['HLT_Ele32_WPTight_Gsf']}
            self.pt_Thes={
                '2016' : 35,
                '2017' : 37,
                '2018' : None,
                'UL2016preVFP' : 35,
                'UL2016postVFP' : 35,
                'UL2017' : 37,
                'UL2018' : 35}
        self.Nocut_npvs=ROOT.TH1F('Nocut_npvs','Nocut_npvs', 100, 0, 1000)
       	self.trig_sel_npvs=ROOT.TH1F('trig_sel_npvs','trig_sel_npvs', 100, 0, 1000)
        self.tight_lep_sel_npvs=ROOT.TH1F('tight_lep_sel_npvs','tight_lep_sel_npvs', 100, 0, 1000)
        self.losse_lep_veto_npvs=ROOT.TH1F('losse_lep_veto_npvs','losse_lep_veto_npvs', 100, 0, 1000)
        self.sec_lep_veto_npvs=ROOT.TH1F('sec_lep_veto_npvs','sec_lep_veto_npvs',100,0,1000)
        self.jet_sel_npvs=ROOT.TH1F('jet_sel_npvs','jet_sel_npvs',100,0,1000)
        self.b_tag_jet_sel_npvs=ROOT.TH1F('b_tag_jet_sel_npvs','b_tag_jet_sel_npvs',100,0,1000)
        self.wightSum_WO_bWeight=ROOT.TH1F('wightSum_WO_bWeight','wightSum_WO_bWeight',25,0,25)
        self.wightSum_W_bWeight=ROOT.TH1F('wightSum_W_bWeight','wightSum_W_bWeight',25,0,25)
        self.N_jets=ROOT.TH1F('N_jets','N_jets',25,0,25)
        self.N_b_jets=ROOT.TH1F('N_b_jets','N_b_jets',25,0,25)
    def analyze(self, myTree):
	counter=0
	for event in myTree:
	    counter = counter+1
	    #if (counter<100000): continue
	    if(counter % 10000 == 0): 
		print counter
		#if(counter % 10000==0): break
	
	    try:
	 	LHEWeightSign = getattr(event,'LHEWeight_originalXWGTUP')/abs(getattr(event,'LHEWeight_originalXWGTUP'))
	    except:
             	LHEWeightSign = 1
	    if(self.isMC == True):
	 	PuWeight = getattr(event,'puWeight') 
	    PreFireWeight = getattr(event,'L1PreFiringWeight_Nom')
	    PV_npvs = getattr(event, "PV_npvs")
	    if(self.isMC == True):self.Nocut_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
	    else:self.Nocut_npvs.Fill(PV_npvs)  
	   
	    ##################################
	    #trigger selection	--0--
	    ###################################
	       
	    trigger=0;
 	    if(self.lepflavour=="mu"):
                for value in self.trigger_selection[self.dataYear]: 
	 	    trigger=trigger+getattr(event,value)   #trigger value will be o or 1. So sum = 1 if any given trigger is true
	        if(trigger != 0):
	    	     if(self.isMC == True):self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
	 	     else:self.trig_sel_npvs.Fill(PV_npvs)
	    	else:
	     	    continue
	    elif(self.lepflavour=="el"):
	    	for value in self.trigger_selection[self.dataYear]: trigger=trigger+getattr(event,value)
	    	if(trigger != 0):
	 	      if(self.isMC == True):self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
	 	      else:self.trig_sel_npvs.Fill(PV_npvs)
	    	else:
                      continue
	    #print "---------------------------------trigger selection      --0------------"
	    
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
	 	     continue
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
	 	       	Jetpt = getattr(event,'Jet_pt')
                    	jetpt = Jetpt[0]
	 	    	for electron in electron_id:
	 	    	    if(self.Isolation==True):elSF = create_elSF(self.dataYear,electron.pt,electron.EtaSC,jetpt,"Tight","noSyst")
	 	    	    elif(self.Isolation==False):elSF = create_elSF(self.dataYear,electron.pt,electron.EtaSC,jetpt,"Veto","noSyst")
	 	            self.tight_lep_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
	 	    #print "elSF : ",elSF, "Integral : ",self.tight_lep_sel_npvs.Integral()," weight : " , (self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF," LHE : " , LHEWeightSign
	 	    if(self.isMC == False):
	 	    	self.tight_lep_sel_npvs.Fill(PV_npvs)
  	    	else:
	 	    #print "one tight muon selection-1- "
                    continue
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
	 	    continue
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
	 	    continue
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
	 	     continue
	 	 
	    if(self.lepflavour=="el"):
	     	muons_losse_size=0
	     	for muon in muons:
	 	    if(muon.looseId==1 and muon.pt>10 and abs(muon.eta)<2.4 and muon.pfRelIso04_all<0.2): muons_losse_size+=1
	 	    if(muons_losse_size>0): break
	     	if(muons_losse_size==0):
             	    if(self.isMC == True):self.sec_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
	 	    if(self.isMC == False):self.sec_lep_veto_npvs.Fill(PV_npvs)
	   	else:
	 	     #print "second lepton veto  --3--"
             	     continue
	    #print '--------------------------------------------------another lepton veto  --3------------'
	 
	 
	    ##################################
	    #jet selection  --4--
	    ##################################  
         
	 
	    jet_id = []
	    jetid_for_N_jets = []
	    muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
	    electron4v = ROOT.TLorentzVector(0.,0.,0.,0.)
	    if(self.lepflavour=="mu"):
	    	for muon in muons_id:
            	    muon4v=muon.p4()
	    if(self.lepflavour=="el"):
	        for electron in electron_id:
	 	    electron4v = electron.p4()
            jets = Collection(event, "Jet")
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
                
            if(self.isMC == True): bweight_for_N_b_jets = Probability_2("Central",jetid_for_N_jets)
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
	    	continue
	    #print '---------------------------------------------------------------jet selection  --4--
	 
	   
	    ##################################
	    #b tag jet  --5--
	    ##################################

	    btagjet_id = []
	    for jet in jet_id:
	    	if(abs(jet.eta)<2.4 and jet.btagDeepFlavB>self.Tight_b_tag_crite[self.dataYear]): 
	 	    btagjet_id.append(jet)
	    if(len(btagjet_id)==self.BTag_Njets):
	    	if(self.isMC == True):
		    #print getattr(event,'event')
	 	    bweight = Probability_2("Central",jet_id)	
	 	    if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*JetPUJetID_SF*bweight)
	 	    if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*JetPUJetID_SF*bweight)
	 	    #print "bweight = ",bweight
	    	if(self.isMC == False):
	 	    if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs)
	 	    if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs)
            else:
	        #print "b tag jet  --5--"
	        continue				
	    #print '---------------------------------------------------------------------------b tag jet  --5--'




	outfile = ROOT.TFile( 'Cutflow_hist.root', 'RECREATE' )
	hist_dir = outfile.mkdir("histograms")
    	hist_dir.cd()
	self.Nocut_npvs.Write()
	self.trig_sel_npvs.Write()
	self.tight_lep_sel_npvs.Write()
	self.losse_lep_veto_npvs.Write()
	self.sec_lep_veto_npvs.Write()
	self.jet_sel_npvs.Write()
	self.b_tag_jet_sel_npvs.Write()
        self.N_jets.Write()
        self.N_b_jets.Write()
        self.wightSum_WO_bWeight.Write()
        self.wightSum_W_bWeight.Write()
	outfile.Close()	

        print()
        self.b_tag_jet_sel_npvs.Print()
        self.Nocut_npvs.Print()
        self.trig_sel_npvs.Print()
        self.tight_lep_sel_npvs.Print()
        self.losse_lep_veto_npvs.Print()
        self.sec_lep_veto_npvs.Print()
        self.jet_sel_npvs.Print()
        self.N_jets.Print()
        self.N_b_jets.Print()
        self.wightSum_WO_bWeight.Print()
        self.wightSum_W_bWeight.Print()



cutflowModuleConstr_2J1T1_mu_mc_2016 =   lambda : cutflow(2,1,True,"mu",True,'2016')
cutflowModuleConstr_2J1T1_mu_data_2016 =   lambda : cutflow(2,1,True,"mu",False,'2016')
cutflowModuleConstr_2J1T1_el_mc_2016 =   lambda : cutflow(2,1,True,"el",True,'2016')
cutflowModuleConstr_2J1T1_el_data_2016 =   lambda : cutflow(2,1,True,"el",False,'2016')

cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP =   lambda : cutflow(2,1,True,"mu",True,'UL2016preVFP')
cutflowModuleConstr_2J1T1_mu_data_UL2016preVFP =   lambda : cutflow(2,1,True,"mu",False,'UL2016preVFP')
cutflowModuleConstr_2J1T1_el_mc_UL2016preVFP =   lambda : cutflow(2,1,True,"el",True,'UL2016preVFP')
cutflowModuleConstr_2J1T1_el_data_UL2016preVFP =   lambda : cutflow(2,1,True,"el",False,'UL2016preVFP')

cutflowModuleConstr_2J1T1_mu_mc_UL2016postVFP =   lambda : cutflow(2,1,True,"mu",True,'UL2016postVFP')
cutflowModuleConstr_2J1T1_mu_data_UL2016postVFP =   lambda : cutflow(2,1,True,"mu",False,'UL2016postVFP')
cutflowModuleConstr_2J1T1_el_mc_UL2016postVFP =   lambda : cutflow(2,1,True,"el",True,'UL2016postVFP')
cutflowModuleConstr_2J1T1_el_data_UL2016postVFP =   lambda : cutflow(2,1,True,"el",False,'UL2016postVFP')


cutflowModuleConstr_2J1T0_mu_mc_2016 =   lambda : cutflow(2,1,False,"mu",True,'2016')
cutflowModuleConstr_2J1T0_mu_data_2016 =   lambda : cutflow(2,1,False,"mu",False,'2016')
cutflowModuleConstr_2J1T0_el_mc_2016 =   lambda : cutflow(2,1,False,"el",True,'2016')
cutflowModuleConstr_2J1T0_el_data_2016 =   lambda : cutflow(2,1,False,"el",False,'2016')

cutflowModuleConstr_2J1T0_mu_mc_UL2016preVFP =   lambda : cutflow(2,1,False,"mu",True,'UL2016preVFP')
cutflowModuleConstr_2J1T0_mu_data_UL2016preVFP =   lambda : cutflow(2,1,False,"mu",False,'UL2016preVFP')
cutflowModuleConstr_2J1T0_el_mc_UL2016preVFP =   lambda : cutflow(2,1,False,"el",True,'UL2016preVFP')
cutflowModuleConstr_2J1T0_el_data_UL2016preVFP =   lambda : cutflow(2,1,False,"el",False,'UL2016preVFP')

cutflowModuleConstr_2J1T0_mu_mc_UL2016postVFP =   lambda : cutflow(2,1,False,"mu",True,'UL2016postVFP')
cutflowModuleConstr_2J1T0_mu_data_UL2016postVFP =   lambda : cutflow(2,1,False,"mu",False,'UL2016postVFP')
cutflowModuleConstr_2J1T0_el_mc_UL2016postVFP =   lambda : cutflow(2,1,False,"el",True,'UL2016postVFP')
cutflowModuleConstr_2J1T0_el_data_UL2016postVFP =   lambda : cutflow(2,1,False,"el",False,'UL2016postVFP')


cutflowModuleConstr_2J1T1_mu_mc_2017 =   lambda : cutflow(2,1,True,"mu",True,'2017')
cutflowModuleConstr_2J1T1_mu_data_2017 =   lambda : cutflow(2,1,True,"mu",False,'2017')
cutflowModuleConstr_2J1T1_el_mc_2017 =   lambda : cutflow(2,1,True,"el",True,'2017')
cutflowModuleConstr_2J1T1_el_data_2017 =   lambda : cutflow(2,1,True,"el",False,'2017')

cutflowModuleConstr_2J1T0_mu_mc_2017 =   lambda : cutflow(2,1,False,"mu",True,'2017')
cutflowModuleConstr_2J1T0_mu_data_2017 =   lambda : cutflow(2,1,False,"mu",False,'2017')
cutflowModuleConstr_2J1T0_el_mc_2017 =   lambda : cutflow(2,1,False,"el",True,'2017')
cutflowModuleConstr_2J1T0_el_data_2017 =   lambda : cutflow(2,1,False,"el",False,'2017')

cutflowModuleConstr_2J1T1_mu_mc_UL2017 =   lambda : cutflow(2,1,True,"mu",True,'UL2017')
cutflowModuleConstr_2J1T1_mu_data_UL2017 =   lambda : cutflow(2,1,True,"mu",False,'UL2017')
cutflowModuleConstr_2J1T1_el_mc_UL2017 =   lambda : cutflow(2,1,True,"el",True,'UL2017')
cutflowModuleConstr_2J1T1_el_data_UL2017 =   lambda : cutflow(2,1,True,"el",False,'UL2017')

cutflowModuleConstr_2J1T0_mu_mc_UL2017 =   lambda : cutflow(2,1,False,"mu",True,'UL2017')
cutflowModuleConstr_2J1T0_mu_data_UL2017 =   lambda : cutflow(2,1,False,"mu",False,'UL2017')
cutflowModuleConstr_2J1T0_el_mc_UL2017 =   lambda : cutflow(2,1,False,"el",True,'UL2017')


cutflowModuleConstr_2J1T1_mu_mc_UL2018 =   lambda : cutflow(2,1,True,"mu",True,'UL2018')
cutflowModuleConstr_2J1T1_mu_data_UL2018 =   lambda : cutflow(2,1,True,"mu",False,'UL2018')
cutflowModuleConstr_2J1T1_el_mc_UL2018 =   lambda : cutflow(2,1,True,"el",True,'UL2018')
cutflowModuleConstr_2J1T1_el_data_UL2018 =   lambda : cutflow(2,1,True,"el",False,'UL2018')

cutflowModuleConstr_2J1T0_mu_mc_UL2018 =   lambda : cutflow(2,1,False,"mu",True,'UL2018')
cutflowModuleConstr_2J1T0_mu_data_UL2018 =   lambda : cutflow(2,1,False,"mu",False,'UL2018')
cutflowModuleConstr_2J1T0_el_mc_UL2018 =   lambda : cutflow(2,1,False,"el",True,'UL2018')
#if __name__ == "__main__":
#    if(InFile==None):
#   	print "provide input file cutflow.py -f inputfile.root"
#   	sys.exit()



    #cutflow_2J1T1_mu_mc_UL2016preVFP = cutflow_class(2,1,True,"el",True,'UL2016preVFP')
    #cutflow_2J1T1_mu_mc_UL2016preVFP.analyze(myTree)
     
