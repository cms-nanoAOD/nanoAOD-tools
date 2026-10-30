import ROOT as R
R.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *


import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
#from MainModule import *
import math

R.gInterpreter.ProcessLine('#include "KinFit.C"')


class MainProducer(Module):
    def __init__(self,lepton_flv):
	self.lepton_flv = lepton_flv

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

	self.out.branch("bQurkPt_gen", "F")
	self.out.branch("bQurkEta_gen", "F")
	self.out.branch("bQurkPhi_gen", "F")
	self.out.branch("bQurkMass_gen", "F")

	self.out.branch("topPt_gen", "F")
	self.out.branch("topEta_gen", "F")
        self.out.branch("topPhi_gen", "F")
	self.out.branch("topMass_gen", "F")	


	self.out.branch("MuonPt_gen", "F") 
	self.out.branch("MuonEta_gen", "F")
	self.out.branch("MuonPhi_gen", "F")
	self.out.branch("MuonMass_gen", "F")

	
	self.out.branch("ElectronPt_gen", "F")
        self.out.branch("ElectronEta_gen", "F")
        self.out.branch("ElectronPhi_gen", "F")
        self.out.branch("ElectronMass_gen", "F")	

	self.out.branch("Pt_nu_gen", "F")
	self.out.branch("Eta_nu_gen", "F")
	self.out.branch("Phi_nu_gen", "F")
	self.out.branch("Mass_nu_gen", "F")

	self.out.branch("Px_nu_gen", "F")
	self.out.branch("Py_nu_gen", "F")
	self.out.branch("Pz_nu_gen", "F")
	self.out.branch("Pt_nu","F")

	self.out.branch("mtwMass_gen", "F")


	self.out.branch("bQurkPt_kin", "F")
        self.out.branch("bQurkEta_kin", "F")
        self.out.branch("bQurkPhi_kin", "F")
        self.out.branch("bQurkMass_kin", "F")

        self.out.branch("topPt_kin", "F")
        self.out.branch("topEta_kin", "F")
        self.out.branch("topPhi_kin", "F")
        self.out.branch("topMass_kin", "F")


        self.out.branch("MuonPt_kin", "F")
        self.out.branch("MuonEta_kin", "F")
        self.out.branch("MuonPhi_kin", "F")
        self.out.branch("MuonMass_kin", "F")


        self.out.branch("ElectronPt_kin", "F")
        self.out.branch("ElectronEta_kin", "F")
        self.out.branch("ElectronPhi_kin", "F")
        self.out.branch("ElectronMass_kin", "F")

        self.out.branch("Pt_nu_kin", "F")
        self.out.branch("Eta_nu_kin", "F")
        self.out.branch("Phi_nu_kin", "F")
        self.out.branch("Mass_nu_kin", "F")

        self.out.branch("Px_nu_kin", "F")
        self.out.branch("Py_nu_kin", "F")
        self.out.branch("Pz_nu_kin", "F")

        self.out.branch("mtwMass_kin", "F")

	self.out.branch("findmuon", "F")
	self.out.branch("findelectron", "F")
	self.out.branch("findtau", "F")

	self.out.branch("topMass_fromTau","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
	#print self.lepton_flv
	Genparts = Collection(event,"GenPart")
	#print "total genpart = ",getattr(event,'nGenPart') 
	for genpart in Genparts:
	    if(abs(genpart.pdgId)==5):# find b quark
		motheridx =  genpart.genPartIdxMother #get idx mother of b quark
                ID=0
		for genpart2 in Genparts:
		    if(ID==motheridx and abs(genpart2.pdgId)==6): # check if the idx of mother is belongs top quark
		    	topMass_gen = genpart2.mass 
			#print topMass_gen
                    	self.out.fillBranch("topMass_gen", topMass_gen)
			daugher_id,daugher_pdg,mother_pdg = findDaughter(ID,genpart2.pdgId,Genparts) # get the lepton and b qurks comming from top top
			#if(len(daugher_id)>0):
			#	print "daugher_id :  ", daugher_id
			#	print "daugher_pdg : ", daugher_pdg
			#	print "mother_pdg :  ", mother_pdg
			break
                    else: ID = ID+1

	lepton4v_gen = R.TLorentzVector()
	Nu4v_gen = R.TLorentzVector()
	bJet4v_gen = R.TLorentzVector()
	w4v_gen = R.TLorentzVector()
	top4v_gen = R.TLorentzVector()

	lepton4v_kin = R.TLorentzVector()
        Nu4v_kin = R.TLorentzVector() 
	bJet4v_kin = R.TLorentzVector()
	w4v_kin = R.TLorentzVector()
	top4v_gen = R.TLorentzVector()

	for i in range(0,len(daugher_id)):
	    ID = -1
	    for genpart in Genparts:
		ID = ID+1      	
		if(ID==daugher_id[i]):
			#motheridx = genpart.genPartIdxMother
			#motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
			#print "ID : ",ID," pdg : ",genpart.pdgId," M_ID : ",motheridx," M_pdg : ", motherPDG

			if(abs(daugher_pdg[i])==11 and abs(mother_pdg[i])==24 and self.lepton_flv == 'el'):
				ElectronPt_gen = genpart.pt
				ElectronEta_gen = genpart.eta
				ElectronPhi_gen = genpart.phi
				ElectronMass_gen = 0.0005109989461

				lepton4v_gen.SetPtEtaPhiM(ElectronPt_gen,ElectronEta_gen,ElectronPhi_gen,ElectronMass_gen)			    

				#print "el pdg : ",daugher_pdg[i]," pt : ",genpart.pt," eta : ", genpart.eta," phi : ",genpart.phi," mass : ",ElectronMass_gen

				self.out.fillBranch("ElectronPt_gen", ElectronPt_gen)
				self.out.fillBranch("ElectronEta_gen", ElectronEta_gen)
				self.out.fillBranch("ElectronPhi_gen", ElectronPhi_gen)
				self.out.fillBranch("ElectronMass_gen", ElectronMass_gen)
				self.out.fillBranch("findelectron", 1)
				self.out.fillBranch("findmuon", 0)


			if(abs(daugher_pdg[i])==13 and abs(mother_pdg[i])==24 and self.lepton_flv == 'mu'):
				MuonPt_gen = genpart.pt
				MuonEta_gen = genpart.eta			
				MuonPhi_gen = genpart.phi
				MuonMass_gen = 0.1056583745	
		
				lepton4v_gen.SetPtEtaPhiM(MuonPt_gen,MuonEta_gen,MuonPhi_gen,MuonMass_gen)		        
		
				#print "mu pdg : ",daugher_pdg[i]," pt : ",genpart.pt," eta : ", genpart.eta," phi : ",genpart.phi," mass : ",MuonMass_gen
				#print "mu pdg : ",daugher_pdg[i]," pt : ",Muon4v_gen.Pt()," eta : ", Muon4v_gen.Eta()," phi : ",Muon4v_gen.Phi()," mass : ",Muon4v_gen.M()
				self.out.fillBranch("MuonPt_gen", MuonPt_gen)
				self.out.fillBranch("MuonEta_gen", MuonEta_gen)
				self.out.fillBranch("MuonPhi_gen", MuonPhi_gen)
				self.out.fillBranch("MuonMass_gen", MuonMass_gen)
				self.out.fillBranch("findmuon", 1)
				self.out.fillBranch("findelectron", 0)

			if((abs(daugher_pdg[i])==12 or abs(daugher_pdg[i])==14) and abs(mother_pdg[i])==24):
				Pt_nu_gen = genpart.pt
				Eta_nu_gen = genpart.eta
				Phi_nu_gen = genpart.phi
				Mass_nu_gen = 0.0
				#print "NU pdg : ",daugher_pdg[i]," pt : ",genpart.pt," eta : ", genpart.eta," phi : ",genpart.phi," mass : ",genpart.mass
		
				Nu4v_gen.SetPtEtaPhiM(Pt_nu_gen,Eta_nu_gen,Phi_nu_gen,Mass_nu_gen)	
		
				self.out.fillBranch("Pt_nu_gen", Pt_nu_gen)
				self.out.fillBranch("Eta_nu_gen", Eta_nu_gen)
				self.out.fillBranch("Phi_nu_gen", Phi_nu_gen)
				self.out.fillBranch("Mass_nu_gen", 0.0)
		
				self.out.fillBranch("Px_nu_gen", Nu4v_gen.Px())
				self.out.fillBranch("Py_nu_gen", Nu4v_gen.Py())
				self.out.fillBranch("Pz_nu_gen", Nu4v_gen.Pz())
		
			if(abs(daugher_pdg[i])==5 and abs(mother_pdg[i])==6):
				bQurkPt_gen = genpart.pt
				bQurkEta_gen = genpart.eta
				bQurkPhi_gen = genpart.phi
				bQurkMass_gen = 4.18
				#print "b pdg : ",daugher_pdg[i]," pt : ",genpart.pt," eta : ", genpart.eta," phi : ",genpart.phi," mass : ",genpart.mass
		
				bJet4v_gen.SetPtEtaPhiM(bQurkPt_gen,bQurkEta_gen,bQurkPhi_gen,bQurkMass_gen)		
		
				self.out.fillBranch("bQurkPt_gen", bQurkPt_gen)
				self.out.fillBranch("bQurkEta_gen", bQurkEta_gen)
				self.out.fillBranch("bQurkPhi_gen", bQurkPhi_gen)
				self.out.fillBranch("bQurkMass_gen", bQurkMass_gen)

			
	w4v_gen = lepton4v_gen + Nu4v_gen

	#print "Wmass = ",w4v_gen.M()
	mtwMass_gen = math.sqrt(abs(pow((lepton4v_gen.Pt()+Nu4v_gen.Pt()),2)-pow((lepton4v_gen.Pt()*math.cos(lepton4v_gen.Phi())+Nu4v_gen.Pt()*math.cos(Nu4v_gen.Phi())),2)-pow((lepton4v_gen.Pt()*math.sin(lepton4v_gen.Phi())+Nu4v_gen.Pt()*math.sin( Nu4v_gen.Phi())),2)))

	self.out.fillBranch("mtwMass_gen", mtwMass_gen)

	top4v_gen = w4v_gen + bJet4v_gen

	if(lepton4v_gen.M()==0.0): 
		#print "mu  pt : ",lepton4v_gen.Pt()," eta : ", lepton4v_gen.Eta()," phi : ",lepton4v_gen.Phi()," mass : ",lepton4v_gen.M()
		#print "nu  pt : ",Nu4v_gen.Pt()," eta : ", Nu4v_gen.Eta()," phi : ",Nu4v_gen.Phi()," mass : ",Nu4v_gen.M()
		#print "b   pt : ",bJet4v_gen.Pt()," eta : ", bJet4v_gen.Eta()," phi : ",bJet4v_gen.Phi()," mass : ",bJet4v_gen.M()

		self.out.fillBranch("findtau", 1)	
		self.out.fillBranch("topMass_fromTau", getattr(event,'topMass'))
	else:
		self.out.fillBranch("findtau", 0)
		self.out.fillBranch("topMass_fromTau", 0)	
	#print "top mass = ",top4v_gen.M()
	self.out.fillBranch("topPt_gen", top4v_gen.Pt())
	self.out.fillBranch("topEta_gen", top4v_gen.Eta())
	self.out.fillBranch("topPhi_gen", top4v_gen.Phi())
	self.out.fillBranch("topMass_gen", top4v_gen.M())

	############################################################################# kinfit ###########################################

	#print "begin kinfit ....."
	#Chi2 = 11.


	lep = R.TLorentzVector()
	nu  = R.TLorentzVector()

	if(self.lepton_flv=='mu'):
		lep.SetPtEtaPhiM(getattr(event,'MuonPt'), getattr(event,'MuonEta'), getattr(event,'MuonPhi'), getattr(event,'MuonMass'))
		#print getattr(event,'MuonPt'), getattr(event,'MuonEta'), getattr(event,'MuonPhi'), getattr(event,'MuonMass')
	if(self.lepton_flv=='el'):
                lep.SetPtEtaPhiM(getattr(event,'ElectronPt'), getattr(event,'ElectronEta'), getattr(event,'ElectronPhi'), getattr(event,'ElectronMass'))

        zero_num = 0.000001
	#print getattr(event,'Px_nu'), getattr(event,'Py_nu'), zero_num, zero_num
	nu.SetXYZM(getattr(event,'Px_nu'), getattr(event,'Py_nu'), zero_num, zero_num)


	#print "lep = [",lep.Pt(),",",lep.Eta(),",",lep.Phi(),",",lep.M(),"]"
	#print "nu = [", nu.X(),",", nu.Y(),",", nu.Z(),",", nu.M(),"]"


	#print "Fitting ...."
	new_vec_comp_XYZE = R.PerfomFit(lep,nu)


	lepton4v_kin.SetPxPyPzE(new_vec_comp_XYZE.at(0),new_vec_comp_XYZE.at(1),new_vec_comp_XYZE.at(2),new_vec_comp_XYZE.at(3))
	Nu4v_kin.SetPxPyPzE(new_vec_comp_XYZE.at(4),new_vec_comp_XYZE.at(5),new_vec_comp_XYZE.at(6),new_vec_comp_XYZE.at(7))
	
	#print "lep = [",lepton4v_kin.Pt(),",",lepton4v_kin.Eta(),",",lepton4v_kin.Phi(),",",lepton4v_kin.M(),"]"
	#print "nu = [", Nu4v_kin.X(),",", Nu4v_kin.Y(),",", Nu4v_kin.Z(),",", Nu4v_kin.E(),"]"

	if(self.lepton_flv=='mu'):
		self.out.fillBranch("MuonPt_kin", lepton4v_kin.Pt())
                self.out.fillBranch("MuonEta_kin", lepton4v_kin.Eta())
                self.out.fillBranch("MuonPhi_kin", lepton4v_kin.Phi())
                self.out.fillBranch("MuonMass_kin", lepton4v_kin.M())
	elif(self.lepton_flv=='el'):
		 self.out.fillBranch("ElectronPt_kin", lepton4v_kin.Pt())
                 self.out.fillBranch("ElectronEta_kin", lepton4v_kin.Eta())
                 self.out.fillBranch("ElectronPhi_kin", lepton4v_kin.Phi())
                 self.out.fillBranch("ElectronMass_kin", lepton4v_kin.M())

	self.out.fillBranch("Pt_nu_kin", Nu4v_kin.Pt())
        self.out.fillBranch("Eta_nu_kin", Nu4v_kin.Eta())
        self.out.fillBranch("Phi_nu_kin", Nu4v_kin.Phi())
        self.out.fillBranch("Mass_nu_kin", Nu4v_kin.M())

	self.out.fillBranch("Px_nu_kin", Nu4v_kin.Px())
        self.out.fillBranch("Py_nu_kin", Nu4v_kin.Py())
        self.out.fillBranch("Pz_nu_kin", Nu4v_kin.Pz())


	bJet4v_kin.SetPtEtaPhiM(getattr(event,'bJetPt'),getattr(event,'bJetEta'),getattr(event,'bJetPhi'),getattr(event,'bJetMass'))
        self.out.fillBranch("bQurkPt_kin", bJet4v_kin.Pt())
        self.out.fillBranch("bQurkEta_kin", bJet4v_kin.Eta())
        self.out.fillBranch("bQurkPhi_kin", bJet4v_kin.Phi())
        self.out.fillBranch("bQurkMass_kin", bJet4v_kin.M())

	
	w4v_kin = lepton4v_kin + Nu4v_kin
	
	mtwMass_kin = math.sqrt(abs(pow((lepton4v_kin.Pt()+Nu4v_kin.Pt()),2)-pow((lepton4v_kin.Pt()*math.cos(lepton4v_kin.Phi())+Nu4v_kin.Pt()*math.cos(Nu4v_kin.Phi())),2)-pow((lepton4v_kin.Pt()*math.sin(lepton4v_kin.Phi())+Nu4v_kin.Pt()*math.sin( Nu4v_kin.Phi())),2)))


        self.out.fillBranch("mtwMass_kin", mtwMass_kin)

	
	top4v_kin = w4v_kin + bJet4v_kin

        #print "top mass = ",top4v_gen.M()
	
        self.out.fillBranch("topPt_kin", top4v_kin.Pt())
        self.out.fillBranch("topEta_kin", top4v_kin.Eta())
        self.out.fillBranch("topPhi_kin", top4v_kin.Phi())
        self.out.fillBranch("topMass_kin", top4v_kin.M())

	self.out.fillBranch("Pt_nu", getattr(event,'MET_pt'))
	"""ID2 = 0
	for Genpart in Genparts:
	    motheridx = Genpart.genPartIdxMother
            motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
	    if(abs(motherPDG)==14):
		print Genpart.pdgId, "is dauter of : ",motherPDG
		print ID2," dauther kinematics : pt = ",Genpart.pt," eta = ",Genpart.eta," phi = ",Genpart.phi
	    	ID3 = 0 
	    	for Genpart2 in Genparts:
		    if(ID3==motheridx):
		    	print ID3, " mother kinematics : pt = ",Genpart2.pt," eta = ",Genpart2.eta," phi = ",Genpart2.phi
		    ID3=ID3+1
	    ID2=ID2+1 """
	
	#print "-----------------------------------------------------"
	
        return True


# define modules using the pt_Thes_mu[self.datayear]syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MainModuleConstr_Gen = lambda : MainProducer('mu')

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)"
treecutEN = "Entry$<100"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"

inputFiles=[	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tbarchannel_2J1T1_mu.root"]#,
#		"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]

p=PostProcessor(".",
		inputFiles,
		#treecutEN,
		modules=[MainModuleConstr_Gen()],
		outputbranchsel="clean_All_keep_kin.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
