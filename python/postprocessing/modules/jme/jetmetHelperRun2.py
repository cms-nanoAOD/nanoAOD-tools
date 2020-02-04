#!/usr/bin/env python
import os, sys
import subprocess

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties_copy2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *

# JEC dict
jecTagsMC = {'2016' : 'Summer16_07Aug2017_V11_MC', 
             '2017' : 'Fall17_17Nov2017_V32_MC', 
             '2018' : 'Autumn18_V19_MC'}

archiveTagsDATA = {'2016' : 'Summer16_07Aug2017_V11_DATA', 
                   '2017' : 'Fall17_17Nov2017_V32_DATA', 
                   '2018' : 'Autumn18_V19_DATA',
                  }

jecTagsDATA = { '2016B' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016C' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016D' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016E' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016F' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016G' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2017B' : 'Fall17_17Nov2017B_V32_DATA', 
                '2017C' : 'Fall17_17Nov2017C_V32_DATA', 
                '2017D' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017E' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017F' : 'Fall17_17Nov2017F_V32_DATA', 
                '2018A' : 'Autumn18_RunA_V19_DATA',
                '2018B' : 'Autumn18_RunB_V19_DATA',
                '2018C' : 'Autumn18_RunC_V19_DATA',
                '2018D' : 'Autumn18_RunD_V19_DATA',
                } 

jerTagsMC = {'2016' : 'Summer16_25nsV1_MC',
             '2017' : 'Fall17_V3_MC',
             '2018' : 'Autumn18_V7_MC'
            }

#jet mass resolution: https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging
#nominal, up, down
jmrValues = {'2016' : [1.0, 1.2, 0.8],
             '2017' : [1.09, 1.14, 1.04],
             '2018' : [1.09, 1.14, 1.04]        # Use 2017 values for 2018 until 2018 are released
            }

#jet mass scale
#W-tagging PUPPI softdrop JMS values: https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging
#2016 values 
jmsValues = { '2016' : [1.00, 0.9906, 1.0094], #nominal, down, up
              '2017' : [0.982, 0.978, 0.986],
              '2018' : [0.982, 0.978, 0.986] # Use 2017 values for 2018 until 2018 are released
            }

def createJMECorrector(isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False, metBranchName="MET", applySmearing=True, isFastSim=False):
    
    jecTag_ = jecTagsMC[dataYear] if isMC else jecTagsDATA[dataYear + runPeriod]

    jmeUncert_ = [x for x in jesUncert.split(",")]

    jerTag_ = jerTagsMC[dataYear] 

    jmrValues_ = jmrValues[dataYear]

    jmsValues_ = jmsValues[dataYear]

    archiveTag_ = archiveTagsDATA[dataYear]

    met_ = metBranchName

    print 'JEC=', jecTag_, '\t JER=', jerTag_
    print 'MET branch=', met_

    jmeCorrections = None
    #jme corrections

    if 'AK4' in jetType:
      if isMC:
          jmeCorrections = lambda : jetmetUncertaintiesProducer(era=dataYear,                      globalTag=jecTag_, jesUncertainties=jmeUncert_, jerTag=jerTag_, jetType = jetType, metBranchName=met_, applySmearing = applySmearing)
      else:
          jmeCorrections = lambda : jetmetUncertaintiesProducer(era=dataYear, archive=archiveTag_, globalTag=jecTag_, jesUncertainties=jmeUncert_, jerTag=jerTag_, jetType = jetType, metBranchName=met_, isData=True)
    # no MET variations calculated
    else:
      if isMC:
          jmeCorrections = lambda : fatJetUncertaintiesProducer(era=dataYear,                      globalTag=jecTag_, jesUncertainties=jmeUncert_, redoJEC=redojec, jetType = jetType, jerTag=jerTag_, jmrVals = jmrValues_, jmsVals = jmsValues_, applySmearing = applySmearing)
      else:
          jmeCorrections = lambda : fatJetUncertaintiesProducer(era=dataYear, archive=archiveTag_, globalTag=jecTag_, jesUncertainties=jmeUncert_, redoJEC=redojec, jetType = jetType, jerTag=jerTag_, jmrVals = jmrValues_, jmsVals = jmsValues_, isData=True)

    return jmeCorrections


###In the main postprocessor script, user has to call the function,
###e.g for 2016
#jmeCorrections = createJMECorrector(False, "2016", "B", "Total", True, "AK4PFchs", False)
#include jmeCorrections() in the list of modules to run.
###
jmeCorrections2016_MC_AK4CHS = createJMECorrector(True, "2016", "", "All", True, "AK4PFchs", False)   #2017 MC AK4 CHS
jmeCorrections2017_MC_AK4CHS = createJMECorrector(True, "2017", "", "All", True, "AK4PFchs", False)   #2017 MC AK4 CHS
jmeCorrections2018_MC_AK4CHS = createJMECorrector(True, "2018", "", "All", True, "AK4PFchs", False)   #2017 MC AK4 CHS

