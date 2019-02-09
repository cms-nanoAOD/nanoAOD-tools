#!/usr/bin/env python
from math import fabs, cos, sqrt
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest, matchObjectCollectionMultiple
from ROOT import TLorentzVector

def deltaPhi(phi1,phi2):
    PHI = fabs(phi1-phi2)
    if (PHI<=3.14159265):
        return PHI
    else:
        return 2*3.14159265-PHI

def getPt(pO):
    return pO.pt

def getpt(pO):
    return pO[0].pt

def bitwiseDecoder(STATUS):
    code={
        "0" : "isPrompt",
        "1" : "isDecayedLeptonHadron",
        "2" : "isTauDecayProduct",
        "3" : "isPromptTauDecayProduct",
        "4" : "isDirectTauDecayProduct",
        "5" : "isDirectPromptTauDecayProduct",
        "6" : "isDirectHadronDecayProduct",
        "7" : "isHardProcess",
        "8" : "fromHardProcess",
        "9" : "isHardProcessTauDecayProduct",
        "10" : "isDirectHardProcessTauDecayProduct",
        "11" : "fromHardProcessBeforeFSR",
        "12" : "isFirstCopy",
        "13" : "isLastCopy",
        "14" : "isLastCopyBeforeFSR",
    }
    state=[]
    for SHIFT in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:

        myBIT = ( int(STATUS) >> int(SHIFT) ) & 0x1
        if myBIT==1:
            state.append(code["%s" %SHIFT])
        #print "myBIT : ", myBIT, "; code : ", code["%s" %SHIFT]
        
    return state

def bitwise(STATUS,BIT):

    myBIT = ( int(STATUS) >> int(BIT) ) & 0x1

    return myBIT

def bitwiseJetId(jetid):

    code={
        "1" : "looseBit",
        "2" : "tightBit"
        }

    jetID=[]
    for SHIFT in [1,2]:
        myBIT = ( int(jetid) >> int(SHIFT) ) & 0x1
        if myBIT==1:
            jetID.append(code["%s" %SHIFT])

    return jetID

def cleanFromlepton(InList,leptonList,dR=0.4):
    for lepton in leptonList:
        for phyobj in InList:
            if deltaR(phyobj,lepton)<dR:
                InList.remove(phyobj)
    InList.sort(key=getPt, reverse=True)

def cleanFromleptonSS(InList,leptonList,dR=0.4):
    for lepton in leptonList:
        for jet in InList:
            if deltaR(jet,lepton)<dR:

                if lepton._prefix.split('_')[0]=="Muon":
                    if lepton.pt>5 and lepton.mediumId==1:
                        InList.remove(jet)
                    elif lepton.mediumId==1:
                        if jet.chHEF<0.1 or jet.neHEF<0.2:
                            InList.remove(jet)
                         
                if lepton._prefix.split('_')[0]=="Electron":
                    if lepton.pt>15 and lepton.cutBased>0:
                        InList.remove(jet)
                    elif lepton.cutBased>0:
                        if jet.chHEF<0.1 or jet.neHEF<0.2:
                            InList.remove(jet)
                        
    InList.sort(key=getPt, reverse=True)

#Find the last particle in the chain before decay 23 -> 23 -> *23* -> 13 -13, return an GEN Object/ RECO??
def FindGenParticlebyStat(InList, pdgid, statusid):

    newList=[]
    for element in InList:
        if element.pdgId in pdgid and element.status in statusid:
            #BIT 0; 8; 13; 14
            #if bitwise(element.statusFlags,0) and \
            #        bitwise(element.statusFlags,8) and \
            #        bitwise(element.statusFlags,13) and \
            #        bitwise(element.statusFlags,14):
            #if element.status in ['62','1']:
            newList.append(element)
    if len(newList)>0:
        newList.sort(key=getPt, reverse=True)
    return newList

def isGenMother(particle, motherid, motherstatus, motherflag, genpart):

    moId=particle.genPartIdxMother
    while moId!=-1:
        if genpart[moId].pdgId in motherid and genpart[moId].status==motherstatus and genpart[moId].statusFlags==motherflag:
            return True
        moId=genpart[moId].genPartIdxMother
    return False

def isTauDecay(particle, genpart):

    moId=particle.genPartIdxMother
    while moId!=-1:
        if genpart[moId].pdgId in [15,-15]:
            return True
        moId=genpart[moId].genPartIdxMother
    return False

def FindGenParticlebyStatus(InList, pdgid, statusid1, statusid2):

    newList=[]
    for element in InList:
        if element.pdgId in pdgid and element.status==statusid1:
            moId=element.genPartIdxMother
            if InList[moId].status==statusid2:
                newList.append(element)
    return newList

def fromHardProcess(particle,genpart):
    
    moId=particle.genPartIdxMother
    while moId!=-1:
        if genpart[moId].status==23:
            return True
	moId=genpart[moId].genPartIdxMother
    return False

#def recoFinder(obj1s,obj2s):
#    
#    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.pdgId==y.pdgId)
#    #else:                                                                                                                                                           
#    #    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.partonFlavour==y.pdgId)                                                          
#    #print "dicts = ", dicts
#    recoflatten=[]
#    for key, value in dicts.iteritems():
#        if value is None: continue # None means genparts list is empty.
#        if len(value)==0: continue # empty list mean unsuccessful deltaR matching from GEN to Reco                                                              
#        #print "key = ", key                                                                                                        
#        #print "value[0].pdgId = ", value[0].pdgId
#        recoflatten.append(key)
#
#    return recoflatten

