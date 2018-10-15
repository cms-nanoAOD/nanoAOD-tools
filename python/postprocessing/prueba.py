import ROOT
import math, os,re
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetReCalibrator import JetReCalibrator

fileName = GetFileName(isData, run):

def GetEraForRun(run):
 era = ''
 if  (run <= 297019):                 era = 'A';
 elif(run <= 299329 && run > 297019): era = 'B';
 elif(run <= 302029 && run > 299336): era = 'C';
 elif(run <= 303434 && run > 302029): era = 'D';
 elif(run <= 304826 && run > 303434): era = 'E';
 elif(run <= 306462 && run > 304910): era = 'F';
 return era

def GetFileName(isData, run):
  if not isData: return "Fall17_17Nov2017_V6_MC"
  else return 'Fall17_17Nov2017' + GetEraForRun(run) + '_V6_DATA'

jetType = "AK4PFchs"
jesInputFilePath = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"

jetReCalibrator = JetReCalibrator(fileMC, jetType , True, jesInputFilePath, upToLevel=1)
corr = jetReCalibrator.getCorrection(jet, rho)
