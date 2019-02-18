import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from math import fabs
from PhysicsTools.NanoAODTools.analysis.helper.helper import *
from PhysicsTools.NanoAODTools.postprocessing.tools import closest
from ROOT import TLorentzVector

class Producer(Module):
    #def __init__(self, jetSelection):
    def __init__(self, DEBUG):
        #self.jetSel = jetSelection
        self.debug = DEBUG
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.FilesName=inputFile
        self.InputTree=inputTree
        ##Scalar
        self.out.branch("ZptCorr","F")
        self.out.branch("Zpt","F")
        self.out.branch("Zeta","F")
        self.out.branch("isOSmumu","I")
        self.out.branch("isOSee","I")
        self.out.branch("isOSemu","I")
        self.out.branch("isSSmumu","I")
        self.out.branch("isSSee","I")

        self.out.branch("htpt", "F")
        self.out.branch("htphi", "F")
        self.out.branch("Vmass", "F")
        self.out.branch("Vpt", "F")

        ## Vector
        ## GEN-W sorted in a way 0 index --> W leg ; 1,2 Higgs decay W
        self.out.branch("GenWpt", "F", 0, "nGenW", "nGenW", False)
        self.out.branch("GenWeta", "F", 0, "nGenW", "nGenW", False)
        self.out.branch("GenWphi", "F", 0, "nGenW", "nGenW", False)
        self.out.branch("GenWmass", "F", 0, "nGenW", "nGenW", False)
        self.out.branch("GenWsign", "I", 0, "nGenW", "nGenW", False)
        
        ## GEN-Lepton
        self.out.branch("GenLpt", "F", 0, "nGenL", "nGenL", False)
        self.out.branch("GenLeta", "F", 0, "nGenL", "nGenL", False)
        self.out.branch("GenLphi", "F", 0, "nGenL", "nGenL", False)
        self.out.branch("GenLmass", "F", 0, "nGenL", "nGenL", False)
        self.out.branch("GenLsign", "I", 0, "nGenL", "nGenL", False)

        ## SIGNAL STUDY  ##############################################
        ##RECO
        self.out.branch("RecoLpt", "F", 0, "nRecoL", "nRecoL", False)
        self.out.branch("RecoLeta", "F", 0, "nRecoL", "nRecoL", False)
        self.out.branch("RecoLphi", "F", 0, "nRecoL", "nRecoL", False)
        self.out.branch("RecoLmass", "F", 0, "nRecoL", "nRecoL", False)
        self.out.branch("RecoLsign", "I", 0, "nRecoL", "nRecoL", False)
        ## SIGNAL STUDY  ##############################################
        
        ##ANALYSIS-LEVEL
        #Lepton
        self.out.branch("LepPt", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepEta", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepPhi", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepMass", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepIso03", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepIso04", "F", 0, "nLepton", "nLepton", False)
        self.out.branch("LepSign", "I", 0, "nLepton", "nLepton", False)
        self.out.branch("LepMediumId", "I", 0, "nLepton", "nLepton", False)
        self.out.branch("LepCutBased", "I", 0, "nLepton", "nLepton", False)
        self.out.branch("LepMindRJet", "F", 0, "nLepton", "nLepton", False)

        #Tau
        self.out.branch("TauPt", "F", 0, "nTaulep", "nTaulep", False)
        self.out.branch("TauEta", "F", 0, "nTaulep", "nTaulep", False)
        self.out.branch("TauPhi", "F", 0, "nTaulep", "nTaulep", False)
        self.out.branch("TauMass", "F", 0, "nTaulep", "nTaulep", False)
        #self.out.branch("TauPartFlav", "I", 0, "nTaulep", "nTaulep", False)

        #Photon
        self.out.branch("PhoPt", "F", 0, "nPho", "nPho", False)
	self.out.branch("PhoEta", "F", 0, "nPho", "nPho", False)
        self.out.branch("PhoPhi", "F", 0, "nPho", "nPho", False)
        self.out.branch("PhoMass", "F", 0, "nPho", "nPho", False)
        self.out.branch("PhoSign", "I", 0, "nPho", "nPho", False)

        #Jet
        self.out.branch("JetPt", "F", 0, "nJet", "nJet", False)
	self.out.branch("JetEta", "F", 0, "nJet", "nJet", False)
        self.out.branch("JetPhi", "F", 0, "nJet", "nJet", False)
        self.out.branch("JetMass", "F", 0, "nJet", "nJet", False)
        self.out.branch("JetchHEF", "F", 0, "nJet", "nJet", False)
        self.out.branch("JetneHEF", "F", 0, "nJet", "nJet", False)
        #self.out.branch("JetSign", "I", 0, "nJet", "nJet", False)
        
        #CleanJet
        self.out.branch("CleanJetPt", "F", 0, "nCJet", "nCJet", False)
        self.out.branch("CleanJetEta", "F", 0, "nCJet", "nCJet", False)
        self.out.branch("CleanJetPhi", "F", 0, "nCJet", "nCJet", False)
        self.out.branch("CleanJetMass", "F", 0, "nCJet", "nCJet", False)
        self.out.branch("CleanJetchHEF", "F", 0, "nJet", "nJet", False)
        self.out.branch("CleanJetneHEF", "F", 0, "nJet", "nJet", False)
        #self.out.branch("CleanJetSign", "I", 0, "nCJet", "nCJet", False)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if self.debug: print " === EVENT Begin === "
        ########################################
        #            READ OBJECTS                                                                                                                                                   
        ########################################
        ##READ Collection
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        taus = Collection(event, "Tau")
        photons = Collection(event, "Photon")
        jets = Collection(event, "Jet")
        
        ## PU
        ####                                                                                                                                                                   
        ## Trigger                                                                                                                                                             
        ####
        
        ## PRESELECTION + QUALITY SELECTION + PHASE SPACE SELECTION
        ## Electron
        ElecList =filter(lambda x: (x.pt>15 and fabs(x.eta)<2.4 and x.cutBased>0 ), electrons)
        ## Muon
        MuonList =filter(lambda x: (x.pt>5 and fabs(x.eta)<2.4 and x.mediumId>0 ), muons)
        LepList= ElecList + MuonList
        
        ## Jets Analysis collection
        JetListSS =filter(lambda x: (x.pt>30 and fabs(x.eta)<2.5 and x.jetId>0 and x.puId>4), jets)
        #cleanFromleptonSS(JetListSS,ElecList)
        #cleanFromleptonSS(JetListSS,MuonList)
        #cleanFromleptonSS(JetListSS,TauList)
        cleanFromleptonSS(JetListSS,LepList)
        njet = len(JetListSS)
        ht = ROOT.TLorentzVector()
        #Initialization
        JetPt=[0.]*(njet); JetEta=[0.]*(njet); JetPhi=[0.]*(njet); JetMass=[0.]*(njet); JetchHEF=[0.]*(njet); JetneHEF=[0.]*(njet); #JetSign=[0]*(njet);
        for i,ijet in enumerate(JetListSS):
            JetPt[i] = ijet.pt
            JetEta[i] = ijet.eta
            JetPhi[i] = ijet.phi
            JetMass[i] = ijet.mass
            JetchHEF[i] = ijet.chHEF
            JetneHEF[i] = ijet.neHEF
            #JetSign[i] = ijet.partonFlavour
            #HT
            if ijet.pt<30: continue
            if fabs(ijet.eta)>2.5: continue
            ht += ijet.p4()

        ## CLEANJet
        CleanJetList =filter(lambda x: (x.pt>30 and fabs(x.eta)<2.5 and x.jetId>0 and x.puId>4 and x.nElectrons==0 and x.nMuons==0), jets)
        cleanFromlepton(CleanJetList,ElecList)
        cleanFromlepton(CleanJetList,MuonList)
        ncjet = len(CleanJetList)
        CleanJetPt=[0.]*(ncjet); CleanJetEta=[0.]*(ncjet); CleanJetPhi=[0.]*(ncjet); CleanJetMass=[0.]*(ncjet); CleanJetchHEF=[0.]*(ncjet); CleanJetneHEF=[0.]*(ncjet); #CleanJetSign=[0]*(ncjet);
        for i,icjet in enumerate(CleanJetList):
            CleanJetPt[i] = icjet.pt
            CleanJetEta[i] = icjet.eta
            CleanJetPhi[i] = icjet.phi
            CleanJetMass[i] = icjet.mass
            CleanJetchHEF[i] = icjet.chHEF
            CleanJetneHEF[i] = icjet.neHEF
            #CleanJetSign[i] = icjet.partonFlavour

        #Lepton
        nlep=len(LepList)
        LepList.sort(key=getPt, reverse=True)
        #Initialization
        LepPt=[0.]*(nlep); LepEta=[0.]*(nlep); LepPhi=[0.]*(nlep); LepMass=[0.]*(nlep); LepIso03=[0.]*(nlep); LepIso04=[0.]*(nlep); LepSign=[0]*(nlep); 
        LepMediumId=[-1]*(nlep); LepCutBased=[-1]*(nlep); LepMindRJet=[6.5]*(nlep)
        for i,ilep in enumerate(LepList):
            LepPt[i]=ilep.pt
            LepEta[i]=ilep.eta
            LepPhi[i]=ilep.phi
            LepMass[i]=ilep.mass
            LepSign[i]=ilep.pdgId
            if abs(LepSign[i])==11:
                LepCutBased[i]=ilep.cutBased
                LepIso03[i]=ilep.pfRelIso03_all
            else:
                LepMediumId[i]=ilep.mediumId
                LepIso03[i]=ilep.pfRelIso03_all
                LepIso04[i]=ilep.pfRelIso04_all
            if closest(ilep,JetListSS)[1]<900:
                LepMindRJet[i]=closest(ilep,JetListSS)[1]

        #Tau
        TauList =filter(lambda x: (x.pt>18 and fabs(x.eta)<2.3), taus)
        cleanFromlepton(TauList,LepList)
        ntau=len(TauList)
        #Initialization
        TauPt=[0.]*(ntau); TauEta=[0.]*(ntau); TauPhi=[0.]*(ntau); TauMass=[0.]*(ntau); #TauPartFlav=[0]*(ntau); 
        for i,itau in enumerate(TauList):
            TauPt[i] = itau.pt
            TauEta[i] = itau.eta
            TauPhi[i] = itau.phi
            TauMass[i] = itau.mass
            ## https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc80X_doc.html#Tau
            #TauPartFlav[i] = itau.genPartFlav

        ## Photon                                                                                                                  
        PhotonList =filter(lambda x: (x.pt>15 and fabs(x.eta)<2.5), photons)
        cleanFromlepton(PhotonList,LepList)
        npho = len(PhotonList)
        #Initialization
        PhoPt=[0.]*(npho); PhoEta=[0.]*(npho); PhoPhi=[0.]*(npho); PhoMass=[0.]*(npho); PhoSign=[0]*(npho);
        for i,ipho in enumerate(PhotonList):
            PhoPt[i] = ipho.pt
            PhoEta[i] = ipho.eta
            PhoPhi[i] = ipho.phi
            PhoMass[i] = ipho.mass
            PhoSign[i] = ipho.pdgId

        ###########################################
        #   GEN LEVEL
        ###########################################
        ## Gen Weight
        ####
        ## Lhe Particles
        ####
        ## Mc Stitching
        ####
        ## GenParticle
        ## Initialization
        Zweight= 1.
        Zpt=-999.
        Zeta=-999.
        if "nGenPart" in self.InputTree.GetListOfBranches():
            genparts = Collection(event, "GenPart")
            GenLists=filter(lambda x:x,genparts)
            ## GEN candidates objects
            theGenZ = FindGenParticlebyStat(GenLists, [23],[62])
            theGenw = FindGenParticlebyStat(GenLists, [24,-24],[22,62])
            theGenW =filter(lambda x: x.statusFlags!=4481,theGenw)
            # Gen Top
            theGenTop = FindGenParticlebyStat(GenLists, [6],[1])
            theGenAntiTop = FindGenParticlebyStat(GenLists, [-6],[1])

            # GEN Leptons
            genLepton = FindGenParticlebyStat(GenLists, [13,-13,11,-11],[1])
            genNeutrino = FindGenParticlebyStat(GenLists, [12,-12,14,-14],[1])
            genHadron = FindGenParticlebyStat(GenLists, [1,2,3,4,5,-1,-2,-3,-4,-5],[1])
            
            ## GEN Zpt weight
            NgenZ=0

            if "DYJetsToLL" in self.FilesName.GetName().split('/')[-1].split('_')[0]:
                for genZ in theGenZ:
                    #if genZ.status!=62: continue
                    NgenZ+=1
                    if NgenZ>1: continue
                    Zpt=genZ.pt
                    Zeta=genZ.eta
                    #Ugo's Prescription                                                                                                                      
                    if Zpt<20: Zweight=1.2
                    if Zpt>20 and Zpt<30: Zweight=1.
                    if Zpt>30 and Zpt<40: Zweight=0.75
                    if Zpt>40 and Zpt<50: Zweight=0.65
                    if Zpt>50 and Zpt<200: Zweight=0.65-0.00034*Zpt
                    if Zpt>200: Zweight=0.6

            ## GEN-level signal ANALYSIS
            
            #GEN-Lepton
            #Initialization
            nPart=3 ## Number of lepton to write
            GenLpt=[0.]*nPart; GenLeta=[0.]*nPart; GenLphi=[0.]*nPart; GenLsign=[0]*nPart; GenLmass=[0.]*nPart
            RecoLpt=[0.]*nPart; RecoLeta=[0.]*nPart; RecoLphi=[0.]*nPart; RecoLsign=[0]*nPart; RecoLmass=[0.]*nPart
            matchPair=genRecoFinder(genLepton,ElecList+MuonList)
            for num,igenlep in enumerate(matchPair):
                if (num+1)>nPart: continue
                genlep=igenlep[0]
                recolep=igenlep[1]
                #W mom from outer leg
                index=0
                if isGenMother(genlep,[24,-24],62,10497,genparts):
                    index=0
                elif isGenMother(genlep,[-24,24],22,14721,genparts):
                    index=1
                elif isGenMother(genlep,[-24,24],22,14721,genparts):
                    index=2
                else:
                    continue
                
                GenLpt[index]=genlep.pt
                GenLeta[index]=genlep.eta
                GenLphi[index]=genlep.phi
                GenLsign[index]=genlep.pdgId
                GenLmass[index]=genlep.mass

                RecoLpt[index]=recolep.pt
                RecoLeta[index]=recolep.eta
                RecoLphi[index]=recolep.phi
                RecoLsign[index]=recolep.pdgId
                RecoLmass[index]=recolep.mass

            #GEN-Wboson
            #Initialization
            GenWpt=[0.]*nPart; GenWeta=[0.]*nPart; GenWphi=[0.]*nPart; GenWsign=[0]*nPart; GenWmass=[0.]*nPart
            for num,genW in enumerate(theGenW):
                if (num+1)>nPart: continue
                GenWpt[num]=genW.pt
                GenWeta[num]=genW.eta
                GenWphi[num]=genW.phi
                GenWsign[num]=genW.pdgId
                GenWmass[num]=genW.mass

            ##### Fill Gen-object
            self.out.fillBranch("GenLpt", GenLpt)
            self.out.fillBranch("GenLeta", GenLeta)
            self.out.fillBranch("GenLphi", GenLphi)
            self.out.fillBranch("GenLsign", GenLsign)
            self.out.fillBranch("GenLmass", GenLmass)

            # gen-reco
            self.out.fillBranch("RecoLpt", RecoLpt)
            self.out.fillBranch("RecoLeta", RecoLeta)
            self.out.fillBranch("RecoLphi", RecoLphi)
            self.out.fillBranch("RecoLsign", RecoLsign)
            self.out.fillBranch("RecoLmass", RecoLmass)

            self.out.fillBranch("GenWpt", GenWpt)
            self.out.fillBranch("GenWeta", GenWeta)
            self.out.fillBranch("GenWphi", GenWphi)
            self.out.fillBranch("GenWsign", GenWsign)
            self.out.fillBranch("GenWmass", GenWmass)
            
        ########################################
        #   ANALYSIS
        ########################################
        ##Categorization base on number of leptons and flavour combination.
        isOSmumu=0; isOSee=0; isOSemu=0; isSSmumu=0; isSSee=0
        Vmass=-999.
        Vpt=-999.
        #Filling only with leading and subleading lepton
        if nlep>=2:
            ##Opposite sign 
            if LepSign[0]+LepSign[1]==0:
                ## same flavor 13+13
                if abs(LepSign[0])+abs(LepSign[1])==26:
                    isOSmumu=1
                ## same flavor 11+11
                elif abs(LepSign[0])+abs(LepSign[1])==22:
                    isOSee=1
            # opposite flavor -11+13 = 2 ; 11-13 =-2
            elif abs(LepSign[0])==11 and LepSign[0]+LepSign[1] in [2,-2]:
                isOSemu=1
            # same sign 13+13 ; -13-13
            elif LepSign[0]+LepSign[1] in [26,-26]:
                isSSmumu=1
            # same sign 11+11 ; -11-11
            elif LepSign[0]+LepSign[1] in [22,-22]:
                isSSee=1

            Vmass=invariantMass(LepPt[0],LepEta[0],LepPhi[0],LepMass[0],LepPt[1],LepEta[1],LepPhi[1],LepMass[1])
            Vpt=invariantMassPt(LepPt[0],LepEta[0],LepPhi[0],LepMass[0],LepPt[1],LepEta[1],LepPhi[1],LepMass[1])


        #### FILLING BRANCHES #######
        ##GEN
        self.out.fillBranch("Zpt",Zpt)
        self.out.fillBranch("Zeta",Zeta)
        self.out.fillBranch("ZptCorr",Zweight)

        ##Fill RECO-Object
        self.out.fillBranch("isOSmumu",isOSmumu)
        self.out.fillBranch("isOSee",isOSee)
        self.out.fillBranch("isOSemu",isOSemu)
        self.out.fillBranch("isSSmumu",isSSmumu)
        self.out.fillBranch("isSSee",isSSee)
            
        #Lepton
        self.out.fillBranch("LepPt", LepPt)
        self.out.fillBranch("LepEta", LepEta)
        self.out.fillBranch("LepPhi", LepPhi)
        self.out.fillBranch("LepMass", LepMass)
        self.out.fillBranch("LepIso03", LepIso03)
        self.out.fillBranch("LepIso04", LepIso04)
        self.out.fillBranch("LepSign", LepSign)
        self.out.fillBranch("LepMediumId", LepMediumId)
        self.out.fillBranch("LepCutBased", LepCutBased)
        self.out.fillBranch("LepMindRJet", LepMindRJet)

        #Tau
        self.out.fillBranch("TauPt", TauPt)
        self.out.fillBranch("TauEta", TauEta)
        self.out.fillBranch("TauPhi", TauPhi)
        self.out.fillBranch("TauMass", TauMass)
        #self.out.fillBranch("TauPartFlav", TauPartFlav)
        
        #Photon
        self.out.fillBranch("PhoPt", PhoPt)
	self.out.fillBranch("PhoEta", PhoEta)
        self.out.fillBranch("PhoPhi", PhoPhi)
        self.out.fillBranch("PhoMass", PhoMass)
        self.out.fillBranch("PhoSign", PhoSign)
        
        #Jet
        self.out.fillBranch("JetPt", JetPt)
	self.out.fillBranch("JetEta", JetEta)
        self.out.fillBranch("JetPhi", JetPhi)
        self.out.fillBranch("JetMass", JetMass)
        self.out.fillBranch("JetchHEF", JetchHEF)
        self.out.fillBranch("JetneHEF", JetneHEF)
        #self.out.fillBranch("JetSign", JetSign)
        #self.out.fillBranch("JetdRLep", JetdRLep)
        
        #Cjet
        self.out.fillBranch("CleanJetPt", CleanJetPt)
        self.out.fillBranch("CleanJetEta", CleanJetEta)
        self.out.fillBranch("CleanJetPhi", CleanJetPhi)
        self.out.fillBranch("CleanJetMass", CleanJetMass)
        self.out.fillBranch("CleanJetchHEF", CleanJetchHEF)
        self.out.fillBranch("CleanJetneHEF", CleanJetneHEF)
        #self.out.fillBranch("CleanJetSign", CleanJetSign)
        #self.out.fillBranch("CleanJetdRLep", CleanJetdRLep)
        
        self.out.fillBranch("htpt",ht.Pt())
        self.out.fillBranch("htphi",ht.Phi())
        self.out.fillBranch("Vmass",Vmass)
        self.out.fillBranch("Vpt",Vpt)

        if self.debug: print " === EVENT END === "
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

producer = lambda : Producer(DEBUG=False)

#\
    #jetSelection= lambda j : (j.pt > 30 and abs(j.eta)<2.5)
#\)