def genRecoFinder(obj1s,obj2s):

    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.pdgId==y.pdgId)
    genRecoflatten=[]
    for key, value in dicts.iteritems():
        if value is None: continue # None means genparts list is empty.                                                   
        if len(value)==0: continue # empty list mean unsuccessful deltaR matching from GEN to Reco                                                                           
        genRecoflatten.append([key,value[0]])
    if len(genRecoflatten)>0:
        genRecoflatten.sort(key=getpt, reverse=True)
    return genRecoflatten
    
def transverseMass(lepPt, lepPhi, met, metPhi):
    cosDPhi = cos(deltaPhi(lepPhi,metPhi))
    return sqrt(2*lepPt*met*(1-cosDPhi))

def invariantMass(p1_pt, p1_eta, p1_phi, p1_mass, p2_pt, p2_eta, p2_phi, p2_mass):

    if p1_pt<0 or p2_pt<0: return -1
    p1 = TLorentzVector()
    p2 = TLorentzVector()
    p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass)
    p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass)
    return (p1+p2).M()

def invariantMassPt(p1_pt, p1_eta, p1_phi, p1_mass, p2_pt, p2_eta, p2_phi, p2_mass):

    if p1_pt<0 or p2_pt<0: return -1
    p1 = TLorentzVector()
    p2 = TLorentzVector()
    p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass)
    p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass)
    return (p1+p2).Pt()

def invariantDoubleMass(Z_pt, Z_eta, Z_phi, jet1_pt, jet1_eta, jet1_phi, jet2_pt, jet2_eta, jet2_phi):

    if jet1_pt<0 or jet2_pt<0: return -1
    j1 = TLorentzVector()
    j2 = TLorentzVector()
    Z = TLorentzVector()
    Z.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, 91.)
    j1.SetPtEtaPhiM(jet1_pt, jet1_eta, jet1_phi, 5.)
    j2.SetPtEtaPhiM(jet2_pt, jet2_eta, jet2_phi, 5.)
    return (j1+j2+Z).M()

def daughterFinder(fgenparts,mothersList, genparts):

    #Two Possibilities                                                                                                                               
    #1.) decay is computed in ME status                                                                                                                                         
    # a.)WH 1 <- 23 | <- 22 | <- 62 <- 44 <- ... <- 22                                                                                               
    #2.) decay is generated at Pythia 8                                                                                                                                             
    # a.)W 1 | <- 62 <- 44 <- ... <- 22                                                                                                                                  
    # b.)WH 1 | <- 22 | <- 62 <- 44 <- ... <- 22                                                                                                                          
    daughters=[]
    motherIndex=[]
    pythiaFlags=['isPrompt', 'isHardProcess', 'fromHardProcess', 'isFirstCopy', 'isLastCopy']
    meFlags=['isPrompt', 'isHardProcess', 'fromHardProcess', 'isLastCopy']
    for genOBJ in fgenparts:
        decayChain=[]
        if genOBJ.status==1:
            moId=genOBJ.genPartIdxMother
            decayChain.append([genOBJ.pdgId,genOBJ.status,bitwiseDecoder(genOBJ.statusFlags),moId])
            while moId!=-1:
                decayChain.append([genparts[moId].pdgId,genparts[moId].status,bitwiseDecoder(genOBJ.statusFlags),moId])
                moId=genparts[moId].genPartIdxMother
        if len(decayChain)==0: continue
        #Running through on decayChain                                                                                                                                            
        #avoid overshot                                                                                                                                                         
        del decayChain[-1]
        for candidates in decayChain:
            pdgId=abs(candidates[0])
            staTus=candidates[1]
            staTusFlag=candidates[2]
            moInd=candidates[3]

            #pyStatus=[i for i, j in zip(staTusFlag, pythiaFlags) if i == j]
            #meStatus=[i for i, j in zip(staTusFlag, meFlags) if i == j]                                                                                  
            #if len(pyStatus)!=0 or len(meStatus)!=0 : break                                                                                                          
            if staTus!=62: continue
            if abs(pdgId) in mothersList:
                daughters.append(genOBJ)
                motherIndex.append(moInd)
                break

    return [daughters]

def printDecayCollection(inList,genpart):
    print ":==BEGIN COLLECTION HISTORY==:"
    for num,gen in enumerate(inList):
        moId=gen.genPartIdxMother
        print "Particle ",num, " --> pdgId = ", gen.pdgId , " ; status = ", gen.status , " ; pt = ", gen.pt, " ; mass = ", gen.mass," ; statflag = ", gen.statusFlags
        while moId!=-1:
            print "Particle ",num, " -- > mon pdgId = ", genpart[moId].pdgId , " ; mon status = ", genpart[moId].status , " ; pt = ", genpart[moId].pt , " ; mass = ", genpart[moId].mass," ; statflag = ", genpart[moId].statusFlags
            moId=genpart[moId].genPartIdxMother
    print ":==END==:"

def printDecayParticle(obj,genpart):
    print ":==BEGIN PARTICLE HISTORY==:"
    moId=obj.genPartIdxMother
    print " --> pdgId = ", obj.pdgId , " ; status = ", obj.status , " ; pt = ", obj.pt, " ; mass = ", obj.mass, " ; statflag = ", obj.statusFlags
    while moId!=-1:
        print " -- > mon pdgId = ", genpart[moId].pdgId , " ; mon status = ", genpart[moId].status , " ; pt = ", genpart[moId].pt , " ; mass = ", genpart[moId].mass," ; statflag = ", genpart[moId].statusFlags
        moId=genpart[moId].genPartIdxMother
    print ":==END==:"
