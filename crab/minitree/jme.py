#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

#jecredo option has been removed check why------> Doest matter because redo option was for fat jets not for AK4 jets 

#createJMECorrector(isMC=True, dataYear=2016,runPeriod="B",jesUncert="Total",jetType="AK4PFchs",noGroom=False,metBranchName="MET",applySmearing=True, isFastSim=False, applyHEMfix=False,splitJER=False, saveMETUncs=['T1', 'T1Smear']
jmeCorrectionsUL2016preVFP_MC_AK4CHS = createJMECorrector(True, "UL2016_preVFP", "", "All", "AK4PFchs", False,"MET", splitJER=True)   #2016 MC AK4 CHS 
jmeCorrectionsUL2016postVFP_MC_AK4CHS = createJMECorrector(True, "UL2016", "", "All", "AK4PFchs", False,"MET", splitJER=True)   #2016 MC AK4 CHS
jmeCorrectionsUL2017_MC_AK4CHS = createJMECorrector(True, "UL2017", "", "All", "AK4PFchs", False,"MET", splitJER=True)   #2017 MC AK4 CHS
jmeCorrectionsUL2018_MC_AK4CHS = createJMECorrector(True, "UL2018", "", "All", "AK4PFchs", False,"MET", splitJER=True)   #2018 MC AK4 CHS

#jecTag_ = jecTagsDATA[dataYear + runPeriod]

#preVFP
jmeCorrectionsULRun2016B_ver1_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "B", "All", "AK4PFchs") 
jmeCorrectionsULRun2016B_ver2_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "B", "All", "AK4PFchs")
jmeCorrectionsULRun2016C_HIPM_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "C", "All", "AK4PFchs")
jmeCorrectionsULRun2016D_HIPM_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "D", "All", "AK4PFchs")
jmeCorrectionsULRun2016E_HIPM_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "E", "All", "AK4PFchs")
jmeCorrectionsULRun2016F_HIPM_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "F", "All", "AK4PFchs")

#postVFP
jmeCorrectionsULRun2016F_DATA_AK4CHS = createJMECorrector(False, "UL2016", "F", "All", "AK4PFchs") # postVFP
jmeCorrectionsULRun2016G_DATA_AK4CHS = createJMECorrector(False, "UL2016", "G", "All", "AK4PFchs")
jmeCorrectionsULRun2016H_DATA_AK4CHS = createJMECorrector(False, "UL2016", "H", "All", "AK4PFchs")

#UL2017
jmeCorrectionsULRun2017B_DATA_AK4CHS = createJMECorrector(False, "UL2017", "B", "All", "AK4PFchs")
jmeCorrectionsULRun2017C_DATA_AK4CHS = createJMECorrector(False, "UL2017", "C", "All", "AK4PFchs")
jmeCorrectionsULRun2017D_DATA_AK4CHS = createJMECorrector(False, "UL2017", "D", "All", "AK4PFchs")
jmeCorrectionsULRun2017E_DATA_AK4CHS = createJMECorrector(False, "UL2017", "E", "All", "AK4PFchs")
jmeCorrectionsULRun2017F_DATA_AK4CHS = createJMECorrector(False, "UL2017", "F", "All", "AK4PFchs")

#UL2018
jmeCorrectionsULRun2018A_DATA_AK4CHS = createJMECorrector(False, "UL2018", "A", "All", "AK4PFchs")
jmeCorrectionsULRun2018B_DATA_AK4CHS = createJMECorrector(False, "UL2018", "B", "All", "AK4PFchs")
jmeCorrectionsULRun2018C_DATA_AK4CHS = createJMECorrector(False, "UL2018", "C", "All", "AK4PFchs")
jmeCorrectionsULRun2018D_DATA_AK4CHS = createJMECorrector(False, "UL2018", "D", "All", "AK4PFchs")
