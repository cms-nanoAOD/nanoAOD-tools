#!/usr/bin/env python
import os, sys


def PrintTrueflags(flags):
        trueflags = []
        for key in flags.keys():
            if(flags[key]==True):
            	print key ,":",#flags[key]
	#print "exit"
	

def Binary_flags(n):
    Raw_binaryNum = list(map(int, str(bin(n))[2:]))
    #print Raw_binaryNum
    #print len(Raw_binaryNum)
    binaryNum = []
    if len(Raw_binaryNum)<15:
	for i in range(0,15-len(Raw_binaryNum)):
	    binaryNum.append(0)
    	
    #print len(binaryNum)
    binaryNum = binaryNum + list(map(int, str(bin(n))[2:]))
    #print len(binaryNum)
    #print binaryNum
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
                #print "------> %s flag : %s : "%(genpart.pdgId,genpart.statusFlags),
                #PrintTrueflags(Binary_flags(genpart.statusFlags))
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
 
#PrintTrueflags(Binary_flags(4481))
#PrintTrueflags(Binary_flags(2433))
