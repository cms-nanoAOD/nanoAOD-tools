from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import os
import optparse
import sys

usage = 'python submit_crab.py'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
parser.add_option('--status', dest = 'status', default = False, action = 'store_true', help = 'Default do not check the status')
parser.add_option('-s', '--sub', dest = 'sub', default = False, action = 'store_true', help = 'Default do not submit')
parser.add_option('-k', '--kill', dest = 'kill', default = False, action = 'store_true', help = 'Default do not kill')
parser.add_option('-r', '--resub', dest = 'resub', default = False, action = 'store_true', help = 'Default do not resubmit')
parser.add_option('-g', '--gout', dest = 'gout', default = False, action = 'store_true', help = 'Default do not do getoutput')
(opt, args) = parser.parse_args()

def cfg_writer(sample, isMC, outdir):
    f = open("crab_cfg.py", "w")
    f.write("from WMCore.Configuration import Configuration\n")
    #f.write("from CRABClient.UserUtilities import config, getUsernameFromSiteDB\n")
    f.write("\nconfig = Configuration()\n")
    f.write("config.section_('General')\n")
    f.write("config.General.requestName = '"+sample.label+"'\n")
    if not isMC:
        f.write("config.General.instance = 'preprod'\n") #needed to solve a bug with Oracle server... 
    f.write("config.General.transferLogs=True\n")
    f.write("config.section_('JobType')\n")
    f.write("config.JobType.pluginName = 'Analysis'\n")
    f.write("config.JobType.psetName = 'PSet.py'\n")
    f.write("config.JobType.scriptExe = 'crab_script.sh'\n")
    f.write("config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py', '../scripts/keep_and_drop.txt']\n") #hadd nano will not be needed once nano tools are in cmssw
    f.write("config.JobType.sendPythonFolder = True\n")
    f.write("config.section_('Data')\n")
    f.write("config.Data.inputDataset = '"+sample.dataset+"'\n")
    f.write("config.Data.allowNonValidInputDataset = True\n")
    #f.write("config.Data.inputDBS = 'phys03'")
    f.write("config.Data.inputDBS = 'global'\n")
    if not isMC:
        f.write("config.Data.splitting = 'LumiBased'\n")
        if sample.year == '2016':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'\n")
        elif sample.year == '2017':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'\n")
        elif sample.year == '2018':
            f.write("config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'\n")
        f.write("config.Data.unitsPerJob = 50\n")
    else:
        f.write("config.Data.splitting = 'FileBased'\n")
        f.write("config.Data.unitsPerJob = 1\n")
    #config.Data.runRange = ''
    #f.write("config.Data.splitting = 'EventAwareLumiBased'")
    #f.write("config.Data.totalUnits = 10\n")
    f.write("config.Data.outLFNDirBase = '/store/user/%s/%s' % ('"+str(os.environ.get('USER'))+"', '" +outdir+"')\n")
    f.write("config.Data.publication = False\n")
    f.write("config.Data.outputDatasetTag = '"+sample.label+"'\n")
    f.write("config.section_('Site')\n")
    f.write("config.Site.storageSite = 'T2_IT_Pisa'\n")
    #f.write("config.Site.storageSite = "T2_CH_CERN"
    #f.write("config.section_("User")
    #f.write("config.User.voGroup = 'dcms'
    f.close()

def crab_script_writer(sample, outpath, isMC, modules, presel):
    f = open("crab_script.py", "w")
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

    #f.write("infile = "+str(sample.files)+"\n")
    #f.write("outpath = '"+ outpath+"'\n")
    #Deafult PostProcessor(outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression='LZMA:9',friend=False,postfix=None, jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0, prefetch=False,longTermCache=False)\n")
    if isMC:
        f.write("metCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", jesUncert='All', redojec=True)\n")
        f.write("fatJetCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", jesUncert='All', redojec=True, jetType = 'AK8PFchs')\n")
        f.write("p=PostProcessor('.', inputFiles(), '', modules=["+modules+"], provenance=True, fwkJobReport=True, histFileName='hist.root', histDirName='plots', outputbranchsel='keep_and_drop.txt')\n")# haddFileName='"+sample.label+".root'
    else: 
        f.write("metCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", runPeriod='"+str(sample.runP)+"', jesUncert='All', redojec=True)\n")
        f.write("fatJetCorrector = createJMECorrector(isMC="+str(isMC)+", dataYear="+str(sample.year)+", runPeriod='"+str(sample.runP)+"', jesUncert='All', redojec=True, jetType = 'AK8PFchs')\n")
        f.write("p=PostProcessor('.', inputFiles(), '"+presel+"', modules=["+modules+"], provenance=True, fwkJobReport=True, jsonInput=runsAndLumis(), haddFileName='tree_hadd.root', outputbranchsel='keep_and_drop.txt')\n")#
    f.write("p.run()\n")
    f.write("print 'DONE'\n")
    f.close()

    f_sh = open("crab_script.sh", "w")
    f_sh.write("#!/bin/bash\n")
    f_sh.write("echo Check if TTY\n")
    f_sh.write("if [\"`tty`\" != \"not a tty\" ]; then\n")
    f_sh.write("  echo \"YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES\"\n")
    f_sh.write("else\n\n")
    f_sh.write("echo \"ENV...................................\"\n")
    f_sh.write("env\n")
    f_sh.write("echo \"VOMS\"\n")
    f_sh.write("voms-proxy-info -all\n")
    f_sh.write("echo \"CMSSW BASE, python path, pwd\"\n")
    f_sh.write("echo $CMSSW_BASE\n")
    f_sh.write("echo $PYTHON_PATH\n")
    f_sh.write("echo $PWD\n")
    f_sh.write("rm -rf $CMSSW_BASE/lib/\n")
    f_sh.write("rm -rf $CMSSW_BASE/src/\n")
    f_sh.write("rm -rf $CMSSW_BASE/module/\n")
    f_sh.write("rm -rf $CMSSW_BASE/python/\n")
    f_sh.write("mv lib $CMSSW_BASE/lib\n")
    f_sh.write("mv src $CMSSW_BASE/src\n")
    f_sh.write("mv module $CMSSW_BASE/module\n")
    f_sh.write("mv python $CMSSW_BASE/python\n")

    f_sh.write("echo Found Proxy in: $X509_USER_PROXY\n")
    f_sh.write("python crab_script.py $1\n")
    if isMC:
        f_sh.write("hadd tree_hadd.root tree.root hist.root\n")
    f_sh.write("fi\n")
    f_sh.close()

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

