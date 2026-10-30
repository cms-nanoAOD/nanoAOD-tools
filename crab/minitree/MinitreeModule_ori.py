import ROOT
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Mc_prob_cal_forBweght import *
from foxwol_n_fourmomentumSolver import *

def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print 'WARNING: catching exception and returning -1. Exception arguments: %s' % e.args
            return -1.
        else:
            raise e

"""def MuonRC_cal_MC(roccor,genparticles,genIdx,Mucharge,Mupt,Mueta,Muphi,MunTrackerLayers):                                           #Rochester correction
        if genIdx >= 0 and genIdx < len(genparticles):
           genMu = genparticles[genIdx]
           MuonPt_corr = Mupt * mk_safe(roccor.kSpreadMC, Mucharge, Mupt, Mueta, Muphi, genparticles[genIdx].pt)
	   MuonPt_corr_error = Mupt*mk_safe(roccor.kSpreadMCerror, Mucharge, Mupt, Mueta, Muphi, genparticles[genIdx].pt)
	   #print MuonPt_corr," ", MuonPt_corr_error
	else:
           u1 = random.uniform(0.0, 1.0)
           MuonPt_corr=Mupt*mk_safe(roccor.kSmearMC, Mucharge, Mupt, Mueta, Muphi, MunTrackerLayers, u1)
           MuonPt_corr_error = Mupt*mk_safe(roccor.kSmearMCerror, Mucharge, Mupt, Mueta, Muphi, MunTrackerLayers, u1)
        return MuonPt_corr,MuonPt_corr_error

def MuonRC_cal_Data(roccor,Mucharge,Mupt,Mueta,Muphi):
	MuonPt_corr = Mupt * mk_safe(roccor.kScaleDT,Mucharge, Mupt, Mueta, Muphi)
	MuonPt_corr_error = Mupt * mk_safe(roccor.kScaleDTerror,Mucharge, Mupt, Mueta, Muphi)
        return MuonPt_corr,MuonPt_corr_error """

