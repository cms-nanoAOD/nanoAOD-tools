#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
#	'/store/data/Run2016D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/FB2EEAE0-BD81-1043-BD77-80BB4273EB6D.root',
#	'file:/afs/cern.ch/user/g/gimandor/public/Hmumu/nanoAODtest/CMSSW_9_4_6/WWTo2L2Nu_DoubleScattering_2017_nanoV5.root',
	#'/store/user/arizzi/FSRmyNanoProdMc2017_NANOV4b/VBFHToMuMu_M125_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv3_FSRmyNanoProdMc2017_NANOV4b_017_realistic_v14-v1/191012_175617/0000/myNanoProdMc2017_NANO_7.root'
        #'/store/user/nlu/Hmm/nanoAOD/FSRv1/store/mc/VBFHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1-1592/191012_055625/0000/myNanoProdMc2016_NANO_1.root'
#        "file:/home/users/sdonato/scratchssd/Skim/CMSSW_10_2_6/src/PhysicsTools/NanoAODTools/crab/myNanoProdMc2016_NANO_1.root"
'/store/user/arizzi/FSRmyNanoProdData2017_NANOV4/SingleMuon/RunIISummer16MiniAODv3_FSRmyNanoProdData2017_NANOV4_un2017E-31Mar2018-v1/191007_095718/0000/myNanoProdData2017_NANO_514.root'
#	'/store/data/Run2016B_ver2/SingleMuon/NANOAOD/Nano1June2019_ver2-v1/240000/0B92AB39-E3F2-DE4A-9CFE-CEE7D48B0798.root',
#	'/store/data/Run2018D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/98CBE3D1-4761-F24E-8007-2B2777551D2B.root',
#	'../../NanoAOD/test/lzma.root' ##you can change only this line
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

