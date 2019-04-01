#!/usr/bin/env python
'''@package docstring
Just a giant list of processes and properties
'''

processes =    {
        # inclusive NLO V+jets
        'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_nlo','MC',6025.2),
        'DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZtoNuNu_nlo','MC',11433.),
        'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('WJets_nlo','MC',61527.),

        # LO Z->nunu
        'ZJetsToNuNu_HT-100To200_13TeV-madgraph':('ZtoNuNu_ht100to200','MC',280.5),
        'ZJetsToNuNu_HT-200To400_13TeV-madgraph':('ZtoNuNu_ht200to400','MC',77.7),
        'ZJetsToNuNu_HT-400To600_13TeV-madgraph':('ZtoNuNu_ht400to600','MC',10.71),
        'ZJetsToNuNu_HT-600To800_13TeV-madgraph':('ZtoNuNu_ht600to800','MC',2.562),
        'ZJetsToNuNu_HT-800To1200_13TeV-madgraph':('ZtoNuNu_ht800to1200','MC',1.183),
        'ZJetsToNuNu_HT-1200To2500_13TeV-madgraph':('ZtoNuNu_ht1200to2500','MC',0.286),
        'ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph':('ZtoNuNu_ht2500toinf','MC',0.006945),
        'ZJetsToNuNu_HT-600ToInf_13TeV-madgraph':('ZtoNuNu_ht600toinf','MC',4.098),

        # LO Z->ll
        'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht100to200','MC',148.),
        'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht200to400','MC',40.94),
        'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht400to600','MC',5.497),
        'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht600toinf','MC',2.193),
        'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht1200to2500','MC',0.1514),
        'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht2500toinf','MC',0.003565),
        'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht600to800','MC',1.367),
        'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('ZJets_ht800to1200','MC',0.6304),

        # LO W->lnu
        'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht100to200','MC',1343),
        'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht200to400','MC',359.6),
        'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht400to600','MC',48.85),
        'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht600to800','MC',12.05),
        'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht800to1200','MC',5.501),
        'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht1200to2500','MC',1.329),
        'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht2500toinf','MC',0.03216),
        'WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('WJets_ht600toinf','MC',18.91),

        # NLO W->lnu
        'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('WJets_pt100to250','MC',677.82),
        'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('WJets_pt250to400','MC',24.083),
        'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('WJets_pt400to600','MC',3.0563),
        'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('WJets_pt600toinf','MC',0.4602),

        # NLO Z->ll
        'DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_pt50to100','MC',374.6800),
        'DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_pt100to250','MC',86.5200),
        'DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_pt250to400','MC',3.3247),
        'DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_pt400to650','MC',0.4491),
        'DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZJets_pt650toinf','MC',0.0422),

        # NLO Z->nunu
        'DYJetsToNuNu_PtZ-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZtoNuNu_pt100to250','MC',3*54.8229),
        'DYJetsToNuNu_PtZ-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZtoNuNu_pt250to400','MC',3*2.0705),
        'DYJetsToNuNu_PtZ-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZtoNuNu_pt400to650','MC',3*0.2779),
        'DYJetsToNuNu_PtZ-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8':('ZtoNuNu_pt650toinf','MC',3*0.0261),
                          
        # LO gamma
        'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('GJets_ht40to100','MC',23080.0),
        'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('GJets_ht100to200','MC',9235),
        'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('GJets_ht200to400','MC',2298),
        'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('GJets_ht400to600','MC',277.6),
        'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('GJets_ht600toinf','MC',93.47),

        # QCD
        'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht100to200','MC',27990000),
        'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht200to300','MC',1735000),
        'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht300to500','MC',366800),
        'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht500to700','MC',29370),
        'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht700to1000','MC',6524),
        'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht1000to1500','MC',1064),
        'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht1500to2000','MC',121.5),
        'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':('QCD_ht2000toinf','MC',25.42),

        # Single tops
        'ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8':('SingleTop_tTbar_lep','MC',26.22),
        'ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8':('SingleTop_tT_lep','MC',44.07),
        'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':('SingleTop_tW','MC',35.85),
        'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':('SingleTop_tbarW','MC',35.85),
        'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1':('SingleTop_tTbar','MC',80.95),
        'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1':('SingleTop_tT','MC',136.02),
        'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1':('SingleTop_s_lep','MC',10.11),
        'ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1':('SingleTop_t_lep','MC',216.99),
        'ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1':('SingleTop_tchannel','MC',44.3),

        # ttbar
        'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':                    ('TTbar_MLM','MC',831.76),
        'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':             ('TTbar_2L','MC',831.76*(1-0.68)*(1-0.68)),
        'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':    ('TTbar_1LT','MC',831.76*0.68*(1-0.68)),
        'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': ('TTbar_1LTbar','MC',831.76*0.68*(1-0.68)),
        'TTJets_SingleLeptFromT_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8': ('TTbar_FXFX_1LT','MC',831.76*0.68*(1-0.68)),
        'TTJets_SingleLeptFromTbar_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8': ('TTbar_FXFX_1LTbar','MC',831.76*0.68*(1-0.68)),
        'TT_TuneEE5C_13TeV-powheg-herwigpp':                                ('TTbar_Herwig','MC',831.76),
        'TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8':                 ('TTbar_FXFX','MC',831.76),
        'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8':                           ('TTbar_Powheg','MC',831.76),
        'TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8':                   ('TTbar_PowhegISRDown','MC',831.76),
        'TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8':                     ('TTbar_PowhegISRUp','MC',831.76),
        'TT_TuneCUETP8M2T4down_13TeV-powheg-pythia8':                       ('TTbar_PowhegTuneDown','MC',831.76),
        'TT_TuneCUETP8M2T4up_13TeV-powheg-pythia8':                         ('TTbar_PowhegTuneUp','MC',831.76),
        'TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8':('TTTo2L2Nu','MC',88.288),

        # exotic top
        'tZq_ll_4f_13TeV-amcatnlo-pythia8':('SingleTop_tZll','MC',0.0758),
        'tZq_nunu_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1':('SingleTop_tZnunu','MC',0.1379),
        'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8':('TTbar_GJets','MC',3.786),
        'TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8':('SingleTop_tG','MC',2.967),

        # EWK V+jets
        'EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8':('ZtoNuNu_EWK','MC',10.04),
        'EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8':('ZJets_EWK','MC',3.99),
        'EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8':('WJets_EWKWPlus','MC',25.81),
        'EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8':('WJets_EWKWMinus','MC',20.35),

        # regular dibosons
        'WW_TuneCUETP8M1_13TeV-pythia8':('Diboson_ww','MC',118.7),
        'WZ_TuneCUETP8M1_13TeV-pythia8':('Diboson_wz','MC',47.13),
        'ZZ_TuneCUETP8M1_13TeV-pythia8':('Diboson_zz','MC',16.523),
        
        # fancy dibosons
        'WWTo2L2Nu_13TeV-powheg':('WWTo2L2Nu','MC',(118.7-3.974)*0.1086*0.1086*9), #12.178
        'WWTo4Q_13TeV-powheg':('WWTo4Q','MC',51.723),
        'WWToLNuQQ_13TeV-powheg':('WWToLNuQQ','MC',49.997),
        'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8':('WZTo1L1Nu2Q','MC',10.71),
        'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8':('WZTo1L3Nu','MC',3.033),
        'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8':('WZTo2L2Q','MC',5.595),
        'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8':('WZTo3LNu','MC',4.430),
        'ZZTo2L2Nu_13TeV_powheg_pythia8':('ZZTo2L2Nu','MC',0.5644),
        'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8':('ZZTo2L2Q','MC',3.22),
        'ZZTo4L_13TeV_powheg_pythia8':('ZZTo4L','MC',1.212),
        'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8':('ggZZTo2e2nu','MC',0.003956),
        'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8':('ggZZTo2mu2tau','MC',0.003956),
        'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8':('ggZZTo2e2mu','MC',0.0073462),
        'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8':('ggZZTo2e2tau','MC',0.0073462),
        'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8':('ggZZTo2mu2tau','MC',0.0073462),
        'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8':('ggZZTo4e','MC',0.0036478),
        'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8':('ggZZTo4mu','MC',0.0036478),
        'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8':('ggZZTo4tau','MC',0.0036478),

        # Higgs->bb
        'ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8':('ZHbb_mH125','MC',0.08912),
        'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8':('ZllHbb_mH125','MC',0.04865),
        'ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8':('ggZHbb_mH125','MC',0.014366),
        'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8':('ggZllHbb_mH125','MC',0.007842),
        'WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':('WmLNuHbb','MC',0.100),
        'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8':('WpLNuHbb','MC',0.159),
        'ttHTobb_M125_13TeV_powheg_pythia8':('ttHbb','MC',0.506*0.5824),
        'GluGluHToBB_M125_13TeV_powheg_pythia8':('ggHbb','MC',48.48*0.5824),
        'VBFHToBB_M125_13TeV_amcatnlo_pythia8':('VBFHbb','MC',3.782*0.5824),

}