class MinitreeProducer(Module):
    def __init__(self,Total_Njets,BTag_Njets,Isolation,letopn_flv,isMC,dataYear):
	self.Total_Njets = Total_Njets 
        self.BTag_Njets = BTag_Njets
	self.Isolation = Isolation
	self.letopn_flv = letopn_flv
	self.isMC = isMC
	self.dataYear = dataYear

	"""rc_corrections={
                '2016' : 'RoccoR2016.txt',
                '2017' : 'RoccoR2017.txt',
                '2018' : 'RoccoR2018.txt'}	
	rc_dir = 'roccor.Run2.v3'
	p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections[self.dataYear])"""

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	
	if(self.letopn_flv == 'mu'):
	     self.out.branch("MuonPt","F")
	     self.out.branch("MuonEta","F")
	     self.out.branch("MuonPhi","F")
	     self.out.branch("MuonMass","F")
	     self.out.branch("MuonE","F")
	     self.out.branch("MuonCharge","I")
	     """self.out.branch("Muon_corrected_pt", "F")
             self.out.branch("Muon_correctedUp_pt", "F")
             self.out.branch("Muon_correctedDown_pt", "F")
	     self.out.branch("mtwMass_RC_corr", "F")"""	
	     if(self.isMC==True):self.out.branch("muSF","F")
	
	if(self.letopn_flv == 'el'):
             self.out.branch("ElectronPt","F")
	     self.out.branch("ElectronEta","F")
	     self.out.branch("ElectronSCEta","F")
	     self.out.branch("ElectronPhi","F")
	     self.out.branch("ElectronMass","F")
	     self.out.branch("ElectronE","F") 	
	     self.out.branch("ElectronCharge","I")
	     if(self.isMC==True):self.out.branch("elSF","F")
	self.out.branch("Px_nu","F")
	self.out.branch("Py_nu","F")
	self.out.branch("Pz_nu","F")
        self.out.branch("mtwMass","F")
	self.out.branch("bJetMass",  "F")
        self.out.branch("bJetPt",  "F")
        self.out.branch("bJetEta",  "F")
        self.out.branch("abs_bJetEta",  "F")
        self.out.branch("bJetPhi",  "F")
        self.out.branch("bJetdeepCSV",  "F")
        if(self.isMC==True):self.out.branch("bJethadronFlavour",  "F")

	self.out.branch("lJetMass",  "F")
        self.out.branch("lJetPt",  "F")
        self.out.branch("lJetEta",  "F")
        self.out.branch("abs_lJetEta",  "F")
        self.out.branch("lJetPhi",  "F")
        self.out.branch("lJetdeepCSV",  "F")
        if(self.isMC==True):self.out.branch("lJethadronFlavour",  "F")

	if(self.Total_Njets == 3 and  (self.BTag_Njets == 1 or self.BTag_Njets == 2)):
	    self.out.branch("oJetMass",  "F")
            self.out.branch("oJetPt",  "F")
            self.out.branch("oJetEta",  "F")
            self.out.branch("abs_oJetEta",  "F")
            self.out.branch("oJetPhi",  "F")
            self.out.branch("oJetdeepCSV",  "F")
            if(self.isMC==True):self.out.branch("oJethadronFlavour",  "F")

	self.out.branch("FW1", "F")
	self.out.branch("FW2", "F")
	self.out.branch("FW3", "F")

	self.out.branch("topMass", "F")
	self.out.branch("topPt", "F")
	self.out.branch("cosThetaStar", "F")
	self.out.branch("cosThetaStar", "F")
	self.out.branch("mlb", "F")
	self.out.branch("E_lb","F")
	self.out.branch("p_lb","F")
	self.out.branch("theta_lb", "F")
	self.out.branch("jetpTSum","F")
	self.out.branch("hardJetMass", "F")
	self.out.branch("lJetMass", "F")
	self.out.branch("diJetMass","F")
	self.out.branch("dEta_bJet_lJet","F")
	self.out.branch("dEta_top_lJet","F")
	if(self.letopn_flv == 'mu'):
	    self.out.branch("dEta_mu_bJet","F")
	    self.out.branch("dEta_mu_lJet","F")
	    self.out.branch("dPhi_mu_bJet","F")
	    self.out.branch("dPhi_mu_met","F")
	    self.out.branch("dPhi_mu_lJet","F" )
	    self.out.branch("dR_mu_bJet","F" )		
	    self.out.branch("dR_mu_lJet","F") 
	
	if(self.letopn_flv == 'el'):
            self.out.branch("dEta_el_bJet","F")
            self.out.branch("dEta_el_lJet","F")
            self.out.branch("dPhi_el_bJet","F")
            self.out.branch("dPhi_el_met","F")
            self.out.branch("dPhi_el_lJet","F" )
            self.out.branch("dR_el_bJet","F" )
            self.out.branch("dR_el_lJet","F")

	self.out.branch("dPhi_bJet_lJet","F")
	self.out.branch("dPhi_top_lJet", "F")
	self.out.branch("dR_bJet_lJet","F") 
	self.out.branch("dR_top_lJet","F") 
	if(self.isMC==True):
	    self.out.branch("Xsec_wgt","F")
	    self.out.branch("Event_wgt","F")
	    self.out.branch("LHEWeightSign","F")
	    self.shape_systs = ["Central","lf","hf","cferr1","cferr2","lfstats1","lfstats2","hfstats1","hfstats2","jes"]
            for syst in self.shape_systs:
		if(syst == "Central"):self.out.branch("bWeight","F")
                else: self.out.branch("bWeight_"+syst,  "F",lenVar="2")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
	if(self.isMC==True):	
		x_sec = 2890800
		Lumi=1.0
                if(self.dataYear=="2016"):Lumi = 35882.5
		elif(self.dataYear=="2017"):Lumi = 41529.5
		NEvents = 22455794

	        Xsec_wgt = (x_sec*Lumi)/NEvents
	#print Xsec_wgt
	muons = Collection(event, "Muon")
	electrons = Collection(event, "Electron")
	lepton4v = ROOT.TLorentzVector()
	leptonSF = 0
	leptonCharge = 0
	#print self.letopn_flv
	if(self.letopn_flv=="mu"):
	    pt_Thes={
		'2016' : 26,
		'2017' : 30,
		'2018' : None}
	    for lep in muons:
		#print "muonpt = %s muoneta = %s muoniso = %s muonid = %s iso = %s"%(lep.pt,lep.eta,lep.pfRelIso04_all,lep.tightId,self.Isolation)
		if((self.Isolation==True) and lep.pt>pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.06 and lep.tightId==1):
		    lepton4v=lep.p4()
		    leptonCharge = lep.charge
		    if(self.isMC==True):
			leptonSF = lep.SF_Iso
			"""#																		Rochestor correction
			MuonPt_corr,MuonPt_corr_error = MuonRC_cal_MC(self._roccor,Collection(event, "GenPart"), lep.genPartIdx, lep.charge, lep.pt, lep.eta, lep.phi, lep.nTrackerLayers)
		    else:
			MuonPt_corr,MuonPt_corr_error = MuonRC_cal_Data(self._roccor,lep.charge, lep.pt, lep.eta, lep.phi)"""
		    #print "musf = ",leptonSF
		    #print "mu phi = ",lep.phi
		elif((self.Isolation==False) and lep.pt>pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all>0.2 and lep.tightId==1):
		    #print "criteria passed"
		    lepton4v=lep.p4()
		    leptonCharge = lep.charge
		    if(self.isMC==True):
			leptonSF = lep.SF_Iso
			"""#																		Rochestor correction
			MuonPt_corr,MuonPt_corr_error = MuonRC_cal_MC(self._roccor,Collection(event, "GenPart"), lep.genPartIdx, lep.charge, lep.pt, lep.eta, lep.phi, lep.nTrackerLayers)
		    else:
			MuonPt_corr,MuonPt_corr_error = MuonRC_cal_Data(self._roccor,lep.charge, lep.pt, lep.eta, lep.phi)"""

	if(self.letopn_flv=="el"):
            pt_Thes={
                '2016' : 35,
                '2017' : 37,
                '2018' : None}
            for lep in electrons:
		if((self.Isolation==True) and lep.pt>pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased==4 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
		    lepton4v=lep.p4()
		    ElectronSCEta = lep.EtaSC
		    leptonCharge = lep.charge
		    if(self.isMC==True):leptonSF = lep.SF_Iso
		if((self.Isolation==False) and lep.pt>pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased!=4 and lep.cutBased>=1 and (abs(lep.EtaSC)<1.4442 or abs(lep.EtaSC)>1.5660) and ((abs(lep.EtaSC)<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(lep.EtaSC)> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
		    lepton4v=lep.p4()	
		    ElectronSCEta = lep.EtaSC
		    leptonCharge = lep.charge
		    if(self.isMC==True):leptonSF = lep.SF_Veto
		
	#print "muonpx = %s muonpy = %s muonpz = %s muonE = %s"%(lepton4v.Px(),lepton4v.Py(),lepton4v.Pz(),lepton4v.E())
	leptonPt = lepton4v.Pt()
	leptonEta = lepton4v.Eta()
	leptonPhi = lepton4v.Phi()
	#print "leptonPhi = ",leptonPhi
	leptonMass = lepton4v.M()
	leptonE = lepton4v.E()
        met = getattr(event,'MET_pt')
        metphi =getattr(event,'MET_phi')
	#print "math.sqrt() = ",pow((leptonPt+met),2)-pow((leptonPt*math.cos(leptonPhi)+met*math.cos(metphi)),2)-pow((leptonPt*math.sin(leptonPhi)+met*math.sin(metphi)),2)
	#print "math.cos(leptonPhi) = ",math.cos(leptonPhi)," ",leptonPhi
	Px_nu = met*math.cos(metphi)
	#print "math.sin(leptonPhi) = ",math.sin(leptonPhi)," ",leptonPhi
	Py_nu = met*math.sin(metphi)
	mtwMass = math.sqrt(abs(pow((leptonPt+met),2)-pow((leptonPt*math.cos(leptonPhi)+met*math.cos(metphi)),2)-pow((leptonPt*math.sin(leptonPhi)+met*math.sin(metphi)),2)));
	
	"""if(self.letopn_flv == 'mu'): # Rochester correction
	    mtwMass_RC_corr = math.sqrt(abs(pow((MuonPt_corr+met),2)-pow((leptonPt*math.cos(leptonPhi)+met*math.cos(metphi)),2)-pow((MuonPt_corr*math.sin(leptonPhi)+met*math.sin(metphi)),2)));"""

        neutrino4v = ROOT.TLorentzVector()
        neutrino4v = solveNu4Momentum(lepton4v,met*math.cos(metphi),met*math.sin(metphi))
	
	Pz_nu = neutrino4v.Pz() 
	jets = Collection(event, "Jet")
        


	#for jet in jet_id:
	    #print jet.pt
	bJet4v = ROOT.TLorentzVector()
	lJet4v = ROOT.TLorentzVector()
	oJet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
	top4v = ROOT.TLorentzVector()
	jet_id = []
	btagjet_id = [] 
 	njet4v = ROOT.TLorentzVector()
	#drs = getattr(event,"dR_Ljet_Isomu") 
	#for i in (0,len(drs)):
	   #print "dr = ",drs[i]
	for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetId!=0), jets):
	    njet4v.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
	    if(lepton4v.DeltaR(njet4v)>0.4): 
		jet_id.append(jet)
		#print lepton4v.DeltaR(njet4n)
	#print "jet_id = ",jet_id
	Tight_b_tab_crite={
                '2016' : 0.7527,
                '2017' : 0.8001, #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
                '2018' : None}
	Lose_b_tab_crite={
                '2016' : 0.1241,
                '2017' : 0.1522,
                '2018' : None}
	for jet in jet_id:
	    njet4v.SetPtEtaPhiM(jet.pt,jet.eta,jet.phi,jet.mass)
            #print lepton4v.DeltaR(njet4v)
	    #print jet.btagDeepB," ",jet.eta
	#print getattr(event,'event');
	
	for jet in filter(lambda j:(j.btagDeepB>Tight_b_tab_crite[self.dataYear] and abs(j.eta)<2.4), jet_id):
	    btagjet_id.append(jet) 
	#print "btagJet_id = ", btagjet_id
        #if(len(btagjet_id)):	return True
	if(self.Total_Njets == 2 and  self.BTag_Njets == 1 and len(btagjet_id)==0):
		for jet in filter(lambda j:(j.btagDeepB>Lose_b_tab_crite[self.dataYear] and abs(j.eta)<2.4), jet_id):
			btagjet_id.append(jet)
		#print len(btagjet_id)


	#print "--------------------------------------2 J 1 T-----------------------------"
	if( self.Total_Njets == 2 and  self.BTag_Njets == 1):
	    #print "--------------------------------------2 J 1 T-----------------------------"
	    for jet in jet_id:
		if(jet==btagjet_id[0]):
		     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
		     if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
		     #print "Dr bjet inside 2J1T con = ",lepton4v.DeltaR(bJet4v)
		else:
		     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)	
		     if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour
	    del_theta = math.cos(lJet4v.Angle(bJet4v.Vect()))
            Foxwol_h1 = wolformvalue2J(poly1(del_theta),bJetPt,lJetPt)
            Foxwol_h2 = wolformvalue2J(poly2(del_theta),bJetPt,lJetPt)       
	    Foxwol_h3 = wolformvalue2J(poly3(del_theta),bJetPt,lJetPt)
	    oJetPt = 0.   #This is required when we calculate "hardJetMass" 
		     #		//cout<<"costheta="<<cos(lJet4v->Angle(bJet4v->Vect()))<<";poly1="<<poly1(cos(lJet4v->Angle(bJet4v->Vect())))<<";bJetPt="<<bJetPt<<";ljetPt="<<lJetPt<<";Foxwol_h1="<<Foxwol_h1<<endl;	
	elif(self.Total_Njets == 2 and  self.BTag_Njets == 0):
	    #print "--------------------------------------2 J 0 T-----------------------------"
	    for jet in jet_id:
	    	if(jet==jet_id[0]): 
		    deepcsv_score0 =jet.btagDeepB
		    eta0 = abs(jet.eta)
		if(jet==jet_id[1]): 
		    deepcsv_score1 =jet.btagDeepB
		    eta1 = abs(jet.eta)
	    #print  "score0 = %s; score1 = %s" %( deepcsv_score0,deepcsv_score1)
	    if(deepcsv_score0<-1.0 and deepcsv_score1<-1.0):
		if(eta0<eta1):
		    for jet in jet_id:
			if(jet==jet_id[0]):
			     btagjet_id.append(jet)	
			     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
			else:
			     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour
		else:
		    for jet in jet_id:
                        if(jet==jet_id[1]):
			     btagjet_id.append(jet)
			     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
			else:
			     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)	
			     if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour
	    else:
		#print "both score are not less than -1"
		if(deepcsv_score0 > deepcsv_score1):
		    #print "jet0 score > jet1 score "
		    for jet in jet_id:
                        if(jet==jet_id[0]):
			     btagjet_id.append(jet)
			     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
			     #print "bJetMass = %s; bJetPt = %s; bJetEta = %s; abs_bJetEta = %s; bJetPhi = %s; bJetdeepCSV = %s; bJethadronFlavour = %s; bJet4vM = %s; " %(bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJethadronFlavour,bJet4v.M())
			else:
			     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)	
			     if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour
		else:
		    for jet in jet_id:
                        if(jet==jet_id[1]):
			     btagjet_id.append(jet)
			     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
			else:
			     [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)
			     if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour	
	    del_theta=math.cos(lJet4v.Angle(bJet4v.Vect()))
            Foxwol_h1=wolformvalue2J(poly1(del_theta),bJetPt,lJetPt)
            Foxwol_h2=wolformvalue2J(poly2(del_theta),bJetPt,lJetPt)
            Foxwol_h3=wolformvalue2J(poly3(del_theta),bJetPt,lJetPt)
	    oJetPt = 0.   #This is required when we calculate "hardJetMass" 
	elif(self.Total_Njets == 3 and  self.BTag_Njets == 1):
	    #print "--------------------------------------3 J 1 T-----------------------------"
	    jet_compaired=[]
	    for jet in jet_id:
		#print "jet Pt = ", jet.pt
	    	if(jet==btagjet_id[0]):
	    	     #print "btabjet_id = ",jet
		     [bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
	             if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour	
	    	else:
	             jet_compaired.append(jet)
	    #print "comaired jet ids = ",jet_compaired
	    for jet in jet_compaired:
		if(jet==jet_compaired[0]):
                    eta0 = jet.eta
                if(jet==jet_compaired[1]):
                    eta1 = jet.eta
	    #print "eta0 = %s; eta1 = %s" %(eta0,eta1)
	    for jet in jet_compaired:
	    	if(abs(eta0)>abs(eta1)):
		    if(jet==jet_compaired[0]):
			[lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour	
		    else:	
			[oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepCSV,oJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):oJethadronFlavour=jet.hadronFlavour	
		else:
		    if(jet==jet_compaired[1]):
			[lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour	
                    else:			
			[oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepCSV,oJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):oJethadronFlavour=jet.hadronFlavour	
	    [Foxwol_h1,Foxwol_h2,Foxwol_h3]=wolformvalue3J(bJet4v,lJet4v,oJet4v)
	elif(self.Total_Njets == 3 and  self.BTag_Njets == 2):
	    #print "--------------------------------------3 J 2 T-----------------------------"
	    dummyjet_id=[]
	    for jet in jet_id:
		if(jet!=btagjet_id[0] and jet!=btagjet_id[1]):
		    [lJetMass,lJetPt,lJetEta,abs_lJetEta,lJetPhi,lJetdeepCSV,lJet4v]=CollectJetInfo(jet)	
		    if(self.isMC==True):lJethadronFlavour=jet.hadronFlavour
 	    dummybjet0 = ROOT.TLorentzVector()
	    dummybjet1 = ROOT.TLorentzVector()
	    dummytop0 = ROOT.TLorentzVector()
	    dummytop1 = ROOT.TLorentzVector()
	    for jet in btagjet_id:
		if(jet==btagjet_id[0]): 
		    dummybjet0 = jet.p4()
		if(jet==btagjet_id[1]):
                    dummybjet1 = jet.p4()
	    dummytop0= lepton4v+dummybjet0+neutrino4v
	    topmass_bjet0=dummytop0.M()
	    dummytop1= lepton4v+dummybjet1+neutrino4v
            topmass_bjet1=dummytop1.M()
	    for jet in btagjet_id:
		if(abs(topmass_bjet0 - 172.5)<abs(topmass_bjet1 - 172.5)):
		    if(jet==btagjet_id[0]):
			dummyjet_id.append(jet)
			[bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour
		    else:
			[oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepCSV,oJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):oJethadronFlavour=jet.hadronFlavour
		else:
		    if(jet==btagjet_id[1]):
			dummyjet_id.append(jet)
			[bJetMass,bJetPt,bJetEta,abs_bJetEta,bJetPhi,bJetdeepCSV,bJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):bJethadronFlavour=jet.hadronFlavour
		    else:
			[oJetMass,oJetPt,oJetEta,abs_oJetEta,oJetPhi,oJetdeepCSV,oJet4v]=CollectJetInfo(jet)
			if(self.isMC==True):oJethadronFlavour=jet.hadronFlavour
	    [Foxwol_h1,Foxwol_h2,Foxwol_h3]=wolformvalue3J(bJet4v,lJet4v,oJet4v)

	#if(self.Total_Njets == 3 and  self.BTag_Njets == 2): 
	    #btagjet_id.clear()
	    #btagjet_id = dummyjet_id
	
	if(self.isMC==True):
	    bWeight = Probability_2("Central",jet_id)
            for syst in self.shape_systs:
		if(syst=="Central"): 
			self.out.fillBranch("bWeight", bWeight)
		else:
			self.out.fillBranch("bWeight_"+syst,[Probability_2(syst+"_up",jet_id),Probability_2(syst+"_down",jet_id)])
			

	top4v = lepton4v+bJet4v+neutrino4v
	topMass=top4v.M()
	topPt=top4v.Pt()

	mlb = (lepton4v+bJet4v).M()
	E_lb = (lepton4v+bJet4v).E()
	p_lb = (lepton4v+bJet4v).P()
	theta_lb = (lepton4v+bJet4v).Theta()
	jetpTSum = bJetPt+lJetPt
	if(bJetPt>=lJetPt and bJetPt>=oJetPt):hardJetMass = bJet4v.M()
	elif(lJetPt>=bJetPt and lJetPt>=oJetPt):hardJetMass = lJet4v.M()
	elif(oJetPt>=lJetPt and oJetPt>=bJetPt):hardJetMass = oJet4v.M()
	lJetMass = lJet4v.M()
	diJetMass = (lJet4v+bJet4v).M()
	if(self.letopn_flv == 'mu'):
	    dEta_mu_bJet = abs(bJet4v.Eta()-lepton4v.Eta())        #in loretz vector class there is no function avalable for Delta Eta
      	    dEta_mu_lJet = abs(lJet4v.Eta() - lepton4v.Eta()) 
	    dPhi_mu_bJet = lepton4v.DeltaPhi(bJet4v) 
      	    dPhi_mu_met = ROOT.TVector2.Phi_mpi_pi(lepton4v.Phi() - metphi)  #Phi_mpi_pi gives angle -pi to pi
      	    dPhi_mu_lJet = lepton4v.DeltaPhi(lJet4v)
	    dR_mu_bJet = lepton4v.DeltaR(bJet4v)
      	    dR_mu_lJet = lepton4v.DeltaR(lJet4v) 
	if(self.letopn_flv == 'el'):
            dEta_el_bJet = abs(bJet4v.Eta()-lepton4v.Eta())        #in loretz vector class there is no function avalable for Delta Eta
            dEta_el_lJet = abs(lJet4v.Eta() - lepton4v.Eta())
            dPhi_el_bJet = lepton4v.DeltaPhi(bJet4v)
            dPhi_el_met = ROOT.TVector2.Phi_mpi_pi(lepton4v.Phi() - metphi)  #Phi_mpi_pi gives angle -pi to pi
            dPhi_el_lJet = lepton4v.DeltaPhi(lJet4v)
            dR_el_bJet = lepton4v.DeltaR(bJet4v)
            dR_el_lJet = lepton4v.DeltaR(lJet4v)
        dEta_bJet_lJet = abs(lJet4v.Eta() - bJet4v.Eta()) 
        dEta_top_lJet = abs(lJet4v.Eta() - top4v.Eta())				

      	dPhi_bJet_lJet = bJet4v.DeltaPhi(lJet4v)
      	dPhi_top_lJet = top4v.DeltaPhi(lJet4v)

      	dR_bJet_lJet = bJet4v.DeltaR(lJet4v) 
      	dR_top_lJet = top4v.DeltaR(lJet4v)

	
	lep4v_for_transformation = ROOT.TLorentzVector()
        lJet4v_for_transformation = ROOT.TLorentzVector()
	lep4v_for_transformation = lepton4v
	lJet4v_for_transformation = lJet4v       #storing the untranformed lepton4v and ljetv
	bx= top4v.BoostVector().X()
	by= top4v.BoostVector().Y() #calculation the lorezboost commponent of top
	bz= top4v.BoostVector().Z()
	lep4v_for_transformation.Boost(-bx, -by, -bz) #loretz tranformation of lepton4v and ljetv
	lJet4v_for_transformation.Boost(-bx, -by, -bz)
	cosThetaStar = math.cos(lep4v_for_transformation.Angle(lJet4v_for_transformation.Vect()))

	try:
             LHEWeightSign = getattr(event,'LHEWeight_originalXWGTUP')/abs(getattr(event,'LHEWeight_originalXWGTUP'))
        except:
             LHEWeightSign = 1

	if(self.isMC==True):
	     Event_wgt = Xsec_wgt*LHEWeightSign*(getattr(event,'puWeight'))*leptonSF*bWeight

	     self.out.fillBranch("LHEWeightSign",LHEWeightSign)
	     self.out.fillBranch("Xsec_wgt",Xsec_wgt )
	     self.out.fillBranch("Event_wgt",Event_wgt)
	self.out.fillBranch("bJetMass", bJetMass)
        self.out.fillBranch("bJetPt", bJetPt )
        self.out.fillBranch("bJetEta", bJetEta )
        self.out.fillBranch("abs_bJetEta", abs_bJetEta )
        self.out.fillBranch("bJetPhi", bJetPhi )
        self.out.fillBranch("bJetdeepCSV", bJetdeepCSV )
        if(self.isMC==True):self.out.fillBranch("bJethadronFlavour", bJethadronFlavour )

        self.out.fillBranch("lJetMass", lJetMass )
        self.out.fillBranch("lJetPt", lJetPt )
        self.out.fillBranch("lJetEta", lJetEta )
        self.out.fillBranch("abs_lJetEta", abs_lJetEta )
        self.out.fillBranch("lJetPhi", lJetPhi )
        self.out.fillBranch("lJetdeepCSV", lJetdeepCSV )
        if(self.isMC==True):self.out.fillBranch("lJethadronFlavour", lJethadronFlavour )

	if(self.Total_Njets == 3 and  (self.BTag_Njets == 1 or self.BTag_Njets == 2)):
	    self.out.fillBranch("oJetMass", oJetMass )
            self.out.fillBranch("oJetPt", oJetPt )
            self.out.fillBranch("oJetEta", oJetEta )
            self.out.fillBranch("abs_oJetEta", abs_oJetEta )
            self.out.fillBranch("oJetPhi", oJetPhi )
            self.out.fillBranch("oJetdeepCSV", oJetdeepCSV )
            if(self.isMC==True):self.out.fillBranch("oJethadronFlavour", oJethadronFlavour )	
	self.out.fillBranch("Px_nu", Px_nu)
	self.out.fillBranch("Py_nu", Py_nu)
	self.out.fillBranch("Pz_nu", Pz_nu)
	self.out.fillBranch("FW1", Foxwol_h1)
	self.out.fillBranch("FW2", Foxwol_h2)
	self.out.fillBranch("FW3", Foxwol_h3)
	self.out.fillBranch("mtwMass",mtwMass)
	self.out.fillBranch("topMass", topMass)
	self.out.fillBranch("topPt", topPt)
	self.out.fillBranch("cosThetaStar", cosThetaStar)
	self.out.fillBranch("mlb", mlb )
	self.out.fillBranch("E_lb",E_lb )
	self.out.fillBranch("p_lb",p_lb )
	self.out.fillBranch("theta_lb", theta_lb)
	self.out.fillBranch("jetpTSum",jetpTSum )
	self.out.fillBranch("hardJetMass", hardJetMass )
	self.out.fillBranch("lJetMass", lJetMass)
	self.out.fillBranch("diJetMass",diJetMass )
	if(self.letopn_flv == 'mu'):
	    self.out.fillBranch("MuonPt",leptonPt)
	    """self.out.fillBranch("Muon_corrected_pt",MuonPt_corr)                                    # Rochester correction
            self.out.fillBranch("Muon_correctedUp_pt",max(MuonPt_corr+MuonPt_corr_error, 0.0))
            self.out.fillBranch("Muon_correctedDown_pt",max(MuonPt_corr-MuonPt_corr_error, 0.0))
	    self.out.fillBranch("mtwMass_RC_corr", mtwMass_RC_corr)"""
	    self.out.fillBranch("MuonEta",leptonEta)
	    self.out.fillBranch("MuonPhi",leptonPhi)
	    self.out.fillBranch("MuonMass",leptonMass)
	    self.out.fillBranch("MuonE",leptonE)
	    self.out.fillBranch("MuonCharge",leptonCharge)
	    self.out.fillBranch("dEta_mu_bJet",dEta_mu_bJet )
	    self.out.fillBranch("dEta_mu_lJet",dEta_mu_lJet )
	    self.out.fillBranch("dPhi_mu_bJet",dPhi_mu_bJet )
	    self.out.fillBranch("dPhi_mu_met",dPhi_mu_met )
	    self.out.fillBranch("dPhi_mu_lJet",dPhi_mu_lJet )
	    self.out.fillBranch("dR_mu_bJet",dR_mu_bJet)	
	    self.out.fillBranch("dR_mu_lJet",dR_mu_lJet )
	    if(self.isMC==True):self.out.fillBranch("muSF",leptonSF) 

	if(self.letopn_flv == 'el'):
	    self.out.fillBranch("ElectronPt",leptonPt)
            self.out.fillBranch("ElectronEta",leptonEta)
            self.out.fillBranch("ElectronPhi",leptonPhi)
            self.out.fillBranch("ElectronMass",leptonMass)
            self.out.fillBranch("ElectronE",leptonE)
	    self.out.fillBranch("ElectronCharge",leptonCharge)
	    self.out.fillBranch("ElectronSCEta",ElectronSCEta)
            self.out.fillBranch("dEta_el_bJet",dEta_el_bJet )
            self.out.fillBranch("dEta_el_lJet",dEta_el_lJet )
            self.out.fillBranch("dPhi_el_bJet",dPhi_el_bJet )
            self.out.fillBranch("dPhi_el_met",dPhi_el_met )
            self.out.fillBranch("dPhi_el_lJet",dPhi_el_lJet )
            self.out.fillBranch("dR_el_bJet",dR_el_bJet )
            self.out.fillBranch("dR_el_lJet",dR_el_lJet )
	    if(self.isMC==True):self.out.fillBranch("elSF",leptonSF)

	self.out.fillBranch("dEta_bJet_lJet",dEta_bJet_lJet )
	self.out.fillBranch("dEta_top_lJet",dEta_top_lJet )
	self.out.fillBranch("dPhi_bJet_lJet",dPhi_bJet_lJet )
	self.out.fillBranch("dPhi_top_lJet", dPhi_top_lJet )
	self.out.fillBranch("dR_bJet_lJet",dR_bJet_lJet ) 
	self.out.fillBranch("dR_top_lJet",dR_top_lJet ) 
	#print '--------------------------------------------------------------------------------'
	#print(getattr(event,'event'))
        return True

#----------------------------------------------2J1T------------------------------------------------
MinitreeModuleConstr2J1T1_mu_mc_2016 = lambda : MinitreeProducer(2,1,True,'mu',True,'2016')
MinitreeModuleConstr2J1T1_mu_data_2016 = lambda : MinitreeProducer(2,1,True,'mu',False,'2016')
MinitreeModuleConstr2J1T1_el_mc_2016 = lambda : MinitreeProducer(2,1,True,'el',True,'2016')
MinitreeModuleConstr2J1T1_el_data_2016 = lambda : MinitreeProducer(2,1,True,'el',False,'2016')

MinitreeModuleConstr2J1T0_mu_mc_2016 = lambda : MinitreeProducer(2,1,False,'mu',True,'2016')
MinitreeModuleConstr2J1T0_mu_data_2016 = lambda : MinitreeProducer(2,1,False,'mu',False,'2016')
MinitreeModuleConstr2J1T0_el_mc_2016 = lambda : MinitreeProducer(2,1,False,'el',True,'2016')
MinitreeModuleConstr2J1T0_el_data_2016 = lambda : MinitreeProducer(2,1,False,'el',False,'2016')

MinitreeModuleConstr2J1T1_mu_mc_2017 = lambda : MinitreeProducer(2,1,True,'mu',True,'2017')
MinitreeModuleConstr2J1T1_mu_data_2017 = lambda : MinitreeProducer(2,1,True,'mu',False,'2017')
MinitreeModuleConstr2J1T1_el_mc_2017 = lambda : MinitreeProducer(2,1,True,'el',True,'2017')
MinitreeModuleConstr2J1T1_el_data_2017 = lambda : MinitreeProducer(2,1,True,'el',False,'2017')

MinitreeModuleConstr2J1T0_mu_mc_2017 = lambda : MinitreeProducer(2,1,False,'mu',True,'2017')
MinitreeModuleConstr2J1T0_mu_data_2017 = lambda : MinitreeProducer(2,1,False,'mu',False,'2017')
MinitreeModuleConstr2J1T0_el_mc_2017 = lambda : MinitreeProducer(2,1,False,'el',True,'2017')
MinitreeModuleConstr2J1T0_el_data_2017 = lambda : MinitreeProducer(2,1,False,'el',False,'2017')

#----------------------------------------------2J0T------------------------------------------------

MinitreeModuleConstr2J0T1_mu_mc_2016 = lambda : MinitreeProducer(2,0,True,'mu',True,'2016')
MinitreeModuleConstr2J0T1_mu_data_2016 = lambda : MinitreeProducer(2,0,True,'mu',False,'2016')
MinitreeModuleConstr2J0T1_el_mc_2016 = lambda : MinitreeProducer(2,0,True,'el',True,'2016')
MinitreeModuleConstr2J0T1_el_data_2016 = lambda : MinitreeProducer(2,0,True,'el',False,'2016')

MinitreeModuleConstr2J0T0_mu_mc_2016 = lambda : MinitreeProducer(2,0,False,'mu',True,'2016')
MinitreeModuleConstr2J0T0_mu_data_2016 = lambda : MinitreeProducer(2,0,False,'mu',False,'2016')
MinitreeModuleConstr2J0T0_el_mc_2016 = lambda : MinitreeProducer(2,0,False,'el',True,'2016')
MinitreeModuleConstr2J0T0_el_data_2016 = lambda : MinitreeProducer(2,0,False,'el',False,'2016')

MinitreeModuleConstr2J0T1_mu_mc_2017 = lambda : MinitreeProducer(2,0,True,'mu',True,'2017')
MinitreeModuleConstr2J0T1_mu_data_2017 = lambda : MinitreeProducer(2,0,True,'mu',False,'2017')
MinitreeModuleConstr2J0T1_el_mc_2017 = lambda : MinitreeProducer(2,0,True,'el',True,'2017')
MinitreeModuleConstr2J0T1_el_data_2017 = lambda : MinitreeProducer(2,0,True,'el',False,'2017')

MinitreeModuleConstr2J0T0_mu_mc_2017 = lambda : MinitreeProducer(2,0,False,'mu',True,'2017')
MinitreeModuleConstr2J0T0_mu_data_2017 = lambda : MinitreeProducer(2,0,False,'mu',False,'2017')
MinitreeModuleConstr2J0T0_el_mc_2017 = lambda : MinitreeProducer(2,0,False,'el',True,'2017')
MinitreeModuleConstr2J0T0_el_data_2017 = lambda : MinitreeProducer(2,0,False,'el',False,'2017')

#----------------------------------------------3J1T-----------------------------------------------

MinitreeModuleConstr3J1T1_mu_mc_2016 = lambda : MinitreeProducer(3,1,True,'mu',True,'2016')
MinitreeModuleConstr3J1T1_mu_data_2016 = lambda : MinitreeProducer(3,1,True,'mu',False,'2016')
MinitreeModuleConstr3J1T1_el_mc_2016 = lambda : MinitreeProducer(3,1,True,'el',True,'2016')
MinitreeModuleConstr3J1T1_el_data_2016 = lambda : MinitreeProducer(3,1,True,'el',False,'2016')

MinitreeModuleConstr3J1T0_mu_mc_2016 = lambda : MinitreeProducer(3,1,False,'mu',True,'2016')
MinitreeModuleConstr3J1T0_mu_data_2016 = lambda : MinitreeProducer(3,1,False,'mu',False,'2016')
MinitreeModuleConstr3J1T0_el_mc_2016 = lambda : MinitreeProducer(3,1,False,'el',True,'2016')
MinitreeModuleConstr3J1T0_el_data_2016 = lambda : MinitreeProducer(3,1,False,'el',False,'2016')

MinitreeModuleConstr3J1T1_mu_mc_2017 = lambda : MinitreeProducer(3,1,True,'mu',True,'2017')
MinitreeModuleConstr3J1T1_mu_data_2017 = lambda : MinitreeProducer(3,1,True,'mu',False,'2017')
MinitreeModuleConstr3J1T1_el_mc_2017 = lambda : MinitreeProducer(3,1,True,'el',True,'2017')
MinitreeModuleConstr3J1T1_el_data_2017 = lambda : MinitreeProducer(3,1,True,'el',False,'2017')

MinitreeModuleConstr3J1T0_mu_mc_2017 = lambda : MinitreeProducer(3,1,False,'mu',True,'2017')
MinitreeModuleConstr3J1T0_mu_data_2017 = lambda : MinitreeProducer(3,1,False,'mu',False,'2017')
MinitreeModuleConstr3J1T0_el_mc_2017 = lambda : MinitreeProducer(3,1,False,'el',True,'2017')
MinitreeModuleConstr3J1T0_el_data_2017 = lambda : MinitreeProducer(3,1,False,'el',False,'2017')

#------------------------------------------3J2T---------------------------------------------------

MinitreeModuleConstr3J2T1_mu_mc_2016 = lambda : MinitreeProducer(3,2,True,'mu',True,'2016')
MinitreeModuleConstr3J2T1_mu_data_2016 = lambda : MinitreeProducer(3,2,True,'mu',False,'2016')
MinitreeModuleConstr3J2T1_el_mc_2016 = lambda : MinitreeProducer(3,2,True,'el',True,'2016')
MinitreeModuleConstr3J2T1_el_data_2016 = lambda : MinitreeProducer(3,2,True,'el',False,'2016')

MinitreeModuleConstr3J2T0_mu_mc_2016 = lambda : MinitreeProducer(3,2,False,'mu',True,'2016')
MinitreeModuleConstr3J2T0_mu_data_2016 = lambda : MinitreeProducer(3,2,False,'mu',False,'2016')
MinitreeModuleConstr3J2T0_el_mc_2016 = lambda : MinitreeProducer(3,2,False,'el',True,'2016')
MinitreeModuleConstr3J2T0_el_data_2016 = lambda : MinitreeProducer(3,2,False,'el',False,'2016')

MinitreeModuleConstr3J2T1_mu_mc_2017 = lambda : MinitreeProducer(3,2,True,'mu',True,'2017')
MinitreeModuleConstr3J2T1_mu_data_2017 = lambda : MinitreeProducer(3,2,True,'mu',False,'2017')
MinitreeModuleConstr3J2T1_el_mc_2017 = lambda : MinitreeProducer(3,2,True,'el',True,'2017')
MinitreeModuleConstr3J2T1_el_data_2017 = lambda : MinitreeProducer(3,2,True,'el',False,'2017')

MinitreeModuleConstr3J2T0_mu_mc_2017 = lambda : MinitreeProducer(3,2,False,'mu',True,'2017')
MinitreeModuleConstr3J2T0_mu_data_2017 = lambda : MinitreeProducer(3,2,False,'mu',False,'2017')
MinitreeModuleConstr3J2T0_el_mc_2017 = lambda : MinitreeProducer(3,2,False,'el',True,'2017')
MinitreeModuleConstr3J2T0_el_data_2017 = lambda : MinitreeProducer(3,2,False,'el',False,'2017')

#------------------------------------------ 2J1L0T---------------------------------------------------------
MinitreeModuleConstr2J1L0T1_mu_mc_2016 = lambda : MinitreeProducer(2,1,True,'mu',True,'2016')
MinitreeModuleConstr2J1L0T1_mu_data_2016 = lambda : MinitreeProducer(2,1,True,'mu',False,'2016')
MinitreeModuleConstr2J1L0T1_el_mc_2016 = lambda : MinitreeProducer(2,1,True,'el',True,'2016')
MinitreeModuleConstr2J1L0T1_el_data_2016 = lambda : MinitreeProducer(2,1,True,'el',False,'2016')

MinitreeModuleConstr2J1L0T0_mu_mc_2016 = lambda : MinitreeProducer(2,1,False,'mu',True,'2016')
MinitreeModuleConstr2J1L0T0_mu_data_2016 = lambda : MinitreeProducer(2,1,False,'mu',False,'2016')
MinitreeModuleConstr2J1L0T0_el_mc_2016 = lambda : MinitreeProducer(2,1,False,'el',True,'2016')
MinitreeModuleConstr2J1L0T0_el_data_2016 = lambda : MinitreeProducer(2,1,False,'el',False,'2016')

MinitreeModuleConstr2J1L0T1_mu_mc_2017 = lambda : MinitreeProducer(2,1,True,'mu',True,'2017')
MinitreeModuleConstr2J1L0T1_mu_data_2017 = lambda : MinitreeProducer(2,1,True,'mu',False,'2017')
MinitreeModuleConstr2J1L0T1_el_mc_2017 = lambda : MinitreeProducer(2,1,True,'el',True,'2017')
MinitreeModuleConstr2J1L0T1_el_data_2017 = lambda : MinitreeProducer(2,1,True,'el',False,'2017')

MinitreeModuleConstr2J1L0T1_mu_mc_2017 = lambda : MinitreeProducer(2,1,False,'mu',True,'2017')
MinitreeModuleConstr2J1L0T1_mu_data_2017 = lambda : MinitreeProducer(2,1,False,'mu',False,'2017')
MinitreeModuleConstr2J1L0T1_el_mc_2017 = lambda : MinitreeProducer(2,1,False,'el',True,'2017')
MinitreeModuleConstr2J1L0T1_el_data_2017 = lambda : MinitreeProducer(2,1,False,'el',False,'2017')
