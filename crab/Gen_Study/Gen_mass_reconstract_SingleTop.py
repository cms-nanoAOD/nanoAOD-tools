#!/usr/bin/env python3
import os, sys
import ROOT 
import numpy as np
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *

class NanoGenModule(Module):
    def __init__(self,datayear):
        self.writeHistFile=True
        self.datayear = datayear
    #def beginJob(self,histFile=None,histDirName=None):
    #Module.beginJob(self,histFile,histDirName)
    #self.pt_hist = ROOT.TH1D("pt_hist","pt_hist",20,0.0,400)
    #self.eta_hist = ROOT.TH1D("eta_hist","eta_hist",20,0.0,5.0)
    #self.top_mass_hist = ROOT.TH1D("top_mass","top_mass",52,166.0,179.0)
    #self.addObject(self.pt_hist)
    #self.addObject(self.eta_hist)
    #self.addObject(self.top_mass_hist)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("top_ID","I")
        self.out.branch("top_ID_lastcopy","I")


        self.out.branch("top_is_lastcopy","F")

        self.out.branch("top_PDG_lastcopy","F")
        self.out.branch("top_mass_gen_lastcopy", "F")
        self.out.branch("top_mass_gen", "F")
        self.out.branch("top_mass_gen_reco", "F")

        self.out.branch("top_pt_gen", "F")
        self.out.branch("top_pt_gen_lastcopy", "F")
        self.out.branch("top_pt_gen_reco", "F")

        self.out.branch("top_eta_gen", "F")
        self.out.branch("top_eta_gen_lastcopy", "F")
        self.out.branch("top_eta_gen_reco", "F")

        self.out.branch("top_phi_gen", "F")
        self.out.branch("top_phi_gen_lastcopy", "F")
        self.out.branch("top_phi_gen_reco", "F")

        self.out.branch("tau_to_el_flag", "F")
        self.out.branch("tau_to_mu_flag", "F")
        self.out.branch("el_flag", "F")
        self.out.branch("mu_flag", "F")

        self.out.branch("lepton_ID","I")
        self.out.branch("lepton_pt_gen", "F")
        self.out.branch("lepton_eta_gen", "F")
        self.out.branch("lepton_phi_gen", "F")

        self.out.branch("minidR_dresslep","F")
        self.out.branch("DressLep_pt_gen", "F")
        self.out.branch("DressLep_eta_gen", "F")
        self.out.branch("DressLep_phi_gen", "F")
        self.out.branch("DressLep_mass_gen", "F")
        self.out.branch("DressLep_ID", "I")

        self.out.branch("neutrino_ID","I")
        self.out.branch("neutrino_pt_gen", "F")
        self.out.branch("neutrino_eta_gen", "F")
        self.out.branch("neutrino_phi_gen", "F")
        self.out.branch("neutrino_el_flag", "F")
        self.out.branch("neutrino_mu_flag", "F")

        self.out.branch("W_ID","I")
        self.out.branch("W_mass_gen", "F")
        self.out.branch("W_mass_gen_reco", "F")
        self.out.branch("W_pt_gen", "F")
        self.out.branch("W_pt_gen_reco", "F")
        self.out.branch("W_eta_gen", "F")
        self.out.branch("W_eta_gen_reco", "F")
        self.out.branch("W_phi_gen", "F")
        self.out.branch("W_phi_gen_reco", "F")
        self.out.branch("W_to_el_flag", "F")
        self.out.branch("W_to_mu_flag", "F")

        self.out.branch("bjet_ID","I")
        self.out.branch("bjet_pt_gen", "F")
        self.out.branch("bjet_eta_gen", "F")
        self.out.branch("bjet_phi_gen", "F")
        self.out.branch("bjet_mass_gen", "F")

        self.out.branch("bpart_ID","I")
        self.out.branch("bpart_pt_gen", "F")
        self.out.branch("bpart_eta_gen", "F")
        self.out.branch("bpart_phi_gen", "F")
        self.out.branch("minDR_bpart_bjet","F")
        self.out.branch("DR_dresslepton_bjet","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        Genparts = Collection(event,"GenPart")
        GenJets = Collection(event,"GenJet")
        GenDressedLeptons = Collection(event,"GenDressedLepton")
        top_from_bquark = []
        top_from_lepton = []
        top_from_nuetrino = []
        b_quark_id = None
        lepton_id = None
        nuetrino_id = None
        tau_to_el_flag = False
        tau_to_mu_flag = False
        el_flag = False
        mu_flag = False
        neutrino_el_flag = False
        neutrino_mu_flag = False

        lepton4v_gen = ROOT.TLorentzVector()
        Nu4v_gen = ROOT.TLorentzVector()
        bPart4v_gen = ROOT.TLorentzVector()
        bjet4v_gen = ROOT.TLorentzVector()
        w4v_gen_reco = ROOT.TLorentzVector()
        top4v_gen_reco = ROOT.TLorentzVector()
        bjet4v_gen_temp = ROOT.TLorentzVector()
        GenDressedLepton_gen = ROOT.TLorentzVector()
        GenDressedLepton_gen_temp = ROOT.TLorentzVector()

        genpartID = -1
        for genpart in Genparts:
            genpartID = genpartID+1
            if((abs(genpart.pdgId)==11 or abs(genpart.pdgId)==13) or abs(genpart.pdgId)==5 or (abs(genpart.pdgId)==12 or abs(genpart.pdgId)==14)):
                motheridx =  genpart.genPartIdxMother
                PDG = genpart.pdgId
                final_state_GenPart_Flag = Binary_flags(genpart.statusFlags)
                motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
                if(abs(PDG)==5):
                    bPart4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,genpart.mass)
                    bpart_ID = genpartID
                    bpart_pt_gen = genpart.pt
                    bpart_eta_gen = genpart.eta
                    bpart_phi_gen = genpart.phi

                    minidR = 99
                    JetID = -1
                    # print "------------",minidR,"--------------"
                    for genjet in GenJets:
                        JetID = JetID + 1
                        #print genjet.pt
                        bjet4v_gen_temp.SetPtEtaPhiM(genjet.pt,genjet.eta,genjet.phi,genjet.mass)
                        minidR_temp = bPart4v_gen.DeltaR(bjet4v_gen_temp)
                        #math.sqrt((genpart.eta-genjet.eta)*(genpart.eta-genjet.eta)+(genpart.phi-genjet.phi)*(genpart.phi-genjet.phi)) 
                        if(minidR_temp<minidR):
                                minidR = minidR_temp
                                bjet_pt_gen = genjet.pt
                                bjet_eta_gen = genjet.eta
                                bjet_phi_gen = genjet.phi
                                bjet_mass_gen = genjet.mass
                                bjet4v_gen.SetPtEtaPhiM(bjet_pt_gen,bjet_eta_gen,bjet_phi_gen,bjet_mass_gen)
                                bjet_ID = JetID
                                #bjet4v_gen.Print()
                                #print bpart_ID," ",JetID," ",minidR, "",int(bjet4v_gen.Pt() )
                    #print int(bjet4v_gen.Pt())
                    # bjet4v_gen.Print()
                    if(abs(motherPDG)!=6):
                        while (abs(GmotherPDG)!=6):
                            if(motherPDG == GmotherPDG or GmotherPDG ==-1 or motherPDG ==-1 or Gmotheridx==-1): # motherPDG == GmotherPDG this can make sure that we this is the case then we will find the Gmother again in gen part loop
                                #print("break while loop @ motherPDG = %s, GmotherPDG = %s Gmotheridx = %s" % (motherPDG, GmotherPDG,Gmotheridx))
                                break
                            PDG = motherPDG
                            motheridx = Gmotheridx
                            motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts)
                            #print abs(GmotherPDG)," ---> ",
                            #print("-----> ",motherPDG,Gmotheridx,GmotherPDG)
                    ## ----- it is possible the b quark (5) ahs it mother as top (6)
                    if(abs(motherPDG)==6):
                        #print abs(motherPDG)," --> ",
                        top_from_bquark.append(motheridx)
                        flag_for_b = final_state_GenPart_Flag
                    elif(abs(motherPDG)==abs(PDG) and abs(GmotherPDG)==6 and len(top_from_bquark)!=0):
                        #print abs(GmotherPDG)," ---> ",
                        if(top_from_bquark[0]!=abs(Gmotheridx)):
                            top_from_bquark.append(Gmotheridx)
                            flag_for_b = final_state_GenPart_Flag
                        #print "Gmother is top ; len(top_from_bquark) was !=0"
                    elif(abs(motherPDG)==abs(PDG) and abs(GmotherPDG)==6 and len(top_from_bquark)==0):
                        #print abs(GmotherPDG)," ----> ",
                        top_from_bquark.append(Gmotheridx)
                        flag_for_b = final_state_GenPart_Flag
                        #print "top_from_bquark : ",top_from_bquark
                elif((abs(PDG)==11 or abs(PDG)==13) and (isflagTrue(final_state_GenPart_Flag,"fromHardProcess")==True or isflagTrue(final_state_GenPart_Flag,"isDirectHardProcessTauDecayProduct")==True)):
                    lepton_ID = genpartID
                    lepton_pt_gen = genpart.pt
                    lepton_eta_gen = genpart.eta
                    lepton_phi_gen = genpart.phi
                    if(abs(PDG)==13): 
                        lepton4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.1056583745)
                        GenDressedLeptonsID = -1
                        minidR_dresslep = 999
                        for GenDressedLepton in GenDressedLeptons:
                            GenDressedLeptonID = GenDressedLeptonsID + 1
                            if(abs(GenDressedLepton.pdgId) ==13):GenDressedLepton_gen_temp.SetPtEtaPhiM(GenDressedLepton.pt,GenDressedLepton.eta,GenDressedLepton.phi,GenDressedLepton.mass)
                            else: continue
                            minidR_dresslep_temp = lepton4v_gen.DeltaR(GenDressedLepton_gen_temp)
                            
                            if(minidR_dresslep_temp<minidR_dresslep):
                                minidR_dresslep = minidR_dresslep_temp
                                DressLep_pt_gen = GenDressedLepton.pt
                                DressLep_eta_gen = GenDressedLepton.eta
                                DressLep_phi_gen = GenDressedLepton.phi
                                DressLep_mass_gen = GenDressedLepton.mass
                                GenDressedLepton_gen.SetPtEtaPhiM(DressLep_pt_gen,DressLep_eta_gen,DressLep_phi_gen,DressLep_mass_gen)# = GenDressedLepton_gen_temp
                                DressLep_ID =  GenDressedLeptonID
                        if(minidR_dresslep==999):
                                DressLep_pt_gen = DressLep_eta_gen = DressLep_phi_gen = DressLep_mass_gen = -99
                                DressLep_ID = -1
                        mu_flag = True
                    if(abs(PDG)==11): 
                        lepton4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.0005109989461)
                        GenDressedLeptonsID = -1
                        minidR_dresslep = 999
                        for GenDressedLepton in GenDressedLeptons:
                            GenDressedLeptonID = GenDressedLeptonsID + 1
                            if(abs(GenDressedLepton.pdgId) ==11): GenDressedLepton_gen_temp.SetPtEtaPhiM(GenDressedLepton.pt,GenDressedLepton.eta,GenDressedLepton.phi,GenDressedLepton.mass)
                            else: continue
                            minidR_dresslep_temp = lepton4v_gen.DeltaR(GenDressedLepton_gen_temp)
                            
                            if(minidR_dresslep_temp<minidR_dresslep):
                                minidR_dresslep = minidR_dresslep_temp
                                DressLep_pt_gen = GenDressedLepton.pt
                                DressLep_eta_gen = GenDressedLepton.eta
                                DressLep_phi_gen = GenDressedLepton.phi
                                DressLep_mass_gen = GenDressedLepton.mass
                                GenDressedLepton_gen.SetPtEtaPhiM(DressLep_pt_gen,DressLep_eta_gen,DressLep_phi_gen,DressLep_mass_gen)# = GenDressedLepton_gen_temp
                                DressLep_ID =  GenDressedLeptonID
                        if(minidR_dresslep==999):
                                DressLep_pt_gen = DressLep_eta_gen = DressLep_phi_gen = DressLep_mass_gen = -99
                                DressLep_ID = -1
                        el_flag = True
                    if( abs(motherPDG)==24 or abs(motherPDG)==11 or abs(motherPDG)==13 or abs(motherPDG)==15):
                        while ((motherPDG == GmotherPDG and GmotherPDG !=-1 and motherPDG !=-1 and Gmotheridx!=-1 and abs(GmotherPDG)!=6) or ( (abs(motherPDG)==24 or abs(motherPDG)==15) and abs(GmotherPDG)!=6 and GmotherPDG !=-1)):
                            if(abs(motherPDG)==15 and abs(PDG)==11 ): tau_to_el_flag = True
                            if(abs(motherPDG)==15 and abs(PDG)==13 ): tau_to_mu_flag = True
                            PDG = motherPDG
                            motheridx = Gmotheridx
                            motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts)
                        ## ---- it is not posible to be top as mother because in case of lepton we find w(24) as mother atleast and top(6) as Grandmother 
                        if(abs(GmotherPDG)==6): # we dont want to add the top quarks which give lepton in final state which leptons mother is not W boson
                            top_from_lepton.append(Gmotheridx)
                            #print "top_from_lepton : ",top_from_lepton
                elif((abs(PDG)==12 or abs(PDG)==14) and (isflagTrue(final_state_GenPart_Flag,"fromHardProcess")==True or isflagTrue(final_state_GenPart_Flag,"isDirectHardProcessTauDecayProduct")==True)):
                    neutrino_ID = genpartID
                    Nu4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.0)
                    neutrino_pt_gen = genpart.pt
                    neutrino_eta_gen = genpart.eta
                    neutrino_phi_gen = genpart.phi
                    neutrino_el_flag = True if(abs(PDG)==12)  else False
                    neutrino_mu_flag = True if(abs(PDG)==14)  else False

                    if( abs(motherPDG)==24  or abs(motherPDG)==15):
                        while ((motherPDG == GmotherPDG and GmotherPDG !=-1 and motherPDG !=-1 and Gmotheridx!=-1 and abs(GmotherPDG)!=6) or ( (abs(motherPDG)==24 or abs(motherPDG)==15) and abs(GmotherPDG)!=6 and GmotherPDG !=-1)):
                             PDG = motherPDG
                             motheridx = Gmotheridx
                             motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts) 
                        ## ---- it is not posible to be top as mother because in case of lepton we find w(24) as mother atleast and top(6) as Grandmother 
                        if(abs(GmotherPDG)==6): #we dont want to add the top quarks which give lepton in final state which leptons mother is not W boson
                             top_from_nuetrino.append(Gmotheridx)

            if abs(genpart.pdgId) == 6:
                if (((genpart.statusFlags >> 13) & 0x1) > 0): # is last copy
                    self.out.fillBranch("top_PDG_lastcopy",genpart.pdgId)
                    self.out.fillBranch("top_mass_gen_lastcopy", genpart.mass)
                    self.out.fillBranch("top_pt_gen_lastcopy", genpart.pt)
                    self.out.fillBranch("top_eta_gen_lastcopy", genpart.eta)
                    self.out.fillBranch("top_ID_lastcopy", genpartID)
                    self.out.fillBranch("top_phi_gen_lastcopy", genpart.phi)

        if(len(top_from_lepton)==1 and len(top_from_bquark)==1):
            if(top_from_lepton[0]==top_from_bquark[0] and top_from_lepton[0]==top_from_nuetrino[0]):
                w4v_gen_reco = GenDressedLepton_gen + Nu4v_gen         
                top4v_gen_reco = w4v_gen_reco + bjet4v_gen

                #print int(GenDressedLepton_gen.Pt()), " ",int(lepton_pt_gen)," ",int(Nu4v_gen.Pt()), " ", int(bpart_pt_gen)," ",int(bjet4v_gen.Pt())," ",bpart_ID," ",bjet_ID
                self.out.fillBranch("W_mass_gen_reco", w4v_gen_reco.M())
                self.out.fillBranch("W_pt_gen_reco", w4v_gen_reco.Pt())
                self.out.fillBranch("W_eta_gen_reco", w4v_gen_reco.Eta())
                self.out.fillBranch("W_phi_gen_reco", w4v_gen_reco.Phi())

                self.out.fillBranch("top_mass_gen_reco", top4v_gen_reco.M())
                self.out.fillBranch("top_pt_gen_reco", top4v_gen_reco.Pt())
                self.out.fillBranch("top_eta_gen_reco", top4v_gen_reco.Eta())
                self.out.fillBranch("top_phi_gen_reco", top4v_gen_reco.Phi())

                
                ID = -1
                for genpart in Genparts:
                    ID +=1
                    if(abs(genpart.pdgId)==24 and abs(genpart.genPartIdxMother)==top_from_lepton[0] ):
                        #print "----->", ID, " ", genpart.pdgId, " ", genpart.genPartIdxMother," ", top_from_lepton[0]
                        #print "-----> stored ",genpart.pdgId  
                        self.out.fillBranch("W_mass_gen", genpart.mass)
                        self.out.fillBranch("W_pt_gen", genpart.pt)
                        self.out.fillBranch("W_eta_gen", genpart.eta)
                        self.out.fillBranch("W_phi_gen", genpart.phi)
                        self.out.fillBranch("W_ID", ID)
                        break 
                ID=-1
                for genpart in Genparts:
                    ID +=1
                    if(ID==top_from_lepton[0]):
                        #print genpart.statusFlags
                        #PrintTrueflags(Binary_flags(genpart.statusFlags))
                        if(tau_to_el_flag):self.out.fillBranch("tau_to_el_flag", 1.0)
                        else:self.out.fillBranch("tau_to_el_flag", 0.0)
                        if(tau_to_mu_flag):self.out.fillBranch("tau_to_mu_flag", 1.0)
                        else:self.out.fillBranch("tau_to_mu_flag", 0.0)
                        if(el_flag):self.out.fillBranch("el_flag", 1.0)
                        else:self.out.fillBranch("el_flag", 0.0)
                        if(mu_flag):self.out.fillBranch("mu_flag", 1.0)
                        else:self.out.fillBranch("mu_flag", 0.0)
                        self.out.fillBranch("top_is_lastcopy", isflagTrue(Binary_flags(genpart.statusFlags),"isLastCopy"))
                        self.out.fillBranch("top_mass_gen", genpart.mass)
                        self.out.fillBranch("top_pt_gen", genpart.pt)
                        self.out.fillBranch("top_eta_gen", genpart.eta)
                        self.out.fillBranch("top_phi_gen", genpart.phi)
                        self.out.fillBranch("top_ID", ID)
                        

                        self.out.fillBranch("neutrino_pt_gen",neutrino_pt_gen)
                        self.out.fillBranch("neutrino_eta_gen",neutrino_eta_gen)
                        self.out.fillBranch("neutrino_phi_gen",neutrino_phi_gen)
                        self.out.fillBranch("neutrino_el_flag", neutrino_el_flag)
                        self.out.fillBranch("neutrino_mu_flag", neutrino_mu_flag)
                        self.out.fillBranch("neutrino_ID", neutrino_ID)

                        self.out.fillBranch("lepton_pt_gen", lepton_pt_gen)
                        self.out.fillBranch("lepton_eta_gen",  lepton_eta_gen)
                        self.out.fillBranch("lepton_phi_gen", lepton_phi_gen)
                        self.out.fillBranch("lepton_ID", lepton_ID)

                        self.out.fillBranch("minidR_dresslep",minidR_dresslep)
                        self.out.fillBranch("DressLep_pt_gen", DressLep_pt_gen)
                        self.out.fillBranch("DressLep_eta_gen", DressLep_eta_gen)
                        self.out.fillBranch("DressLep_phi_gen", DressLep_phi_gen)
                        self.out.fillBranch("DressLep_mass_gen", DressLep_mass_gen)
                        self.out.fillBranch("DressLep_ID", DressLep_ID)

                        self.out.fillBranch("bjet_pt_gen", bjet_pt_gen)
                        self.out.fillBranch("bjet_eta_gen", bjet_eta_gen)
                        self.out.fillBranch("bjet_phi_gen", bjet_phi_gen)
                        self.out.fillBranch("bjet_mass_gen",bjet_mass_gen)
                        self.out.fillBranch("bjet_ID",bjet_ID)
                        self.out.fillBranch("DR_dresslepton_bjet",GenDressedLepton_gen.DeltaR(bjet4v_gen))

                        self.out.fillBranch("bpart_pt_gen", bpart_pt_gen)
                        self.out.fillBranch("bpart_eta_gen",bpart_eta_gen)
                        self.out.fillBranch("bpart_phi_gen",bpart_phi_gen)
                        self.out.fillBranch("bpart_ID",bpart_ID)
                        self.out.fillBranch("minDR_bpart_bjet",minidR)
                        break
            else:
                #print "top_from_lepton : ",top_from_lepton," top_from_bquark : ",top_from_bquark," top_from_nuetrino : ",top_from_nuetrino

                self.out.fillBranch("W_mass_gen", -1000)
                self.out.fillBranch("W_pt_gen",-1000)
                self.out.fillBranch("W_eta_gen", -1000)
                self.out.fillBranch("W_phi_gen", -10000)

                self.out.fillBranch("tau_to_el_flag", -2.0)
                self.out.fillBranch("tau_to_mu_flag", -2.0)
                self.out.fillBranch("el_flag", -2.0)
                self.out.fillBranch("mu_flag", -2.0)

                self.out.fillBranch("W_mass_gen_reco", -1000)
                self.out.fillBranch("W_pt_gen_reco",-1000)
                self.out.fillBranch("W_eta_gen_reco", -1000)
                self.out.fillBranch("W_phi_gen_reco", -10000)

                self.out.fillBranch("top_mass_gen", -1000)
                self.out.fillBranch("top_pt_gen", -1000)
                self.out.fillBranch("top_eta_gen", -1000)
                self.out.fillBranch("top_phi_gen", -1000)
                self.out.fillBranch("top_mass_gen_reco", -1000)
                self.out.fillBranch("top_pt_gen_reco", -1000)
                self.out.fillBranch("top_eta_gen_reco", -1000)
                self.out.fillBranch("top_phi_gen_reco", -1000)

                self.out.fillBranch("neutrino_pt_gen",-1000)
                self.out.fillBranch("neutrino_eta_gen",-1000)
                self.out.fillBranch("neutrino_phi_gen",-1000)

                self.out.fillBranch("lepton_pt_gen",  -1000)
                self.out.fillBranch("lepton_eta_gen",  -1000)
                self.out.fillBranch("lepton_phi_gen", -1000)

                self.out.fillBranch("minidR_dresslep",-1000)
                self.out.fillBranch("DressLep_pt_gen", -1000)
                self.out.fillBranch("DressLep_eta_gen", -1000)
                self.out.fillBranch("DressLep_phi_gen", -1000)
                self.out.fillBranch("DressLep_mass_gen", -1000)
                self.out.fillBranch("DressLep_ID", -1000)


                self.out.fillBranch("bjet_pt_gen", -1000)
                self.out.fillBranch("bjet_eta_gen", -1000)
                self.out.fillBranch("bjet_phi_gen", -1000)
                self.out.fillBranch("bjet_mass_gen",-1000)
                self.out.fillBranch("DR_dresslepton_bjet",-1000)

                self.out.fillBranch("bpart_pt_gen", -1000)
                self.out.fillBranch("bpart_eta_gen",-1000)
                self.out.fillBranch("bpart_phi_gen",-1000)
                self.out.fillBranch("minDR_bpart_bjet",-1000)
        else:
            self.out.fillBranch("W_mass_gen_reco", -999)
            self.out.fillBranch("W_pt_gen_reco",-999)
            self.out.fillBranch("W_eta_gen_reco", -999)
            self.out.fillBranch("W_phi_gen_reco", -999)
               
            self.out.fillBranch("W_mass_gen", -999)
            self.out.fillBranch("W_pt_gen",-999)
            self.out.fillBranch("W_eta_gen", -999)
            self.out.fillBranch("W_phi_gen", -999)

            self.out.fillBranch("tau_to_el_flag", -1.0)
            self.out.fillBranch("tau_to_mu_flag", -1.0)
            self.out.fillBranch("top_mass_gen", -999)
            self.out.fillBranch("top_pt_gen", -999)
            self.out.fillBranch("top_eta_gen", -999)
            self.out.fillBranch("top_phi_gen", -999)
            self.out.fillBranch("top_mass_gen_reco", -999)
            self.out.fillBranch("top_pt_gen_reco", -999)
            self.out.fillBranch("top_eta_gen_reco", -999)
            self.out.fillBranch("top_phi_gen_reco", -999)

            self.out.fillBranch("neutrino_pt_gen",-999)
            self.out.fillBranch("neutrino_eta_gen",-999)
            self.out.fillBranch("neutrino_phi_gen",-999)
           
            self.out.fillBranch("lepton_pt_gen",  -999)
            self.out.fillBranch("lepton_eta_gen",  -999)
            self.out.fillBranch("lepton_phi_gen", -999)

            self.out.fillBranch("minidR_dresslep",-999)
            self.out.fillBranch("DressLep_pt_gen", -999)
            self.out.fillBranch("DressLep_eta_gen", -999)
            self.out.fillBranch("DressLep_phi_gen", -999)
            self.out.fillBranch("DressLep_mass_gen", -999)
            self.out.fillBranch("DressLep_ID", -999)


            self.out.fillBranch("bjet_pt_gen", -999)
            self.out.fillBranch("bjet_eta_gen", -999)
            self.out.fillBranch("bjet_phi_gen", -999)
            self.out.fillBranch("bjet_mass_gen",-999)
            self.out.fillBranch("DR_dresslepton_bjet",-1000)

            self.out.fillBranch("bpart_pt_gen", -999)
            self.out.fillBranch("bpart_eta_gen",-999)
            self.out.fillBranch("bpart_phi_gen",-999)
            self.out.fillBranch("minDR_bpart_bjet",-999)
        del lepton4v_gen
        del Nu4v_gen
        del bPart4v_gen
        del bjet4v_gen
        del w4v_gen_reco
        del top4v_gen_reco
        del bjet4v_gen_temp
        del GenDressedLepton_gen
        del GenDressedLepton_gen_temp
        return True

NanoGenConstr_UL2016_Alt_mass = lambda : NanoGenModule('UL2016')
NanoGenConstr_UL2016_Alt_width = lambda : NanoGenModule('UL2016')