jmeCorrections2016_MC_AK8Puppi = createJMECorrector(True, "2016", "", "All", True, "AK8PFPuppi", False)   #2017 MC AK4 CHS
jmeCorrections2017_MC_AK8Puppi = createJMECorrector(True, "2017", "", "All", True, "AK8PFPuppi", False)   #2017 MC AK4 CHS
jmeCorrections2018_MC_AK8Puppi = createJMECorrector(True, "2018", "", "All", True, "AK8PFPuppi", False)   #2017 MC AK4 CHS

jmeCorrections2017B_DATA_AK4CHS = createJMECorrector(False, "2017", "B", "All", True, "AK4PFchs", False)
jmeCorrections2017C_DATA_AK4CHS = createJMECorrector(False, "2017", "C", "All", True, "AK4PFchs", False)
jmeCorrections2017D_DATA_AK4CHS = createJMECorrector(False, "2017", "D", "All", True, "AK4PFchs", False)
jmeCorrections2017E_DATA_AK4CHS = createJMECorrector(False, "2017", "E", "All", True, "AK4PFchs", False)
jmeCorrections2017F_DATA_AK4CHS = createJMECorrector(False, "2017", "F", "All", True, "AK4PFchs", False)

jmeCorrections2017B_DATA_AK8Puppi = createJMECorrector(False, "2017", "B", "All", True, "AK8PFPuppi", False)
jmeCorrections2017C_DATA_AK8Puppi = createJMECorrector(False, "2017", "C", "All", True, "AK8PFPuppi", False)
jmeCorrections2017D_DATA_AK8Puppi = createJMECorrector(False, "2017", "D", "All", True, "AK8PFPuppi", False)
jmeCorrections2017E_DATA_AK8Puppi = createJMECorrector(False, "2017", "E", "All", True, "AK8PFPuppi", False)
jmeCorrections2017F_DATA_AK8Puppi = createJMECorrector(False, "2017", "F", "All", True, "AK8PFPuppi", False)

jmeCorrections2016B_DATA_AK4CHS = createJMECorrector(False, "2016", "B", "All", True, "AK4PFchs", False)
jmeCorrections2016C_DATA_AK4CHS = createJMECorrector(False, "2016", "C", "All", True, "AK4PFchs", False)
jmeCorrections2016D_DATA_AK4CHS = createJMECorrector(False, "2016", "D", "All", True, "AK4PFchs", False)
jmeCorrections2016E_DATA_AK4CHS = createJMECorrector(False, "2016", "E", "All", True, "AK4PFchs", False)
jmeCorrections2016F_DATA_AK4CHS = createJMECorrector(False, "2016", "F", "All", True, "AK4PFchs", False)
jmeCorrections2016G_DATA_AK4CHS = createJMECorrector(False, "2016", "G", "All", True, "AK4PFchs", False)
jmeCorrections2016H_DATA_AK4CHS = createJMECorrector(False, "2016", "H", "All", True, "AK4PFchs", False)

jmeCorrections2016B_DATA_AK8Puppi = createJMECorrector(False, "2016", "B", "All", True, "AK8PFPuppi", False)
jmeCorrections2016C_DATA_AK8Puppi = createJMECorrector(False, "2016", "C", "All", True, "AK8PFPuppi", False)
jmeCorrections2016D_DATA_AK8Puppi = createJMECorrector(False, "2016", "D", "All", True, "AK8PFPuppi", False)
jmeCorrections2016E_DATA_AK8Puppi = createJMECorrector(False, "2016", "E", "All", True, "AK8PFPuppi", False)
jmeCorrections2016F_DATA_AK8Puppi = createJMECorrector(False, "2016", "F", "All", True, "AK8PFPuppi", False)
jmeCorrections2016G_DATA_AK8Puppi = createJMECorrector(False, "2016", "G", "All", True, "AK8PFPuppi", False)
jmeCorrections2016H_DATA_AK8Puppi = createJMECorrector(False, "2016", "H", "All", True, "AK8PFPuppi", False)

jmeCorrections2018A_DATA_AK4CHS = createJMECorrector(False, "2018", "A", "All", True, "AK4PFchs", False)
jmeCorrections2018B_DATA_AK4CHS = createJMECorrector(False, "2018", "B", "All", True, "AK4PFchs", False)
jmeCorrections2018C_DATA_AK4CHS = createJMECorrector(False, "2018", "C", "All", True, "AK4PFchs", False)
jmeCorrections2018D_DATA_AK4CHS = createJMECorrector(False, "2018", "D", "All", True, "AK4PFchs", False)

jmeCorrections2018A_DATA_AK8Puppi = createJMECorrector(False, "2018", "A", "All", True, "AK8PFPuppi", False)
jmeCorrections2018B_DATA_AK8Puppi = createJMECorrector(False, "2018", "B", "All", True, "AK8PFPuppi", False)
jmeCorrections2018C_DATA_AK8Puppi = createJMECorrector(False, "2018", "C", "All", True, "AK8PFPuppi", False)
jmeCorrections2018D_DATA_AK8Puppi = createJMECorrector(False, "2018", "D", "All", True, "AK8PFPuppi", False)


#include jmeCorrections() in the list of modules to run.
###


