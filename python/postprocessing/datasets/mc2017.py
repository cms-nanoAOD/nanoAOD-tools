from PhysicsTools.NanoAODTools.postprocessing.datasets.componentContainer import  ComponentContainer


TT = [
    ComponentContainer('TTToSemiLeptonic_PSweights', '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTToSemiLeptonic', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTTo2L2Nu','/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTJets_amc_SingleLeptFromTbar','/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTJets_amc_SingleLeptFromT','/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
]

V = [
    ComponentContainer('DY_newpmx','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM'),
    ComponentContainer('DY','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_70to100', '/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_400to600', '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_200to400', '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_100to200', '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_10to50', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_2J', '/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_1J', '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('DY_0J', '/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('WJets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
]

ttV = [
    ComponentContainer("TTW_LO","/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM"),
    ComponentContainer("TTW_LO_noext","/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM"),    
    ComponentContainer("TTZ_LO","/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM"),
    ComponentContainer("TTH_amc","/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM"),
    ComponentContainer("TTGJets","/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM"),
    ComponentContainer("TTGJets_newpmx","/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM"),
]

tW = [
    #ComponentContainer('tW','/ST_tW_top_5f_inclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    #ComponentContainer('tW','/ST_tW_top_5f_inclusiveDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TW','/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TW_NoFullyHadronic_PSweights','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TW_NoFullyHadronic','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    #ComponentContainer('','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    #ComponentContainer('','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TbarW_PSweights','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TbarW','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TbarW_NoFullyHadronic_PSweights','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TbarW_NoFullyHadronic','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    
]

VV = [
    ComponentContainer("WWTo2L2Nu","/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM"),
    ComponentContainer("WZTo3LNu","/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM"),
    ComponentContainer("WZTo2L2Q","/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM"),
    ComponentContainer('ZZTo2L2Q', '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('ZZTo2Q2Nu', '/ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('ZZTo4L', '/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('ZZTo4L_ext1', '/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM'),
    ComponentContainer('VVTo2L2Nu','/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
]

VVV = [

]

Rare = [
    ComponentContainer('tZq_ll','/tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTZZ','/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTZH','/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    ComponentContainer('TTWZ','/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM'),
    
    
# '/TTTW_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
# '/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
# '/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM',
# '/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
# '/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
#'/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM',
]

samples = TT + V + ttV + tW + VV + VVV + Rare
for sample in samples:
    sample.options['isData'] = False
