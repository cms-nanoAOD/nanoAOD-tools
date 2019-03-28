#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
    #'../data/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8-v1.root' ##you can change only this line
    '/store/mc/RunIIAutumn18NanoAODv4/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/30000/53AD801E-F002-DA42-9D0F-6F9DD4FD06E0.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

