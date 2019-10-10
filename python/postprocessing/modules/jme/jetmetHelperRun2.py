#!/usr/bin/env python
import os, sys
import subprocess

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *

# JEC dict
jecTagsMC = {'2016' : 'Summer16_07Aug2017_V11_MC', 
             '2017' : 'Fall17_17Nov2017_V32_MC', 
             '2018' : 'Autumn18_V8_MC'}

archiveTagsDATA = {'2016' : 'Summer16_07Aug2017_V11_DATA', 
                   '2017' : 'Fall17_17Nov2017_V32_DATA', 
                   '2018' : 'Autumn18_V8_DATA'
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
                '2018A' : 'Autumn18_RunA_V8_DATA',
                '2018B' : 'Autumn18_RunB_V8_DATA',
                '2018C' : 'Autumn18_RunC_V8_DATA',
                '2018D' : 'Autumn18_RunD_V8_DATA',
                } 

jerTagsMC = {'2016' : 'Summer16_25nsV1_MC',
             '2017' : 'Fall17_V3_MC',
             '2018' : 'Fall17_V3_MC'
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

def createJMECorrector(isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False):
    
    dataYear = str(dataYear)
    jecTag_ = jecTagsMC[dataYear] if isMC else jecTagsDATA[dataYear + runPeriod]

    jmeUncert_ = [x for x in jesUncert.split(",")]

    jerTag_ = jerTagsMC[dataYear] 

    jmrValues_ = jmrValues[dataYear]

    jmsValues_ = jmsValues[dataYear]

    archiveTag_ = archiveTagsDATA[dataYear]
  
    print 'JEC=', jecTag_, '\t JER=', jerTag_

    jmeCorrections = None
    #jme corrections
    if isMC:
        jmeCorrections = lambda : jetmetUncertaintiesProducer(era=dataYear, globalTag=jecTag_, jesUncertainties=jmeUncert_, jerTag=jerTag_, jetType = jetType)
    else:
        jmeCorrections = lambda : jetmetUncertaintiesProducer(era=dataYear, archive=archiveTag_, globalTag=jecTag_, jesUncertainties=jmeUncert_, jerTag=jerTag_, jetType = jetType, isData=True)
    return jmeCorrections


###In the main postprocessor script, user has to call the function,
###e.g for 2016
#jmeCorrections = createJMECorrector(False, "2016", "B", "Total", True, "AK4PFchs", False)
#include jmeCorrections() in the list of modules to run.
###
