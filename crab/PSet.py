#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	'/store/data/Run2016D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/FB2EEAE0-BD81-1043-BD77-80BB4273EB6D.root',
#	'/store/data/Run2018D/SingleMuon/NANOAOD/Nano1June2019-v1/40000/98CBE3D1-4761-F24E-8007-2B2777551D2B.root',
#	'../../NanoAOD/test/lzma.root' ##you can change only this line
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

