import math
import ROOT
import numpy as np
from foxwol_n_fourmomentumSolver import solveNu4Momentum
import multiprocessing as mp

def calculate_top_quark_momentum(MuonPt, MuonEta, MuonPhi, MuonM, met, metphi, bJetMass, bJetPt, bJetEta, bJetPhi):
    # Step 1: Create Muon 4-momentum (muon4V)
    muon4V = ROOT.TLorentzVector()
    muon4V.SetPtEtaPhiM(MuonPt, MuonEta, MuonPhi, MuonM)

    # Step 2: Calculate Px and Py for neutrino from met and metphi
    Px_nu = met * math.cos(metphi)
    Py_nu = met * math.sin(metphi)

    # Step 3: Solve for the neutrino 4-momentum (neutrino4V) using the provided solver
    neutrino4V = solveNu4Momentum(muon4V, Px_nu, Py_nu)

    # Step 4: Calculate the W boson 4-momentum (w4V) by adding muon and neutrino 4-momenta
    w4V = muon4V + neutrino4V

    # Step 5: Create b-quark 4-momentum (bquark4V)
    bquark4V = ROOT.TLorentzVector()
    bquark4V.SetPtEtaPhiM(bJetPt, bJetEta, bJetPhi, bJetMass)

    # Step 6: Calculate the top quark 4-momentum (top4V) by adding W boson and b-quark 4-momenta
    top4V = w4V + bquark4V

    return top4V

