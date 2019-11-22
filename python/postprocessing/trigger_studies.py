import ROOT 

infile = ROOT.TFile.Open(".root")
tree = infile.Get("Events")
maxlen = 300000

plotpath = "/eos/user/a/adeiorio/GEMRecHit/"

#event = array( 'i', [0])
#run = array( 'i', [0])
#lumiblock = array( 'i', [0])

n_Muon = array( 'i', [0])
Muon_eta = array( 'f', maxlen*[0])
Muon_phi = array( 'f', maxlen*[0])
Muon_pt = array( 'f', maxlen*[0])
Muon_mass = array( 'f', maxlen*[0])
tree.SetBranchAddress("n_Muon", n_Muon)
tree.SetBranchAddress("Muon_eta", Muon_eta)
tree.SetBranchAddress("Muon_phi", Muon_phi)
tree.SetBranchAddress("Muon_pt", Muon_pt)
tree.SetBranchAddress("Muon_mass", Muon_mass)

n_Electron = array( 'i', [0])
Electron_eta = array( 'f', maxlen*[0])
Electron_phi = array( 'f', maxlen*[0])
Electron_pt = array( 'f', maxlen*[0])
Electron_mass = array( 'f', maxlen*[0])
tree.SetBranchAddress("n_Electron", n_Electron)
tree.SetBranchAddress("Electron_eta", Electron_eta)
tree.SetBranchAddress("Electron_phi", Electron_phi)
tree.SetBranchAddress("Electron_pt", Electron_pt)
tree.SetBranchAddress("Electron_mass", Electron_mass)

HLT_Mu50 = array( 'b', [0])
HLT_Mu55 = array( 'b', [0])
HLT_TkMu100 = array( 'b', [0])
tree.SetBranchAddress("HLT_Mu50", HLT_Mu50)
tree.SetBranchAddress("HLT_Mu55", HLT_Mu55)
tree.SetBranchAddress("HLT_TkMu100", HLT_TkMu100)
tree.SetBranchAddress("", )
tree.SetBranchAddress("", )
tree.SetBranchAddress("", )
tree.SetBranchAddress("", )
#tree.SetBranchAddress("", )

#histogram booking
muonpt = ROOT.TH1F("Muon_pt", "Muon_pt", 500, 0, 5000)

for i in xrange(0,tree.GetEntries()):
    tree.GetEntry(i)
    for j in xrange(0, n_Muon):
