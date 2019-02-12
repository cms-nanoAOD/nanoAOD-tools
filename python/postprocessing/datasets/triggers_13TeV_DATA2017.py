# Triggers for 2017 DATA

triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8", 
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8",
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v",
                         ] # Note: Mass3p8 and 19/9 missing in early data 
triggers_mumu_noniso = [ "HLT_Mu37_TkMu27" ] # Only in late data
triggers_mumu_ss = [ "HLT_Mu18_Mu9_SameSign", # Only in late data
                     "HLT_Mu18_Mu9_SameSign_DZ", 
                     "HLT_Mu20_Mu10_SameSign", 
                     "HLT_Mu20_Mu10_SameSign_DZ" ]
triggers_mumu = triggers_mumu_iso

triggers_ee = [ "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", # Note: no-dz version missing in 2017B
                "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", ] 
triggers_ee_noniso = ["HLT_DoubleEle25_CaloIdL_MW", # 25 and 27 missing in early part of 2017
                      "HLT_DoubleEle27_CaloIdL_MW", 
                      "HLT_DoubleEle33_CaloIdL_MW" ]

triggers_mue   = [ "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",  # NoDZ version only from 2017C
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", 
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ" ] # Mu8/Ele23 w/o DZ is always prescaled

triggers_mue_noiso = [ 'HLT_Mu27_Ele37_CaloIdL_MW',
                       'HLT_Mu37_Ele27_CaloIdL_MW']

# note: all dilepton+HT are missing in the early part of the data taking (2017B)
triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT350",
                      "HLT_DoubleMu4_Mass8_DZ_PFHT350" ]
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350", 
                    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350", ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ" ]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL" ] 
triggers_3mu = [ "HLT_TripleMu_10_5_5_DZ", 
                 "HLT_TripleMu_12_10_5", 
                 #"HLT_TripleMu_5_3_3_Mass3p8to60_DCA", # 5_3_3 only in late part of the data (esp. DCA one)
                 "HLT_TripleMu_5_3_3_Mass3p8to60_DZ" ]

triggers_3mu_alt=["HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx"]

triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL" ,
                   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ" ]

triggers_1mu_iso = [ 'HLT_IsoMu24', 'HLT_IsoMu24_eta2p1', # Prescaled at high lumi
                     'HLT_IsoMu27']                          # Always unprescaled
triggers_1mu_noniso = [ 'HLT_Mu50', 'HLT_Mu55' ] # 55 only in late part of the data

triggers_1e_iso = [ "HLT_Ele32_WPTight_Gsf", # Ele32 missing in Run2017B
                    "HLT_Ele35_WPTight_Gsf" ]
triggers_1e_noniso = [ "HLT_Ele115_CaloIdVT_GsfTrkIdT"] # Not 2017B

# Prescaled lepton triggers
triggers_FR_1mu_noiso = [ "HLT_Mu%d" % pt for pt in (8,17) ] # DoubleMu PD
triggers_FR_1mu_iso = [ "HLT_Mu%d_TrkIsoVVL" % pt for pt in (8,17) ] # DoubleMu PD
triggers_FR_1mu_noiso_highpt = [ "HLT_Mu%d" % pt for pt in (20,27,50) ] + ["HLT_Mu3_PFJet40"] # SingleMu PD
triggers_FR_1e_noiso = [ "HLT_Ele%d_CaloIdM_TrackIdM_PFJet30" % pt for pt in (8,17,23) ] # SingleElectron
triggers_FR_1e_iso   = [ "HLT_Ele%d_CaloIdL_TrackIdL_IsoVL_PFJet30" % pt for pt in (8,12,23) ] # SingleElectron


# HT:
triggers_pfht1050 = ['HLT_PFHT1050']

# AK8 HT:
triggers_pfht800_mass50 = ['HLT_AK8PFHT800_TrimMass50']

# PF Jet
triggers_pfjet500 = ['HLT_AK8PFJet500']

# AK8 PF Jet
triggers_pfjet400_mass30 = ['HLT_AK8PFJet400_TrimMass30']


#lepton tau
triggers_leptau = ["HLT_IsoMu27_LooseChargedIsoPFTau20_SingleL1",
                   "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
                   "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                   "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg"]


triggers_htmet = ['HLT_PFHT500_PFMET100_PFMHT100_IDTight']

triggers_metNoMu100_mhtNoMu100=["HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60"]

triggers_met = [ 'HLT_PFMET120_PFMHT120_IDTight',
                 'HLT_PFMET120_PFMHT120_IDTight_PFHT60']

triggers_pfht = ["HLT_PFHT180",
                 "HLT_PFHT250",
                 "HLT_PFHT350",
                 "HLT_PFHT370",
                 "HLT_PFHT430",
                 "HLT_PFHT510",
                 "HLT_PFHT590",
                 "HLT_PFHT680",
                 "HLT_PFHT780",
                 "HLT_PFHT890"]
