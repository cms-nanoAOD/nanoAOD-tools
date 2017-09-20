import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.source.fileNames = [
	'../../NanoAOD/test/save.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

