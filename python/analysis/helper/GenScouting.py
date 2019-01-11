from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, matchObjectCollectionMultiple

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
YELLOW = '\033[33m'

def getPt(pO):
    return pO[0].pt

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
    

def Display(DaughterList,MotherList, genparts):

    CollectionList=[]
    for obj in genparts:
        if obj.pdgId in DaughterList:
            CollectionList.append(obj)
    
    print BOLD,"=== Begin EVENT ===",ENDC
    print "Looking at ",CollectionList," of size : ",len(CollectionList)," from genparts of size :",len(genparts)," with MotherID ",MotherList
    
    for num,genw in enumerate(CollectionList):
        print YELLOW,"With daughter ",num,"th genpart with pdgId : ",OKGREEN,genw.pdgId,ENDC,", status : ",OKGREEN,genw.status,ENDC,", mass : ",genw.mass\
,", statusFlags : ", OKGREEN,bitwiseDecoder(genw.statusFlags),ENDC
        moId=genw.genPartIdxMother
        
        if genw.status!=1: print "NOT STABLE FINAL STATE"; continue
        if moId==-1: print "NO MOTHER, moId=-1"; continue
        
        if genparts[moId].pdgId in MotherList:
            print "With 0st grandmother pdgId : ",OKGREEN,genparts[moId].pdgId,ENDC,", status : ",OKGREEN,genparts[moId].status,ENDC,", mass : ",OKGREEN,genparts[moId].mass,ENDC,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId].statusFlags),ENDC
            moId2=genparts[moId].genPartIdxMother
            if moId2>0:
                print "With 1st grandmother pdgId : ",OKGREEN,genparts[moId2].pdgId,ENDC,", status : ",OKGREEN,genparts[moId2].status,ENDC,", mass : ",OKGREEN,genparts[moId2].mass,ENDC,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId2].statusFlags),ENDC
                moId3=genparts[moId2].genPartIdxMother
                if moId3>0:
                    print "With 2nd grandmother pdgId : ",OKGREEN,genparts[moId3].pdgId,ENDC,", status : ",OKGREEN,genparts[moId3].status,ENDC,", mass : ",OKGREEN,genparts[moId3].mass,ENDC,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId3].statusFlags),ENDC
                    moId4=genparts[moId3].genPartIdxMother
                    if moId4>0:
                        print "With 3rd grandmother pdgId : ", genparts[moId4].pdgId,", status : ", genparts[moId4].status,", mass : ", genparts[moId4].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId4].statusFlags),ENDC
                        moId5=genparts[moId4].genPartIdxMother
                        if moId5>0:
                            print "With 4th grandmother pdgId : ", genparts[moId5].pdgId,", status : ", genparts[moId5].status,", mass : ", genparts[moId5].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId5].statusFlags),ENDC
                            moId6=genparts[moId5].genPartIdxMother
                            if moId6>0:
                                print "With 5th grandmother pdgId : ", genparts[moId6].pdgId,", status : ", genparts[moId6].status,", mass : ", genparts[moId6].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId6].statusFlags),ENDC
                                moId7=genparts[moId6].genPartIdxMother
                                if moId7>0:
                                    print "With 6th grandmother pdgId : ", genparts[moId7].pdgId,", status : ", genparts[moId7].status,", mass : ", genparts[moId7].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId7].statusFlags),ENDC
                                    moId8=genparts[moId7].genPartIdxMother
                                    if moId8>0:
                                        print "With 7th grandmother pdgId : ", genparts[moId8].pdgId,", status : ", genparts[moId8].status,", mass : ", genparts[moId8].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId8].statusFlags),ENDC
                                        moId9=genparts[moId8].genPartIdxMother
                                        if moId9>0:
                                            print "With 8th grandmother pdgId : ", genparts[moId9].pdgId,", status : ", genparts[moId9].status,", mass : ", genparts[moId9].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId9].statusFlags),ENDC
                                            moId10=genparts[moId9].genPartIdxMother
                                            if moId10>0:
                                                print FAIL,"With 9th grandmother pdgId : ", genparts[moId10].pdgId,", status : ", genparts[moId10].status,", mass : ", genparts[moId10].mass,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId10].statusFlags),ENDC
        else:
            print "MOTHER NOT in ",MotherList,"'s pdgId : ",OKGREEN,genparts[moId].pdgId,ENDC,", status : ",OKGREEN,genparts[moId].status,ENDC,", mass : ",OKGREEN,genparts[moId].mass,ENDC,", statusFlags : ", OKGREEN,bitwiseDecoder(genparts[moId].statusFlags),ENDC
    print BOLD,"=== End EVENT ===",ENDC

def filterGenParticle(pdgidListing, genparts):

    filterlist=[]

    for gen in genparts:
        if abs(gen.pdgId) in pdgidListing:
            filterlist.append(gen)

    return filterlist

def recoFinder(obj1s,obj2s):

    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.pdgId==y.pdgId)
    #else:
    #    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.partonFlavour==y.pdgId)
    #print "dicts = ", dicts
    recoflatten=[]
    for key, value in dicts.iteritems():
        if value is None: continue # None means genparts list is empty.
        if len(value)==0: continue # empty list mean unsuccessful deltaR matching from GEN to Reco
        #print "key = ", key
        #print "value[0].pdgId = ", value[0].pdgId
        
        recoflatten.append(key)
        
    return recoflatten

def genRecoFinder(obj1s,obj2s):

    dicts=matchObjectCollectionMultiple(obj1s,obj2s,0.4,lambda x,y : x.pdgId==y.pdgId)
    genRecoflatten=[]
    for key, value in dicts.iteritems():
        if value is None: continue # None means genparts list is empty.
        if len(value)==0: continue # empty list mean unsuccessful deltaR matching from GEN to Reco
        genRecoflatten.append([key,value[0]])
        
    return genRecoflatten
    
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

def cleanFromLepton(objs,leptonCollection):

    cleanStuffs=[]
    dicts=matchObjectCollectionMultiple(objs,leptonCollection,0.4)
    for key, value in dicts.iteritems():
        #print "key : ", key , " ; value : ", value
        if (value is not None and len(value)!=0) or (value is not None) : continue
        
        cleanStuffs.append(key)
    return cleanStuffs
