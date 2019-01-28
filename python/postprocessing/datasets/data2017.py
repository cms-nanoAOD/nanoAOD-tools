from PhysicsTools.NanoAODTools.postprocessing.datasets.componentContainer import  ComponentContainer


SingleMuon = [
    ComponentContainer('SingleMuon_Run2017B', '/SingleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017C', '/SingleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017D', '/SingleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017E', '/SingleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017F', '/SingleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD'),
    ]

SingleElectron=[
    ComponentContainer('SingleElectron_Run2017B', '/SingleElectron/Run2017B-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017C', '/SingleElectron/Run2017C-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017D', '/SingleElectron/Run2017D-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017E', '/SingleElectron/Run2017E-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017F', '/SingleElectron/Run2017F-Nano14Dec2018-v1/NANOAOD'),
    ]

MuonEG=[
    ComponentContainer('MuonEG_Run2017B', '/MuonEG/Run2017B-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017C', '/MuonEG/Run2017C-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017D', '/MuonEG/Run2017D-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017E', '/MuonEG/Run2017E-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017F', '/MuonEG/Run2017F-Nano14Dec2018-v1/NANOAOD'),
    ]

DoubleMuon=[
    ComponentContainer('DoubleMuon_Run2017B', '/DoubleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017C', '/DoubleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017D', '/DoubleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017E', '/DoubleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017F', '/DoubleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD')
    ]

DoubleElectron=[
    ComponentContainer('DoubleEG_Run2017B', '/DoubleEG/Run2017B-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017C', '/DoubleEG/Run2017C-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017D', '/DoubleEG/Run2017D-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017E', '/DoubleEG/Run2017E-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017F', '/DoubleEG/Run2017F-Nano14Dec2018-v1/NANOAOD'), 
]

MET=[
    ComponentContainer('MET_Run2017B', '/MET/Run2017B-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('MET_Run2017C', '/MET/Run2017C-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('MET_Run2017D', '/MET/Run2017D-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('MET_Run2017E', '/MET/Run2017E-Nano14Dec2018-v1/NANOAOD'), 
    ComponentContainer('MET_Run2017F', '/MET/Run2017F-Nano14Dec2018-v1/NANOAOD'), 
]

samples = SingleMuon+SingleElectron+MuonEG+DoubleMuon+DoubleElectron+MET
for sample in samples:
    sample.options['isData'] = True
