#!/usr/bin/env python3
import os, sys
import ROOT
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from check import *
class EfficiencyModule(Module):
    def __init__(self,datayear,jetSelection):
        self.jetSel = jetSelection
	self.writeHistFile=True
	self.datayear = datayear
	    
    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
	self.pt_hist = ROOT.TH1D("pt_hist","pt_hist",20,0.0,400)
	self.eta_hist = ROOT.TH1D("eta_hist","eta_hist",20,0.0,5.0)
	self.addObject(self.pt_hist)
	self.addObject(self.eta_hist)
    def analyze(self, event):
	Genparts = Collection(event,"GenPart")
	#for genpart in Genparts:
            #if(abs(genpart.pdgId)==5 and genpart.statusFlags==8449):
            #if(abs(genpart.pdgId)==5 and genpart.statusFlags ==8441):
                #print genpart.statusFlags ,"\t\t", bin(genpart.statusFlags)
                #print "pdg id b quark = ", genpart.pdgId, " statusFlags = ", genpart.statusFlags,":",
                #PrintTrueflags(Binary_flags(genpart.statusFlags))
                #print " "
	#print "   now one by one"
	for genpart in Genparts:
	    #if(abs(genpart.pdgId)==5 and genpart.statusFlags==8449):
	    if(abs(genpart.pdgId)==5 and genpart.statusFlags == 22913):
	    	#print genpart.statusFlags ,"\t\t", bin(genpart.statusFlags)
		#print "pdg id b quark = ", genpart.pdgId, " statusFlags = ", genpart.statusFlags,":", 
		#PrintTrueflags(Binary_flags(genpart.statusFlags))
		#print ""
		#print type( genpart.statusFlags)
	    #if(abs(genpart.genPartIdxMother)==6 or abs(genpart.genPartIdxMother)==9 or abs(genpart.genPartIdxMother)==21):
		motheridx =  genpart.genPartIdxMother
		#print("mother idx = " ,motheridx)
		ID=0
		for genpart2 in Genparts:
		    if(ID==motheridx and abs(genpart2.pdgId)==6): 
			#print "------fileter out-----"
	    		#print genpart.statusFlags ,"\t\t", bin(genpart.statusFlags)
		    	#print "    pdg id mother of b quark ", genpart2.pdgId,  " statusFlags = ", genpart2.statusFlags, ":",
			#PrintTrueflags(Binary_flags(genpart2.statusFlags))
			#print ""
			self.pt_hist.Fill(genpart.pt)
			self.eta_hist.Fill(genpart.eta)
			#motherofmotheridx =  genpart2.genPartIdxMother
			#if(abs(genpart2.pdgId)==5):
			#	ID2=0
			#	for genpart3 in Genparts:
                    	#	     if(ID2==motherofmotheridx):
	    		#			#print genpart.statusFlags ,"\t\t", bin(genpart.statusFlags)
                        #		print "       pdg id of grand mother bquark = ", genpart3.pdgId,  " statusFlags = ", genpart3.statusFlags,":",
			#		PrintTrueflags(Binary_flags(genpart3.statusFlags))
			#		print ""
			#		break
			#	     else: ID2 = ID2+1
                        #		
			break
		    else: ID = ID+1
		#getattr(event,'GenPart_pdfId[]')
	        #print("status = ", genpart.status," ", genpart.statusFlags)
		#for motherid in Genparts:
			#print("mother id = ", genpart.pdgId)    
		    
	#print("-------------------------")			
        return True

EfficiencyConstr_2016 = lambda : EfficiencyModule('2016',jetSelection= lambda j : j.pt > 20)
EfficiencyConstr_2017 = lambda : EfficiencyModule('2017',jetSelection= lambda j : j.pt > 20)

treecut=" Entry$<10 "
#inputFiles=["/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]
inputFiles=[	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tbarchannel_2J1T1_el.root",
		"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]

p=PostProcessor( ".",
                inputFiles,
                #treecut,
                modules=[EfficiencyConstr_2017()],
                outputbranchsel="clean.txt",
                provenance=True,
                fwkJobReport=True,
                jsonInput=runsAndLumis(),
                noOut=False,
                histFileName="b_from_top.root",
                histDirName="Histograms")
p.run()

print "DONE"
