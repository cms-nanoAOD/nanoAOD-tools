#!/usr/bin/env python

samplelists=[
	'/lustre/cmswork/hoh/NANO/SSLep/data/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext5-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext5-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016B-03Feb2017_ver2-v2.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016C-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016D-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016E-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016G-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2016H-03Feb2017_ver2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2017C-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2017D-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2017E-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/DoubleMuonRun2017F-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/METRun2016B-03Feb2017_ver2-v2.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/METRun2016E-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/METRun2016G-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/METRun2016H-03Feb2017_ver2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016B-03Feb2017_ver2-v2.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016C-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016D-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016E-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016F-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016G-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2016H-03Feb2017_ver2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2017B-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2017C-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2017D-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2017E-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleElectronRun2017F-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016B-03Feb2017_ver2-v2.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016C-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016D-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016E-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016F-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016G-03Feb2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2016H-03Feb2017_ver2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2017B-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2017C-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2017D-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2017E-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/SingleMuonRun2017F-17Nov2017-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8-v1_1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1.root',
	'/lustre/cmswork/hoh/NANO/SSLep/data/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8-v1.root',
]
