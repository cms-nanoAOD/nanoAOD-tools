from PhysicsTools.NanoAODTools.postprocessing.datasets.componentContainer import  ComponentContainer


# dasgoclient --query="dataset dataset=/*/Run2017*-31Mar2018-*/NANOAOD"
# dasgoclient --query="dataset dataset=/*/Run2017*-17Nov2017-*/MINIAOD"


SingleMuon = [
    ComponentContainer('SingleMuon_Run2017B', '/SingleMuon/Run2017B-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017C', '/SingleMuon/Run2017C-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017D', '/SingleMuon/Run2017D-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017E', '/SingleMuon/Run2017E-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleMuon_Run2017F', '/SingleMuon/Run2017F-31Mar2018-v1/NANOAOD'),
    ]

SingleElectron=[
    ComponentContainer('SingleElectron_Run2017B', '/SingleElectron/Run2017B-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017C', '/SingleElectron/Run2017C-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017D', '/SingleElectron/Run2017D-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017E', '/SingleElectron/Run2017E-31Mar2018-v1/NANOAOD'),
    ComponentContainer('SingleElectron_Run2017F', '/SingleElectron/Run2017F-31Mar2018-v1/NANOAOD'),
    ]

MuonEG=[
    ComponentContainer('MuonEG_Run2017B', '/MuonEG/Run2017B-31Mar2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017C', '/MuonEG/Run2017C-31Mar2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017D', '/MuonEG/Run2017D-31Mar2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017E', '/MuonEG/Run2017E-31Mar2018-v1/NANOAOD'),
    ComponentContainer('MuonEG_Run2017F', '/MuonEG/Run2017F-31Mar2018-v1/NANOAOD'),
    ]

DoubleMuon=[
    ComponentContainer('DoubleMuon_Run2017B', '/DoubleMuon/Run2017B-31Mar2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017C', '/DoubleMuon/Run2017C-31Mar2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017D', '/DoubleMuon/Run2017D-31Mar2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017E', '/DoubleMuon/Run2017E-31Mar2018-v1/NANOAOD'),
    ComponentContainer('DoubleMuon_Run2017F', '/DoubleMuon/Run2017F-31Mar2018-v1/NANOAOD')
    ]

DoubleElectron=[
    ComponentContainer('DoubleEG_Run2017B', '/DoubleEG/Run2017B-31Mar2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017C', '/DoubleEG/Run2017C-31Mar2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017D', '/DoubleEG/Run2017D-31Mar2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017E', '/DoubleEG/Run2017E-31Mar2018-v1/NANOAOD'), 
    ComponentContainer('DoubleEG_Run2017F', '/DoubleEG/Run2017F-31Mar2018-v1/NANOAOD'), 
]

samples = SingleMuon+SingleElectron+MuonEG+DoubleMuon+DoubleElectron
for sample in samples:
    sample.options['isData'] = True
