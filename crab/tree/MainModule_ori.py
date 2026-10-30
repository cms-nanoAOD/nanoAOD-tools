import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from scaleFactor import *

class MainProducer(Module):
    def __init__(self,MC,datayear,dataset):
        self.MC = MC
	print self.MC
	self.datayear = datayear
	self.dataset = dataset
	if(self.MC==True):self.dataset = None
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	if(self.MC): print "self.MC = ",self.MC
	self.out.branch("Jet_dR_Ljet_Isomu",  "F",lenVar="100")
	self.out.branch("Jet_dR_Ljet_AntiIsomu",  "F",lenVar="101")
	self.out.branch("Jet_dR_Ljet_Isoel",  "F",lenVar="102")
	self.out.branch("Jet_dR_Ljet_AntiIsoel",  "F",lenVar="103")

	if(True):
	    self.out.branch("Electron_EtaSC",  "F",lenVar="nElectron")


	    if(self.MC):
		self.out.branch("Electron_SF_Iso",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Iso_IDUp",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Iso_IDDown",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Iso_TrigUp",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Iso_TrigDown",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Veto",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Veto_IDUp",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Veto_IDDown",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Veto_TrigUp",  "F",lenVar="nElectron")
		self.out.branch("Electron_SF_Veto_TrigDown",  "F",lenVar="nElectron")
	if(self.MC):
	    self.out.branch("Muon_SF_Iso",  "F",lenVar="nMuon")
	    self.out.branch("Muon_SF_IsoUp",  "F",lenVar="nMuon")
	    self.out.branch("Muon_SF_IsoDown",  "F",lenVar="nMuon")
	    self.out.branch("Muon_SF_Iso_IDUp",  "F",lenVar="nMuon")
	    self.out.branch("Muon_SF_Iso_IDDown",  "F",lenVar="nMuon")
            self.out.branch("Muon_SF_Iso_TrigUp",  "F",lenVar="nMuon")
	    self.out.branch("Muon_SF_Iso_TrigDown",  "F",lenVar="nMuon")
		

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
	
        electrons = Collection(event, "Electron")
	muons = Collection(event, "Muon")
	jets = Collection(event,"Jet")
	pt_Thes_mu = {
                '2016' : 26,
                '2017' : 30,
                '2018' : None}
	pt_Thes_el={
                '2016' : 35,
                '2017' : 37,
                '2018' : None}
	if(self.MC):
	    if(self.datayear=='2016'): TotalLumi=35855
	    elif(self.datayear=='2017'):TotalLumi=41529
	    elif(self.datayear=='2018'):TotalLumi=41520 
	    Ele_EtaSC,Electron_SF_Iso,Electron_SF_Iso_IDUp,Electron_SF_Iso_IDDown,Electron_SF_Iso_TrigUp,Electron_SF_Iso_TrigDown,Electron_SF_Veto,Electron_SF_Veto_IDUp,Electron_SF_Veto_IDDown,Electron_SF_Veto_TrigUp,Electron_SF_Veto_TrigDown=([]for i in range(11))
	    Muon_SF_Iso,Muon_SF_IsoUp,Muon_SF_IsoDown,Muon_SF_Iso_IDUp,Muon_SF_Iso_IDDown,Muon_SF_Iso_TrigUp,Muon_SF_Iso_TrigDown,Muon_SF_Veto,Muon_SF_Veto_IDUp,Muon_SF_Veto_IDDown,Muon_SF_Veto_TrigUp,Muon_SF_Veto_TrigDown=([]for i in range(12))	
	    Jet_dR_Ljet_Isomu,Jet_dR_Ljet_AntiIsomu,Jet_dR_Ljet_Isoel,Jet_dR_Ljet_AntiIsoel = ([]for i in range(4))
	    if(True):
		 count=0
		 Jetpt = getattr(event,'Jet_pt')
		 jetpt = Jetpt[0]
		 for lep in electrons :
		    Ele_EtaSC.append(lep.deltaEtaSC + lep.eta)
		    Electron_SF_Iso.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Tight","noSyst"))
		    Electron_SF_Iso_IDUp.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Tight","IDUp")) 
		    Electron_SF_Iso_IDDown.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Tight","IDDown"))
		    Electron_SF_Iso_TrigUp.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Tight","TrigUp"))
		    Electron_SF_Iso_TrigDown.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Tight","TrigDown"))
		    Electron_SF_Veto.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Veto","noSyst"))
		    Electron_SF_Veto_IDUp.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Veto","IDUp"))
		    Electron_SF_Veto_IDDown.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Veto","IDDown"))
		    Electron_SF_Veto_TrigUp.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Veto","TrigUp"))
		    Electron_SF_Veto_TrigDown.append(create_elSF(self.datayear,lep.pt,Ele_EtaSC[count],jetpt,"Veto","TrigDown"))
		    if(len(Jet_dR_Ljet_Isoel)==len(Jet_dR_Ljet_AntiIsoel) and lep.pt>pt_Thes_el[self.datayear] and abs(lep.eta)<2.1 and lep.cutBased>=1 and (abs(Ele_EtaSC[count])<1.4442 or abs(Ele_EtaSC[count])>1.5660) and ((abs(Ele_EtaSC[count])<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(Ele_EtaSC[count])> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
			el4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			el4v = lep.p4()
			#print "el pt =",el4v.Pt()
			#for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetId!=0), jets):
			#if(len(Jet_dR_Ljet_Isoel)==len(Jet_dR_Ljet_AntiIsoel)): #this condiation make sure that len(dR)=len(jets) and dr information is saved for only one leptop and if the second leption is found then dr info is skiped because any way we rejet those event which has two tight lepton in cut strings for mimitree
			for jet in jets:
		    	    jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			    jet4v = jet.p4()
			    if(lep.cutBased==4):
				Jet_dR_Ljet_Isoel.append(el4v.DeltaR(jet4v))
				#Jet_dR_Ljet_AntiIsoel.append(999) 
			    if(lep.cutBased!=4 and lep.cutBased>=1):
				#Jet_dR_Ljet_Isoel.append(999)
				Jet_dR_Ljet_AntiIsoel.append(el4v.DeltaR(jet4v))


		    count=count+1
		 #print 'elSF_Veto=',Electron_SF_Iso
		 #print "Antijet dr =", Jet_dR_Ljet_AntiIsoel
		 self.out.fillBranch("Electron_EtaSC", Ele_EtaSC)
		 self.out.fillBranch("Electron_SF_Iso", Electron_SF_Iso)
		 self.out.fillBranch("Electron_SF_Iso_IDUp",Electron_SF_Iso_IDUp)
		 self.out.fillBranch("Electron_SF_Iso_IDDown",Electron_SF_Iso_IDDown)
		 self.out.fillBranch("Electron_SF_Iso_TrigUp",Electron_SF_Iso_TrigUp)
		 self.out.fillBranch("Electron_SF_Iso_TrigDown",Electron_SF_Iso_TrigDown)
		 self.out.fillBranch("Electron_SF_Veto", Electron_SF_Veto)
		 self.out.fillBranch("Electron_SF_Veto_IDUp",Electron_SF_Veto_IDUp)
		 self.out.fillBranch("Electron_SF_Veto_IDDown",Electron_SF_Veto_IDDown)
		 self.out.fillBranch("Electron_SF_Veto_TrigUp",Electron_SF_Veto_TrigUp)
		 self.out.fillBranch("Electron_SF_Veto_TrigDown",Electron_SF_Veto_TrigDown)
	    self.out.fillBranch("Jet_dR_Ljet_Isoel",Jet_dR_Ljet_Isoel)
	    self.out.fillBranch("Jet_dR_Ljet_AntiIsoel",Jet_dR_Ljet_AntiIsoel)
	    if(True):
		 for lep in muons :
		    #if(lep.pt<=5):print lep.pt
		    #print lep.pt
		    Muon_SF_Iso.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"noSyst"))
		    Muon_SF_IsoUp.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"IsoUp"))
		    Muon_SF_IsoDown.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"IsoDown"))
		    Muon_SF_Iso_IDUp.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"IDUp")) 
		    Muon_SF_Iso_IDDown.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"IDDown"))
		    Muon_SF_Iso_TrigUp.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"TrigUp"))
		    Muon_SF_Iso_TrigDown.append(create_muSF(self.datayear,lep.pt,lep.eta,lep.pfRelIso04_all,TotalLumi,"TrigDown"))
		    if(len(Jet_dR_Ljet_Isomu)== len(Jet_dR_Ljet_AntiIsomu) and lep.pt>pt_Thes_mu[self.datayear] and abs(lep.eta)<2.4 and (lep.pfRelIso04_all<0.06 or lep.pfRelIso04_all>0.2) and lep.tightId==1):
			muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			muon4v = lep.p4()
			#for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetId!=0), jets):
			#if(len(Jet_dR_Ljet_Isomu)==len(Jet_dR_Ljet_AntiIsomu)): #this condiation make sure that len(dR)=len(jets) and dr information is saved for only one leptop and if the second leption is found then dr info is skiped because any way we rejet those event which has two tight lepton in cut strings for mimitree
			for jet in jets:
			    jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			    jet4v = jet.p4()
			    if(lep.pfRelIso04_all<0.06):
				Jet_dR_Ljet_Isomu.append(muon4v.DeltaR(jet4v))
				#Jet_dR_Ljet_AntiIsomu.append(999.0)
				#print jet ," ",lep," jetPt = ",jet4v.Pt(), "dr = ",muon4v.DeltaR(jet4v)
			    if(lep.pfRelIso04_all>0.2):
				Jet_dR_Ljet_AntiIsomu.append(muon4v.DeltaR(jet4v))
				#Jet_dR_Ljet_Isomu.append(999.0)
		    #print 'Muon_SF_Iso = ',Muon_SF_Iso
		    #if(nolepton>1):print(nolepton," jets = ",len(jets), " Jet_dR_Ljet_Isomu = ", len(Jet_dR_Ljet_Isomu)," Jet_dR_Ljet_AntiIsomu = ",len(Jet_dR_Ljet_AntiIsomu) )
		 self.out.fillBranch("Muon_SF_Iso", Muon_SF_Iso)
		 self.out.fillBranch("Muon_SF_IsoUp", Muon_SF_IsoUp)
		 self.out.fillBranch("Muon_SF_IsoDown", Muon_SF_IsoDown)
		 self.out.fillBranch("Muon_SF_Iso_IDUp",Muon_SF_Iso_IDUp)
		 self.out.fillBranch("Muon_SF_Iso_IDDown",Muon_SF_Iso_IDDown)
		 self.out.fillBranch("Muon_SF_Iso_TrigUp",Muon_SF_Iso_TrigUp)
		 self.out.fillBranch("Muon_SF_Iso_TrigDown",Muon_SF_Iso_TrigDown)
	    self.out.fillBranch("Jet_dR_Ljet_Isomu",Jet_dR_Ljet_Isomu)
	    self.out.fillBranch("Jet_dR_Ljet_AntiIsomu",Jet_dR_Ljet_AntiIsomu)


	    #self.out.fillBranch("Jet_dR_Ljet_AntiIsomu",Jet_dR_Ljet_AntiIsomu)

	    #print "----------------------------------------------------------------->"

	elif(self.MC == False and self.dataset == "singleElectron"):
	    #print self.dataset
	    Ele_EtaSC,Jet_dR_Ljet_Isoel,Jet_dR_Ljet_AntiIsoel = ([]for i in range(3))
	    if(True):
		 count=0
		 for lep in electrons :
		    Ele_EtaSC.append(lep.deltaEtaSC + lep.eta)
		    if(len(Jet_dR_Ljet_Isoel)==len(Jet_dR_Ljet_AntiIsoel) and lep.pt>pt_Thes_el[self.datayear] and abs(lep.eta)<2.1 and lep.cutBased>=1 and (abs(Ele_EtaSC[count])<1.4442 or abs(Ele_EtaSC[count])>1.5660) and ((abs(Ele_EtaSC[count])<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(Ele_EtaSC[count])> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
			el4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			el4v = lep.p4()
			for jet in jets:
			    jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			    jet4v = jet.p4()
			    if(lep.cutBased==4):
				Jet_dR_Ljet_Isoel.append(el4v.DeltaR(jet4v)) 
			    if(lep.cutBased!=4 and lep.cutBased>=1):
				Jet_dR_Ljet_AntiIsoel.append(el4v.DeltaR(jet4v))


		    count=count+1
		 self.out.fillBranch("Electron_EtaSC", Ele_EtaSC)
	    self.out.fillBranch("Jet_dR_Ljet_Isoel",Jet_dR_Ljet_Isoel)
	    self.out.fillBranch("Jet_dR_Ljet_AntiIsoel",Jet_dR_Ljet_AntiIsoel)
	    #print "Ele_EtaSC = ", Ele_EtaSC
	    #print "Jet_dR_Ljet_Isoel = " , Jet_dR_Ljet_Isoel
	    #print "Jet_dR_Ljet_AntiIsoel = ",Jet_dR_Ljet_AntiIsoel
	elif(self.MC == False and self.dataset == "singleMuon"):
	    #print self.dataset
	    Jet_dR_Ljet_Isomu,Jet_dR_Ljet_AntiIsomu = ([]for i in range(2)) 
	    if(True):
		 for lep in muons :
		    if(len(Jet_dR_Ljet_Isomu)==len(Jet_dR_Ljet_AntiIsomu) and lep.pt>pt_Thes_mu[self.datayear] and abs(lep.eta)<2.4 and (lep.pfRelIso04_all<0.06 or lep.pfRelIso04_all>0.2) and lep.tightId==1):
			muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			muon4v = lep.p4()
			for jet in jets:
			    jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
			    jet4v = jet.p4()
			    if(lep.pfRelIso04_all<0.06):
				Jet_dR_Ljet_Isomu.append(muon4v.DeltaR(jet4v))
				#print jet ," ",lep," jetPt = ",jet4v.Pt(), "dr = ",muon4v.DeltaR(jet4v)
			    if(lep.pfRelIso04_all>0.2):
				Jet_dR_Ljet_AntiIsomu.append(muon4v.DeltaR(jet4v))
		    #print 'Muon_SF_Iso = ',Muon_SF_Iso
	    self.out.fillBranch("Jet_dR_Ljet_Isomu",Jet_dR_Ljet_Isomu)
	    self.out.fillBranch("Jet_dR_Ljet_AntiIsomu",Jet_dR_Ljet_AntiIsomu)
	    #print "Jet_dR_Ljet_Isomu = ",Jet_dR_Ljet_Isomu
	    #print "Jet_dR_Ljet_AntiIsomu = ",Jet_dR_Ljet_AntiIsomu
		
        return True


# define modules using the pt_Thes_mu[self.datayear]syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MainModuleConstr_mc_2016 = lambda : MainProducer(True,'2016',None)
MainModuleConstr_data_2016_singleMuon = lambda : MainProducer(False,'2016','singleMuon')
MainModuleConstr_data_2016_singleElectron = lambda : MainProducer(False,'2016','singleElectron')

MainModuleConstr_mc_2017 = lambda : MainProducer(True,'2017',None)
MainModuleConstr_data_2017_singleMuon = lambda : MainProducer(False,'2017','singleMuon')
MainModuleConstr_data_2017_singleElectron = lambda : MainProducer(False,'2017','singleElectron')
