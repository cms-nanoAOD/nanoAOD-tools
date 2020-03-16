from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os

def cfg_writer(label, dataset, outdir):
    f = open("crab_cfg.py", "w")
    f.write("from WMCore.Configuration import Configuration\n")
    f.write("from CRABClient.UserUtilities import config, getUsernameFromSiteDB\n")
    f.write("\nconfig = Configuration()\n")
    f.write("config.section_('General')\n")
    f.write("config.General.requestName = '"+label+"'\n")
    f.write("config.General.transferLogs=True\n")
    f.write("config.section_('JobType')\n")
    f.write("config.JobType.pluginName = 'Analysis'\n")
    f.write("config.JobType.psetName = 'PSet.py'\n")
    f.write("config.JobType.scriptExe = 'crab_script.sh'\n")
    f.write("config.JobType.inputFiles = ['crab_script_prova.py','../scripts/haddnano.py']\n") #hadd nano will not be needed once nano tools are in cmssw
    f.write("config.JobType.sendPythonFolder = True\n")
    f.write("config.section_('Data')\n")
    f.write("config.Data.inputDataset = '"+dataset+"'\n")
    #f.write("config.Data.inputDBS = 'phys03'")
    f.write("config.Data.inputDBS = 'global'\n")
    f.write("config.Data.splitting = 'FileBased'\n")
    #config.Data.runRange = ''
    #config.Data.lumiMask  = ''
    #f.write("config.Data.splitting = 'EventAwareLumiBased'")
    f.write("config.Data.unitsPerJob = 3\n")
    #f.write("config.Data.totalUnits = 10\n")
    f.write("config.Data.outLFNDirBase = '/store/user/%s/%s' % (getUsernameFromSiteDB(), '" +outdir+"')\n")
    f.write("config.Data.publication = False\n")
    f.write("config.Data.outputDatasetTag = '"+label+"'\n")
    f.write("config.section_('Site')\n")
    f.write("config.Site.storageSite = 'T2_IT_Pisa'\n")
    #f.write("config.Site.storageSite = "T2_CH_CERN"
    #f.write("config.section_("User")
    #f.write("config.User.voGroup = 'dcms'
    f.close()

def crab_script_writer(sample, outpath, isMC, year, modules):
    f = open("crab_script_prova.py", "w")
    f.write("#!/usr/bin/env python\n")
    f.write("import os\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.MET_HLT_Filter import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.examples.preselection import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *\n")
    f.write("from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *\n")

    f.write("metCorrector = createJMECorrector(isMC="+isMC+", dataYear="+year+", jesUncert='All', redojec=True)\n")
    f.write("fatJetCorrector = createJMECorrector(isMC="+isMC+", dataYear="+year+", jesUncert='All', redojec=True, jetType = 'AK8PFchs')\n")

    #f.write("infile = "+str(sample.files)+"\n")
    #f.write("outpath = '"+ outpath+"'\n")
    #Deafult PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression='LZMA:9',friend=False,postfix=None, jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0, prefetch=False,longTermCache=False)\n")
    f.write("p=PostProcessor('.', inputFiles(), '', modules=["+modules+"], provenance=True, fwkJobReport=True, histFileName='"+sample.label+"_hist.root', haddFileName='"+sample.label+".root', histDirName='plots')\n")#, jsonInput=runsAndLumis(), outputbranchsel="+os.path.abspath('../python/postprocessing/examples/keep_and_drop.txt')+"
    f.write("p.run()\n")
    f.write("print 'DONE'\n")
    f.close()

def PSet_writer(sample):
    f = open("PSet.py", "w")
    f.write("import FWCore.ParameterSet.Config as cms\n")
    f.write("process = cms.Process('NANO')\n")
    f.write("process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(),\n")
    #       lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
    f.write(")\n")
    f.write("process.source.fileNames = [\n")
    f.write("        '../../NanoAOD/test/lzma.root' ##you can change only this line\n")
    f.write("]\n")
    f.write("process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))\n")
    f.write("process.output = cms.OutputModule('PoolOutputModule', fileName = cms.untracked.string('"+sample.label+".root'))\n")
    f.write("process.out = cms.EndPath(process.output)\n")
    f.close()
    
sample = TT_Mtt1000toInf_2017
#Writing the configuration file
print "Producing crab configuration file"
cfg_writer(sample.label, sample.dataset, "OutDir")

#Writing the script file 
if '2016' in sample.label:
    year = '2016'
    lep_mod = 'lepSF_2016()'
    btag_mod = 'btagSF2016()'
    met_hlt_mod = 'MET_HLT_Filter_2016()'
if '2017' in sample.label:
    year = '2017'
    lep_mod = 'lepSF_2017()'
    btag_mod = 'btagSF2017()'
    met_hlt_mod = 'MET_HLT_Filter_2017()'
if '2018' in sample.label:
    year = '2018'
    lep_mod = 'lepSF_2018()'
    btag_mod = 'btagSF2018()'
    met_hlt_mod = 'MET_HLT_Filter_2018()'

if ('SingleMuon' in sample.label) or ('SingleElectron' in sample.label):
    isMC = 'False'
else:
    isMC = 'True'

if isMC:
    modules = "MCweight_writer(),  " + met_hlt_mod + ", " + lep_mod + ", " + btag_mod + ", PrefCorr(), metCorrector(), fatJetCorrector()" # Put here all the modules you want to be runned by crab
else:
    modules = "MET_HLT_Filter(), PrefCorr()" # Put here all the modules you want to be runned by crab

print "Producing crab script"
crab_script_writer(sample,'/eos/user/a/adeiorio/Wprime/nosynch/', isMC, year, modules)

#Launching crab
print "Submitting crab jobs..."
os.system("crab submit -c crab_cfg.py")