if not(opt.dat in sample_dict.keys()):
    print sample_dict.keys()
dataset = sample_dict[opt.dat]

samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.  
else:
    print "You are launching a single sample and not an entire bunch of samples"
    samples.append(dataset)

submit = opt.sub
status = opt.status
kill = opt.kill
resubmit = opt.resub
getout = opt.gout
#Writing the configuration file
for sample in samples:
    print 'Launching sample ' + sample.label
    if submit:
        #Writing the script file 
        year = str(sample.year)
        lep_mod = 'lepSF_'+year+'()'
        btag_mod = 'btagSF'+year+'()'
        met_hlt_mod = 'MET_HLT_Filter_'+year+'()'
        if ('Data' in sample.label):
            isMC = False
            presel = "Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter "
            if year == '2016' and sample.runP != 'H':
                presel += " && (HLT_PFHT800 || HLT_PFHT900 || HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT)"
            elif year == '2016' and sample.runP == 'H':
                presel += " && (HLT_PFHT900 || HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT)"
            elif year == '2017' and sample.runP != 'B':
                presel += " && (HLT_PFHT780 || HLT_PFHT890 || HLT_Mu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT)"
            elif year == '2017' and sample.runP == 'B':
                presel += " && (HLT_PFHT780 || HLT_PFHT890 || HLT_Mu50)"
            elif year == '2018':
                presel += " && (HLT_PFHT780 || HLT_PFHT890 || HLT_Mu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT)"
        else:
            isMC = True
            presel = ""
                
        print 'The flag isMC is: ' + str(isMC)

        print "Producing crab configuration file"
        cfg_writer(sample, isMC, "OutDir")
        
        
        if isMC:
            modules = "MCweight_writer(),  " + met_hlt_mod + ", preselection(), " + lep_mod + ", " + btag_mod + ", PrefCorr(), metCorrector(), fatJetCorrector()" # Put here all the modules you want to be runned by crab
        else:
            modules = "preselection(), metCorrector(), fatJetCorrector()" # Put here all the modules you want to be runned by crab
            
        print "Producing crab script"
        crab_script_writer(sample,'/eos/user/'+str(os.environ.get('USER')[0]) + '/'+str(os.environ.get('USER'))+'/Wprime/nosynch/', isMC, modules, presel)
        os.system("chmod +x crab_script.sh")
        
        #Launching crab
        print "Submitting crab jobs..."
        os.system("crab submit -c crab_cfg.py")

    elif kill:
        print "Killing crab jobs..."
        os.system("crab kill -d crab_" + sample.label)
        os.system("rm -rf crab_" + sample.label)

    elif resubmit:
        print "Resubmitting crab jobs..."
        os.system("crab resubmit -d crab_" + sample.label)
        
    elif status:
        print "Checking crab jobs status..."
        os.system("crab status -d crab_" + sample.label)
        
    elif getout:
        print "crab getoutput -d crab_" + sample.label + " --xrootd > ./macros/files/" + sample.label + ".txt"
        os.system("crab getoutput -d crab_" + sample.label + " --xrootd > ./macros/files/" + sample.label + ".txt")
        #for i in xrange(1, 969):
        #os.system("crab getoutput -d crab_" + sample.label + " --outputpath=/eos/user/"+str(os.environ.get('USER')[0]) + "/"+str(os.environ.get('USER'))+"/Wprime/nosynch/" + sample.label + "/ --jobids="+str(i))
