import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class MainProducer(Module):
    def __init__(self,MC,datayear,dataset):
        self.MC = MC
	#print self.MC
        self.datayear = datayear
        self.dataset = dataset
        if(self.MC==True):self.dataset = None
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if(self.MC): 
             print("self.MC = ",self.MC)
        if(self.dataset != "singleMuon"):
            self.out.branch("Electron_EtaSC",  "F",lenVar="nElectron")
        self.out.branch("Jet_dR_Ljet_Isomu",  "F",lenVar="100")
        self.out.branch("Jet_dR_Ljet_AntiIsomu",  "F",lenVar="101")
        self.out.branch("Jet_dR_Ljet_Isoel",  "F",lenVar="102")
        self.out.branch("Jet_dR_Ljet_AntiIsoel",  "F",lenVar="103")


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
                '2018' : None,
	        'UL2016preVFP' : 26,
	        'UL2016postVFP' : 26,
                'UL2017' : 30,
                'UL2018' : 26}

        pt_Thes_el={
                '2016' : 35,
                '2017' : 37,
                '2018' : None,
	        'UL2016preVFP' : 35,
                'UL2016postVFP' : 35,
                'UL2017' : 35,
                'UL2018' : 35}
        eta_Thes_el={
                '2016' : 2.1,
                '2017' : 2.1,
                '2018' : None,
	        'UL2016preVFP' : 2.1,
                'UL2016postVFP' : 2.1,
                'UL2017' : 2.4,
                'UL2018' : 2.4}

        if(self.MC):
            Ele_EtaSC = [] 
            Jet_dR_Ljet_Isomu,Jet_dR_Ljet_AntiIsomu,Jet_dR_Ljet_Isoel,Jet_dR_Ljet_AntiIsoel = ([]for i in range(4))
            if(True):
                 count=0
                 Jetpt = getattr(event,'Jet_pt')
                 jetpt = Jetpt[0]
                 for lep in electrons :
                    #print "elPt : ",lep.pt, "elSCEta : ",lep.deltaEtaSC + lep.eta
                    Ele_EtaSC.append(lep.deltaEtaSC + lep.eta)
                    if((len(Jet_dR_Ljet_Isoel)==0 or len(Jet_dR_Ljet_AntiIsoel)==0) and lep.pt>pt_Thes_el[self.datayear] and abs(lep.eta)<eta_Thes_el[self.datayear] and lep.cutBased>=1 and (abs(Ele_EtaSC[count])<1.4442 or abs(Ele_EtaSC[count])>1.5660) and ((abs(Ele_EtaSC[count])<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(Ele_EtaSC[count])> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
                        el4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                        el4v = lep.p4()
                        #print "el pt =",el4v.Pt()
                        #for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetId!=0), jets):
                        #if(len(Jet_dR_Ljet_Isoel)==len(Jet_dR_Ljet_AntiIsoel)): #this condiation make sure that len(dR)=len(jets) and dr information is saved for only one leptop and if the second leption is found then dr info is skiped because any way we rejet those event which has two tight lepton in cut strings for mimitr
                        for jet in jets:
                            jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                            jet4v = jet.p4()
                            if(lep.cutBased==4 and len(Jet_dR_Ljet_Isoel)!=len(jets)):
                                Jet_dR_Ljet_Isoel.append(el4v.DeltaR(jet4v))
                            if(lep.cutBased!=4 and lep.cutBased>=1 and len(Jet_dR_Ljet_AntiIsoel)!=len(jets)):
                                Jet_dR_Ljet_AntiIsoel.append(el4v.DeltaR(jet4v))
                   
                                
                    count=count+1
	 	 #print 'elSF_Iso=',Electron_SF_Iso
	 	 #print "Antijet dr =", Jet_dR_Ljet_AntiIsoel
                 self.out.fillBranch("Electron_EtaSC", Ele_EtaSC)
            self.out.fillBranch("Jet_dR_Ljet_Isoel",Jet_dR_Ljet_Isoel)
            self.out.fillBranch("Jet_dR_Ljet_AntiIsoel",Jet_dR_Ljet_AntiIsoel)
            if(True):
                #print "--------------------------"
                for lep in muons :
                    #if(lep.pt<=5):print lep.pt
                    #print lep.pt
	 	    #print "muPt : ",lep.pt, "muEta : ", lep.eta
                    if((len(Jet_dR_Ljet_Isomu)==0 or len(Jet_dR_Ljet_AntiIsomu)==0) and lep.pt>pt_Thes_mu[self.datayear] and abs(lep.eta)<2.4 and (lep.pfRelIso04_all<0.06 or lep.pfRelIso04_all>0.2) and lep.tightId==1):
                        muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                        muon4v = lep.p4()
                        #for jet in filter(lambda j:(j.pt>40 and abs(j.eta)<4.7 and j.jetId!=0), jets):
                        for jet in jets:
                            jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                            jet4v = jet.p4()
                            if(lep.pfRelIso04_all<0.06 and len(Jet_dR_Ljet_Isomu)!=len(jets)):
                                Jet_dR_Ljet_Isomu.append(muon4v.DeltaR(jet4v))
                                #print jet ," ",lep," jetPt = ",jet4v.Pt(), "dr = ",muon4v.DeltaR(jet4v)
                            if(lep.pfRelIso04_all>0.2 and len(Jet_dR_Ljet_AntiIsomu)!=len(jets)):
                                Jet_dR_Ljet_AntiIsomu.append(muon4v.DeltaR(jet4v))
                                #Jet_dR_Ljet_Isomu.append(999.0)
                                #print "Muon Pt =%s ; Muon eta =%s ; muon tight ID =%s ; pfRelIso =%s ; Jet_dR_Ljet_Isomu =%s Jet_dR_Ljet_AntiIsomu =%s" % (lep.pt,lep.eta,lep.tightId,lep.pfRelIso04_all,Jet_dR_Ljet_Isomu,Jet_dR_Ljet_AntiIsomu)
                    #print 'Muon_SF_Iso = ',Muon_SF_Iso
                    #if(len(Jet_dR_Ljet_Isomu)!=0 and len(Jet_dR_Ljet_AntiIsomu)!=0):
                    #print getattr(event,'event')  
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
                    if((len(Jet_dR_Ljet_Isoel)==0 or len(Jet_dR_Ljet_AntiIsoel)==0) and lep.pt>pt_Thes_el[self.datayear] and abs(lep.eta)<eta_Thes_el[self.datayear] and lep.cutBased>=1 and (abs(Ele_EtaSC[count])<1.4442 or abs(Ele_EtaSC[count])>1.5660) and ((abs(Ele_EtaSC[count])<=1.479 and abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05) or (abs(Ele_EtaSC[count])> 1.479 and abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10))):
                        el4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                        el4v = lep.p4()
                        for jet in jets:
                            jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                            jet4v = jet.p4()
                            if(lep.cutBased==4 and len(Jet_dR_Ljet_Isoel)!=len(jets)):
                                Jet_dR_Ljet_Isoel.append(el4v.DeltaR(jet4v)) 
                            if(lep.cutBased!=4 and lep.cutBased>=1 and len(Jet_dR_Ljet_AntiIsoel)!=len(jets)):
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
                    if((len(Jet_dR_Ljet_Isomu)==0 or len(Jet_dR_Ljet_AntiIsomu)==0) and lep.pt>pt_Thes_mu[self.datayear] and abs(lep.eta)<2.4 and (lep.pfRelIso04_all<0.06 or lep.pfRelIso04_all>0.2) and lep.tightId==1):
                        muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                        muon4v = lep.p4()
                        for jet in jets:
                            jet4v = ROOT.TLorentzVector(0.,0.,0.,0.)
                            jet4v = jet.p4()
                            if(lep.pfRelIso04_all<0.06 and len(Jet_dR_Ljet_Isomu)!=len(jets)):
                                Jet_dR_Ljet_Isomu.append(muon4v.DeltaR(jet4v))
                                #print jet ," ",lep," jetPt = ",jet4v.Pt(), "dr = ",muon4v.DeltaR(jet4v)
                            if(lep.pfRelIso04_all>0.2 and len(Jet_dR_Ljet_AntiIsomu)!=len(jets)):
                                Jet_dR_Ljet_AntiIsomu.append(muon4v.DeltaR(jet4v))
                    #print "Muon Pt =%s ; Muon eta =%s ; muon tight ID =%s ; pfRelIso =%s ; Jet_dR_Ljet_Isomu =%s Jet_dR_Ljet_AntiIsomu =%s" % (lep.pt,lep.eta,lep.tightId,lep.pfRelIso04_all,Jet_dR_Ljet_Isomu,Jet_dR_Ljet_AntiIsomu)
                    #print 'Muon_SF_Iso = ',Muon_SF_Iso
            self.out.fillBranch("Jet_dR_Ljet_Isomu",Jet_dR_Ljet_Isomu)
            self.out.fillBranch("Jet_dR_Ljet_AntiIsomu",Jet_dR_Ljet_AntiIsomu)
            #print "Jet_dR_Ljet_Isomu = ",Jet_dR_Ljet_Isomu
            #print "Jet_dR_Ljet_AntiIsomu = ",Jet_dR_Ljet_AntiIsomu
	 	
        return True


# define modules using the pt_Thes_mu[self.datayear]syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MainModuleConstr_mc_UL2016preVFP = lambda : MainProducer(True,'UL2016preVFP',None)
MainModuleConstr_mc_UL2016postVFP = lambda : MainProducer(True,'UL2016postVFP',None)

MainModuleConstr_data_UL2016preVFP_singleMuon = lambda : MainProducer(False,'UL2016preVFP','singleMuon')
MainModuleConstr_data_UL2016postVFP_singleMuon = lambda : MainProducer(False,'UL2016postVFP','singleMuon')

MainModuleConstr_data_UL2016preVFP_singleElectron = lambda : MainProducer(False,'UL2016preVFP','singleElectron')
MainModuleConstr_data_UL2016postVFP_singleElectron = lambda : MainProducer(False,'UL2016postVFP','singleElectron')

MainModuleConstr_mc_UL2017 = lambda : MainProducer(True,'UL2017',None)
MainModuleConstr_data_UL2017_singleMuon = lambda : MainProducer(False,'UL2017','singleMuon')
MainModuleConstr_data_UL2017_singleElectron = lambda : MainProducer(False,'UL2017','singleElectron')

MainModuleConstr_mc_UL2018 = lambda : MainProducer(True,'UL2018',None)
MainModuleConstr_data_UL2018_singleMuon = lambda : MainProducer(False,'UL2018','singleMuon')
MainModuleConstr_data_UL2018_singleElectron = lambda : MainProducer(False,'UL2018','singleElectron')