def process_channel(args):
    year, channel, out_dir, lep = args

    year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}
    #file_path = f"/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/{year_folder[year]}/2J1T1/Minitree_{channel}_2J1T1_{lep}.root"
    file_path = f"/nfs/home/common/RUN2_UL/Minitree_corr_bweight/{year_folder[year]}/2J1T1/Minitree_{channel}_2J1T1_{lep}.root"
    root_file = ROOT.TFile.Open(file_path)

    tree = root_file.Get("Events")

    sys_names = ['AbsoluteStat', 'AbsoluteMPFBias', 'Fragmentation', 'SinglePionECAL', 'SinglePionHCAL',
                  'TimePtEta', 'RelativeJEREC1', 'RelativeJEREC2', 'RelativeJERHF', 'RelativePtBB',
                  'RelativePtEC1', 'RelativePtEC2', 'RelativePtHF', 'RelativeBal', 'RelativeSample',
                  'RelativeFSR', 'RelativeStatEC', 'RelativeStatHF', 'PileUpDataMC', 'PileUpPtRef',
                  'PileUpPtBB', 'PileUpPtEC1', 'PileUpPtEC2', 'PileUpPtHF']

    sys_name2 = ["AbsoluteScale", "FlavorQCD", "RelativeStatFSR" ]


    # Disable all branches initially
    tree.SetBranchStatus("*", 0)

    # Enable only the branches you need
    required_branches_el = ["ElectronPt", "ElectronEta", "ElectronPhi", "ElectronMass"]
    required_branches_mu = ["MuonPt", "MuonEta", "MuonPhi", "MuonMass"]
    required_branches= [ "nbjet_sel", "Jet_eta", "Jet_phi" ] + required_branches_el if "el" in lep else [ "nbjet_sel", "Jet_eta", "Jet_phi" ] + required_branches_mu
    #print(required_branches)

    # Add systematic-specific branches
    for sys in sys_names:
        for direction in ['Up', 'Down']:
            required_branches.append(f"Jet_pt_jes{sys}{direction}")
            required_branches.append(f"Jet_mass_jes{sys}{direction}")
            required_branches.append(f"MET_T1_pt_jes{sys}{direction}")
            required_branches.append(f"MET_T1_phi_jes{sys}{direction}")
            required_branches.append(f"bWeight_jes_variation_up")
            required_branches.append(f"bWeight_jes_variation_down")

    # Enable the required branches
    for branch in required_branches:
        tree.SetBranchStatus(branch, 1)
    output_file_name = f"{out_dir}/JERJEStree_{year}_{channel}_2J1T1_{lep}.root"
    output_file = ROOT.TFile(output_file_name, "RECREATE")
    output_tree = ROOT.TTree("Events", "JER JES systematics")

    # Dynamically create branches for each systematic
    branches = {}
    for sys in sys_names:
        for direction in ['Up', 'Down']:
            suffix = f"_jes{sys}{direction}"
            branches[f"topPt{suffix}"] = np.zeros(1, dtype=float)
            branches[f"topPhi{suffix}"] = np.zeros(1, dtype=float)
            branches[f"topEta{suffix}"] = np.zeros(1, dtype=float)
            branches[f"topMass{suffix}"] = np.zeros(1, dtype=float)
            branches[f"topEnergy{suffix}"] = np.zeros(1, dtype=float)

            branches[f"bWeight{suffix}"] = np.zeros(1, dtype=float)

            output_tree.Branch(f"topPt{suffix}", branches[f"topPt{suffix}"], f"topPt{suffix}/D")
            output_tree.Branch(f"topPhi{suffix}", branches[f"topPhi{suffix}"], f"topPhi{suffix}/D")
            output_tree.Branch(f"topEta{suffix}", branches[f"topEta{suffix}"], f"topEta{suffix}/D")
            output_tree.Branch(f"topMass{suffix}", branches[f"topMass{suffix}"], f"topMass{suffix}/D")
            output_tree.Branch(f"topEnergy{suffix}", branches[f"topEnergy{suffix}"], f"topEnergy{suffix}/D")

            output_tree.Branch(f"bWeight{suffix}", branches[f"bWeight{suffix}"], f"bWeight{suffix}/D")
    

    for i, event in enumerate(tree):
        if i >= 10:  # Process only the first 10 entries
           break
        lepton_pt = event.ElectronPt if "el" in lep else event.MuonPt
        lepton_eta = event.ElectronEta if "el" in lep else event.MuonEta
        lepton_phi = event.ElectronPhi if "el" in lep else event.MuonPhi
        lepton_mass = event.ElectronMass if "el" in lep else event.MuonMass

        b_jet_idx = event.nbjet_sel
        bJet_eta = getattr(event, f"Jet_eta")[b_jet_idx]
        bJet_phi = getattr(event, f"Jet_phi")[b_jet_idx]
        for isys,sys in enumerate(sys_names):
            bweight_Up = getattr(event,f"bWeight_jes_variation_up")[isys]
            bweight_Down = getattr(event,f"bWeight_jes_variation_down")[isys]
            for direction in ['Up', 'Down']:
                suffix = f"_jes{sys}{direction}"
                print(f"{suffix = }")
                bJet_pt = getattr(event, f"Jet_pt_jes{sys}{direction}")[b_jet_idx]
                bJet_mass = getattr(event, f"Jet_mass_jes{sys}{direction}")[b_jet_idx]
                
                

                met = getattr(event, f"MET_T1_pt_jes{sys}{direction}")
                metphi = getattr(event, f"MET_T1_phi_jes{sys}{direction}")
                

                top4v = calculate_top_quark_momentum(lepton_pt, lepton_eta, lepton_phi, lepton_mass, met, metphi, bJet_mass, bJet_pt, bJet_eta, bJet_phi)
                print(f"{top4v.Pt() = }",f"{top4v.M() = }")
                branches[f"topPt{suffix}"][0] = top4v.Pt()
                branches[f"topPhi{suffix}"][0] = top4v.Phi()
                branches[f"topEta{suffix}"][0] = top4v.Eta()
                branches[f"topMass{suffix}"][0] = top4v.M()
                branches[f"topEnergy{suffix}"][0] = top4v.E()

                branches[f"bWeight{suffix}"][0] = bweight_Up if direction == "Up" else bweight_Down


        output_tree.Fill()

    root_file.Close()
    output_file.Write()
    output_file.Close()
    
    print(f"All systematics saved to the same {output_file_name}  file with separate branches.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process systematic variations.')
    parser.add_argument('-y', '--year', dest='year', type=str, default='UL2018', help="  UL2017 UL2016preVFP UL2016postVFP UL2018 ")
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default='./', help="Output directory")
    parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='mu', help=" el for electron and mu for muon")


    args = parser.parse_args()
    year = args.year
    out_dir = args.out_dir
    lep = args.lepton

    channels = ['Tchannel']#,'Tbarchannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','tw_antitop', 
                #'tw_top','Schannel','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WZTo2Q2L', 
                #'ZZTo2Q2L','DYJetsToLL','QCD'] # 'WWTolnulnu',

    tasks = [(year, channel, out_dir, lep) for channel in channels]
    with mp.Pool(processes=len(channels)) as pool:
        pool.map(process_channel, tasks)

