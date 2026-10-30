#!/usr/bin/env python3
import os, sys

def PrintTrueflags(flags):
	trueflags = []
	for key in flags.keys():
		if(flags[key]==True):
			print(key ,":",)#flags[key])
	print()

def isflagTrue(flags,spesific_flag):
	trueflags = []
	return_flag = False
	for key in flags.keys():
		if(flags[key]==True and key == spesific_flag):
			return_flag = True
	return return_flag	 
                
def Binary_flags(n):
	Raw_binaryNum = list(map(int, str(bin(n))[2:]))
	binaryNum = []
	if len(Raw_binaryNum)<15:
		for i in range(0,15-len(Raw_binaryNum)):
			binaryNum.append(0)
		
	binaryNum = binaryNum + list(map(int, str(bin(n))[2:]))
	flags = {
		"isPrompt": bool(binaryNum[len(binaryNum)-1-0]),
		"isDecayedLeptonHadron": bool(binaryNum[len(binaryNum)-1-1]),
		"isTauDecayProduct": bool(binaryNum[len(binaryNum)-1-2]),
		"isPromptTauDecayProduct": bool(binaryNum[len(binaryNum)-1-3]),
		"isDirectTauDecayProduct": bool(binaryNum[len(binaryNum)-1-4]),
		"isDirectPromptTauDecayProduct": bool(binaryNum[len(binaryNum)-1-5]),
		"isDirectHadronDecayProduct": bool(binaryNum[len(binaryNum)-1-6]),
		"isHardProcess": bool(binaryNum[len(binaryNum)-1-7]),
		"fromHardProcess": bool(binaryNum[len(binaryNum)-1-8]),
		"isHardProcessTauDecayProduct": bool(binaryNum[len(binaryNum)-1-9]),
		"isDirectHardProcessTauDecayProduct": bool(binaryNum[len(binaryNum)-1-10]),
		"fromHardProcessBeforeFSR": bool(binaryNum[len(binaryNum)-1-11]),
		"isFirstCopy": bool(binaryNum[len(binaryNum)-1-12]),
		"isLastCopy": bool(binaryNum[len(binaryNum)-1-13]),
		"isLastCopyBeforeFSR": bool(binaryNum[len(binaryNum)-1-14])
	} 
	return flags

def findMother(motheridx,Genparts):
	Gmotheridx = -1
	GmotherPDG = -1
	motherPDG = -1
	ID=0
	for genpart in Genparts:
		if(ID==motheridx):
			motherPDG = genpart.pdgId
			Gmotheridx = genpart.genPartIdxMother
			#print
			GID=0
			for Ggenpart in Genparts:
				if(GID==Gmotheridx):
					GmotherPDG = Ggenpart.pdgId
					#print "------> %s is the mother of : %s : "%(GmotherPDG,genpart.pdgId)
					break
				else: GID = GID+1
			break
		else: ID = ID+1
	
	return motherPDG,Gmotheridx,GmotherPDG

def findDaughter(idx,pdg,Genparts):
	daugher_id = []
	daugher_pdg = []
	first_mother_id = []
	first_mother_pdg = []
	ID = 0
	for Genpart in Genparts: 
		#if(ID==idx or isflagTrue(Binary_flags(Genpart.statusFlags),"fromHardProcess")==False): continue;
		if(ID==idx):  
			ID = ID+1
			continue
		elif(abs(Genpart.pdgId)==11 or abs(Genpart.pdgId)==12 or abs(Genpart.pdgId)==13 or abs(Genpart.pdgId)==14 or abs(Genpart.pdgId)==5):
			motheridx = Genpart.genPartIdxMother
			motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
			first_mother = motherPDG
			if(idx==motheridx and isflagTrue(Binary_flags(Genpart.statusFlags),"isPrompt") and isflagTrue(Binary_flags(Genpart.statusFlags),"fromHardProcess")):
				daugher_id.append(ID)
				daugher_pdg.append(Genpart.pdgId)
				first_mother_pdg.append(first_mother)
			else:
				while(idx!=motheridx and GmotherPDG !=-1):
					PDG = motherPDG
					motheridx = Gmotheridx
					motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
					if(idx==motheridx and isflagTrue(Binary_flags(Genpart.statusFlags),"isPrompt") and isflagTrue(Binary_flags(Genpart.statusFlags),"fromHardProcess")):
						daugher_id.append(ID)
						daugher_pdg.append(Genpart.pdgId)
						first_mother_pdg.append(first_mother)	
	ID = ID+1
	return daugher_id,daugher_pdg,first_mother_pdg
