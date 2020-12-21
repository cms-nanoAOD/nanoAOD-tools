import ROOT

infile = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv7/Wprimetotb_M6000W600_RH_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/260000/E12988B6-429A-8543-8BCC-AA3C52D09028.root")
tree = infile.Get("Events")

cut_str = ''
cut_str_highpt = ''
print(tree.GetEntries())
LHE = "abs(LHEPart_pdgId[4])==13"
cut_str += LHE
cut_str_highpt += LHE
print("Requiring a LHE muon")
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
met = '&&(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter)'
hlt = "&&(HLT_PFHT800 || HLT_PFHT900 || HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon175 || HLT_Ele27_WPTight_Gsf)"
cut_str += met + hlt
cut_str_highpt += met + hlt
print("MET Filters and HLT requirements")
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
PV = '&&(PV_ndof>4 && abs(PV_z)<20 && sqrt(PV_x^2+PV_y^2)<2)'
cut_str += PV
cut_str_highpt += PV
print('Requiring good PV')
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
muon_high = '&&(Muon_highPtId[0] == 2 && Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)'
muon_tight = '&&(Muon_tightId[0] && Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)'
cut_str += muon_tight
cut_str_highpt += muon_high
print('Requiring one tight/Highpt muon')
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
#loose_mu = '&&(nMuon==1 || !(Muon_looseId[1] && Muon_pt[1] > 35 && Muon_miniPFRelIso_all[1] < 0.4 && abs(Muon_eta[1]) < 2.4))'
#loose_ele = '&&(nElectron==0 || !(Electron_mvaFall17V2noIso_WPL[0] && Electron_pt[0] > 35 && Electron_miniPFRelIso_all[0] < 0.4 && abs(Electron_eta[0]) < 2.4))'
#cut_str += loose_mu + loose_ele
#cut_str_highpt += loose_mu + loose_ele
#print('Vetoing additional leptons')
#print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
jets = '&&(Jet_jetId[0] >= 2 && Jet_jetId[1] >= 2 && abs(Jet_eta[0]) < 2.4 && abs(Jet_eta[1]) < 2.4 && Jet_pt[0] > 100 && Jet_pt[1] > 100)'
fatjets = '&&(nFatJet > 1)'
cut_str += jets + fatjets
cut_str_highpt += jets+ fatjets
print('Adding jets')
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
muonpt = '&&(Muon_pt[0] > 55)'
cut_str += muonpt
cut_str_highpt += muonpt
print('Requiring muon pt > 55 ')
print(cut_str, cut_str_highpt)
print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))



