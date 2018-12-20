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

def Display(DaughterList,MotherList, genparts):

    CollectionList=[]
    for obj in genparts:
        if obj.pdgId in DaughterList:
            CollectionList.append(obj)
    
    print BOLD,"=== Begin EVENT ===",ENDC
    print "Looking at ",CollectionList," of size : ",len(CollectionList)," from genparts of size :",len(genparts)," with MotherID ",MotherList
    
    for num,genw in enumerate(CollectionList):
        print YELLOW,"With daughter ",num,"th genpart with pdgId : ",OKGREEN,genw.pdgId,ENDC,", status : ",OKGREEN,genw.status,ENDC,", mass : ",genw.mass\
,", statusFlags : ", genw.statusFlags,ENDC
        moId=genw.genPartIdxMother
        if moId==-1: print "NO MOTHER, moId=-1"; continue
        if genparts[moId].pdgId in MotherList:
            print "With 0st grandmother pdgId : ",OKGREEN,genparts[moId].pdgId,ENDC,", status : ",OKGREEN,genparts[moId].status,ENDC,", mass : ",OKGREEN,genparts[moId].mass,ENDC,", statusFlags : ", genparts[moId].statusFlags
            moId2=genparts[moId].genPartIdxMother
            if moId2>0:
                print "With 1st grandmother pdgId : ",OKGREEN,genparts[moId2].pdgId,ENDC,", status : ",OKGREEN,genparts[moId2].status,ENDC,", mass : ",OKGREEN,genparts[moId2].mass,ENDC,", statusFlags : ", genparts[moId2].statusFlags
                moId3=genparts[moId2].genPartIdxMother
                if moId3>0:
                    print "With 2nd grandmother pdgId : ",OKGREEN,genparts[moId3].pdgId,ENDC,", status : ",OKGREEN,genparts[moId3].status,ENDC,", mass : ",OKGREEN,genparts[moId3].mass,ENDC,", statusFlags : ", genparts[moId3].statusFlags
                    moId4=genparts[moId3].genPartIdxMother
                    if moId4>0:
                        print "With 3rd grandmother pdgId : ", genparts[moId4].pdgId,", status : ", genparts[moId4].status,", mass : ", genparts[moId4].mass,", statusFlags : ", genparts[moId4].statusFlags
                        moId5=genparts[moId4].genPartIdxMother
                        if moId5>0:
                            print "With 4th grandmother pdgId : ", genparts[moId5].pdgId,", status : ", genparts[moId5].status,", mass : ", genparts[moId5].mass,", statusFlags : ", genparts[moId5].statusFlags
                            moId6=genparts[moId5].genPartIdxMother
                            if moId6>0:
                                print "With 5th grandmother pdgId : ", genparts[moId6].pdgId,", status : ", genparts[moId6].status,", mass : ", genparts[moId6].mass,", statusFlags : ", genparts[moId6].statusFlags
                                moId7=genparts[moId6].genPartIdxMother
                                if moId7>0:
                                    print "With 6th grandmother pdgId : ", genparts[moId7].pdgId,", status : ", genparts[moId7].status,", mass : ", genparts[moId7].mass,", statusFlags : ", genparts[moId7].statusFlags
                                    moId8=genparts[moId7].genPartIdxMother
                                    if moId8>0:
                                        print "With 7th grandmother pdgId : ", genparts[moId8].pdgId,", status : ", genparts[moId8].status,", mass : ", genparts[moId8].mass,", statusFlags : ", genparts[moId8].statusFlags
                                        moId9=genparts[moId8].genPartIdxMother
                                        if moId9>0:
                                            print "With 8th grandmother pdgId : ", genparts[moId9].pdgId,", status : ", genparts[moId9].status,", mass : ", genparts[moId9].mass,", statusFlags : ", genparts[moId9].statusFlags
                                            moId10=genparts[moId9].genPartIdxMother
                                            if moId10>0:
                                                print FAIL,"With 9th grandmother pdgId : ", genparts[moId10].pdgId,", status : ", genparts[moId10].status,", mass : ", genparts[moId10].mass,", statusFlags : ", genparts[moId10].statusFlags,ENDC
        #else:
        #    print "MOTHER NOT in ",MotherList,"'s pdgId : ",OKGREEN,genparts[moId].pdgId,ENDC,", status : ",OKGREEN,genparts[moId].status,ENDC,", mass : ",OKGREEN,genparts[moId].mass,ENDC,", statusFlags : ", genparts[moId].statusFlags
    print BOLD,"=== End EVENT ===",ENDC
