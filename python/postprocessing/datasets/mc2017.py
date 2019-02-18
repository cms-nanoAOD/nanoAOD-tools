from PhysicsTools.NanoAODTools.postprocessing.datasets.componentContainer import  ComponentContainer

QCD_15to20_Mu    = ComponentContainer('QCD_15to20_Mu', '/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 2.785e+06 )
QCD_20to30_Mu    = ComponentContainer('QCD_20to30_Mu', '/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 2.49e+06 )
QCD_30to50_Mu    = ComponentContainer('QCD_30to50_Mu', '/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 1.364e+06 )
QCD_50to80_Mu    = ComponentContainer('QCD_50to80_Mu', '/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 377400 )
QCD_80to120_Mu   = ComponentContainer('QCD_80to120_Mu', '/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 88350 )
QCD_120to170_Mu  = ComponentContainer('QCD_120to170_Mu', '/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 21250 )
QCD_170to300_Mu  = ComponentContainer('QCD_170to300_Mu', '/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 6969 )
QCD_300to470_Mu  = ComponentContainer('QCD_300to470_Mu', '/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 619.5 )
QCD_470to600_Mu  = ComponentContainer('QCD_470to600_Mu', '/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 58.9 )
#Still missing
#QCD_600to800_Mu  = ComponentContainer('QCD_600to800_Mu', '/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 18.36 )
#QCD_800to1000_Mu = ComponentContainer('QCD_800to1000_Mu', '/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 3.253 )
QCD_1000toInf_Mu = ComponentContainer('QCD_1000toInf_Mu', '/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 1.075 )

QCD_Mu = [ QCD_15to20_Mu, QCD_20to30_Mu, QCD_30to50_Mu, QCD_50to80_Mu, QCD_80to120_Mu, QCD_120to170_Mu, QCD_170to300_Mu, QCD_300to470_Mu, QCD_470to600_Mu,QCD_1000toInf_Mu]  #Still missing: #QCD_600to800_Mu, #QCD_800to1000_Mu


QCD_15to20_EM    = ComponentContainer('QCD_15to20_EM', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',  1.33e+06 )
QCD_20to30_EM    = ComponentContainer('QCD_20to30_EM', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 4.928e+06 )
QCD_30to50_EM    = ComponentContainer('QCD_30to50_EM', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 6.41e+06 )
QCD_50to80_EM    = ComponentContainer('QCD_50to80_EM', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 1.986e+06 )
QCD_80to120_EM    = ComponentContainer('QCD_80to120_EM', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 370900 )
QCD_120to170_EM    = ComponentContainer('QCD_120to170_EM', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 66760 )
#Still Missing
#QCD_170to300_EM    = ComponentContainer('QCD_170to300_EM', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 16430 )
QCD_300toInf_EM    = ComponentContainer('QCD_300toInf_EM', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 1101 )

QCD_EM = [QCD_15to20_EM, QCD_20to30_EM, QCD_30to50_EM, QCD_50to80_EM, QCD_80to120_EM, QCD_120to170_EM, QCD_300toInf_EM] #Still missing QCD_170to300_EM,
QCD_FR =  QCD_Mu + QCD_EM

TT_SL_PS = ComponentContainer('TTToSemiLeptonic_PSweights', '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 2*831.76*(3*0.108)*(1-3*0.108) )
TT_SL    = ComponentContainer('TTToSemiLeptonic', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM', 2*831.76*(3*0.108)*(1-3*0.108) )
TT_2L    = ComponentContainer('TTTo2L2Nu','/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',831.76*((3*0.108)**2))
TT_SLTb  = ComponentContainer('TTJets_amc_SingleLeptFromTbar','/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',831.76*(3*0.108)*(1-3*0.108))
TT_SLT   = ComponentContainer('TTJets_amc_SingleLeptFromT','/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 831.76*(3*0.108)*(1-3*0.108))
TT_Had   = ComponentContainer('TTToHadronic', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM', 831.76*(1-3*0.108)*(1-3*0.108) )

TT = [ TT_SL, TT_SL_PS, TT_2L, TT_SLT, TT_SLTb, TT_Had]


DY_M50     =  ComponentContainer('DYJetsToLL_M50','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',2008.*3)
DY_M10to50 =  ComponentContainer('DYJetsToLL_M10to50','/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 18610)
DY_M50_ext =  ComponentContainer('DYJetsToLL_M50_ext','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',2008.*3)
DY_M50_HT70_100  = ComponentContainer('DYJetsToLL_M50_HT70To100', '/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_M50_HT100_200 = ComponentContainer('DYJetsToLL_M50_HT100to200', '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_M50_HT200_400 = ComponentContainer('DYJetsToLL_M50_HT200to400', '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_M50_HT400_600 = ComponentContainer('DYJetsToLL_M50_HT400to600', '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_M50_HT600_800 = ComponentContainer('DYJetsToLL_M50_HT600to800','/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_0Jets  = ComponentContainer('DYJetsToLL_M50_0J', '/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_1Jets  = ComponentContainer('DYJetsToLL_M50_1J', '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
DY_2Jets  = ComponentContainer('DYJetsToLL_M50_2J', '/DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0)
WJets     = ComponentContainer('WJetsToLNu', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',3* 20508.9)
W1Jet     = ComponentContainer('W1JetsToLNu', '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',8123*1.17)
W2Jet     = ComponentContainer('W2JetsToLNu', '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',2785*1.17)
W3Jet     = ComponentContainer('W3JetsToLNu', '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',993.4*1.17)
W4Jet     = ComponentContainer('W4JetsToLNu', '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',542.4*1.17)

V = [DY_M50, DY_M10to50, DY_M50_ext, DY_M50_HT70_100, DY_M50_HT100_200, DY_M50_HT200_400,  DY_M50_HT400_600,  DY_M50_HT600_800, DY_0Jets,  DY_1Jets, DY_2Jets,  WJets, W1Jet, W2Jet, W3Jet, W4Jet]


TTWToLNu    = ComponentContainer("TTWToLNu","/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",0.2043)
TTW_LO_ext  = ComponentContainer("TTW_LO_ext1","/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM",0.6105 )
TTW_LO      = ComponentContainer("TTW_LO","/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM", 0.6105 )    
TTZ_LO_ext  = ComponentContainer("TTZ_LO_ext1", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM",0.5297/0.692)
TTZ_LO      = ComponentContainer("TTZ_LO", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM", 0.5297/0.692)
TTZToLLNuNu = ComponentContainer("TTZToLLNuNu","/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",0.2529)
TTZToQQ     = ComponentContainer("TTZToQQ","/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",0.5297)
TTH_amc     = ComponentContainer("TTH_amc","/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM",0.5085*(1-0.577))
TTH_pow     = ComponentContainer("TTH_pow","/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM",0.5085*(1-0.577))
TTG         = ComponentContainer("TTGJets","/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM", 3.697)

ttV = [TTWToLNu, TTW_LO_ext, TTW_LO, TTZ_LO_ext, TTZ_LO, TTZToLLNuNu, TTZToQQ, TTH_amc, TTH_pow, TTG]


tW_            = ComponentContainer('TW','/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',35.6)
tW_noHad_PS    = ComponentContainer('TW_NoFullyHadronic_PSweights','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',19.5)
tW_noHad       = ComponentContainer('TW_NoFullyHadronic','/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',19.5)
tbarW_PS       = ComponentContainer('TbarW_PSweights','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 35.6)
tbarW          = ComponentContainer('TbarW','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 35.6)
tbarW_noHad_PS = ComponentContainer('TbarW_NoFullyHadronic_PSweights','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',19.5)
tbarW_noHad    = ComponentContainer('TbarW_NoFullyHadronic','/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',19.5)
t_sch          = ComponentContainer('T_sch','/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',(7.20+4.16)*0.108*3)
t_tch          = ComponentContainer('T_tch','/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',136.02)
t_tbarch       = ComponentContainer('Tbar_tch','/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',80.95)


tW = [tW_, tW_noHad_PS, tW_noHad, tbarW_PS, tbarW, tbarW_noHad_PS, tbarW_noHad, t_sch, t_tch, t_tbarch]
ST = tW + [t_sch, t_tch, t_tbarch]


WWTo2L2Nu = ComponentContainer("WWTo2L2Nu","/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",10.481)
WW_DPS    = ComponentContainer("WW_DPS","/WW_DoubleScattering_13TeV-pythia8_TuneCP5/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",1.921)
WZTo3LNu  = ComponentContainer("WZTo3LNu","/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM",4.666)
WZTo2L2Q  = ComponentContainer("WZTo2L2Q","/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM",5.60)
ZZTo2L2Q  = ComponentContainer('ZZTo2L2Q', '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',3.28)
ZZTo2Q2Nu = ComponentContainer('ZZTo2Q2Nu', '/ZZTo2Q2Nu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',4.04)
ZZTo2L2Nu = ComponentContainer('ZZTo2L2Nu', '/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.564)
ZZTo4L    = ComponentContainer('ZZTo4L', '/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',1.256)
ZZTo4L_ext= ComponentContainer('ZZTo4L_ext1', '/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',1.256)

GGToZZTo2e2mu     = ComponentContainer('GluGluToContinToZZTo2e2mu'    ,  '/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 0.00319      )
GGToZZTo2e2mu_ext = ComponentContainer('GluGluToContinToZZTo2e2mu_ext1',  '/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM' , 0.00319  )
GGToZZTo2e2nu     = ComponentContainer('GluGluToContinToZZTo2e2nu',  '/GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00319        )
GGToZZTo2e2nu_ext = ComponentContainer('GluGluToContinToZZTo2e2nu_ext1'   ,'/GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00319  )
GGToZZTo2e2tau    = ComponentContainer('GluGluToContinToZZTo2e2tau'  ,'/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00319      )
GGToZZTo2e2tau_ext= ComponentContainer('GluGluToContinToZZTo2e2tau_ext1'  ,'/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00319 )
GGToZZTo2mu2nu    = ComponentContainer('GluGluToContinToZZTo2mu2nu'  ,'/GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00319      )
GGToZZTo2mu2nu_ext= ComponentContainer('GluGluToContinToZZTo2mu2nu_ext1'  ,'/GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00319 )
GGToZZTo2mu2tau   = ComponentContainer('GluGluToContinToZZTo2mu2tau' ,'/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00319)
GGToZZTo2mu2tau_ext= ComponentContainer('GluGluToContinToZZTo2mu2tau_ext1' ,'/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00319)
GGToZZTo4e        = ComponentContainer('GluGluToContinToZZTo4e'      ,'/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00159)
GGToZZTo4e_ext    = ComponentContainer('GluGluToContinToZZTo4e_ext1' ,'/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00159)
GGToZZTo4mu       = ComponentContainer('GluGluToContinToZZTo4mu'     ,'/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.00159)
GGToZZTo4mu_ext   = ComponentContainer('GluGluToContinToZZTo4mu_ext1','/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00159)
GGToZZTo4tau      = ComponentContainer('GluGluToContinToZZTo4tau', '/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6_ext1-v1/NANOAODSIM',0.00159)


VV = [WWTo2L2Nu, WW_DPS, WZTo3LNu, WZTo2L2Q, ZZTo2L2Q, ZZTo2L2Nu, ZZTo2Q2Nu, ZZTo4L, ZZTo4L_ext, GGToZZTo2e2mu, GGToZZTo2e2mu_ext, GGToZZTo2e2nu, GGToZZTo2e2nu_ext, GGToZZTo2e2tau, GGToZZTo2e2tau_ext, GGToZZTo2mu2nu, GGToZZTo2mu2nu_ext, GGToZZTo2mu2tau, GGToZZTo2mu2tau_ext, GGToZZTo4e, GGToZZTo4e_ext, GGToZZTo4mu, GGToZZTo4mu_ext, GGToZZTo4tau]


WWW =   ComponentContainer('WWW','/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.2086)
WWZ =    ComponentContainer('WWZ','/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.1651 )
WZZ =    ComponentContainer('WZZ','/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.05565)
WZG =    ComponentContainer('WZG','/WZG_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.0412)
ZZZ =    ComponentContainer('ZZZ','/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.01398)
VVV = [WWW, WWZ, WZZ, WZG, ZZZ]

TTTT = ComponentContainer('TTTT','/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/NANOAODSIM', 0.009103)
tZq  = ComponentContainer('tZq_ll','/tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.0758)
TTZZ = ComponentContainer('TTZZ','/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.001982)
TTZH = ComponentContainer('TTZH','/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.001535)
TTWZ = ComponentContainer('TTWZ','/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.001982)
TTWH = ComponentContainer('TTWH','/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.001140)
TTHH = ComponentContainer('TTHH','/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.0006666)
TTWW = ComponentContainer('TTWZ','/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM',0.006977)

Rare = [tZq, TTZZ, TTZH, TTWZ, TTTT, TTWH, TTHH, TTWW]

samples = TT + V + ttV + ST + VV + VVV + Rare

for sample in samples:
    sample.options['isData'] = False
