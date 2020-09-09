import ROOT as r

path = './'
filename = 'Wprimetotb_M2000W200_LH_SMINTER'

def analyzer(filename):
    rf = r.TFile.Open(filename + '.root')
    tree = rf.Get("t")
    evt = 0
    pre_evt = 0
    b_W = r.TLorentzVector()
    b_t = r.TLorentzVector()
    top = r.TLorentzVector()
    mbb = r.TH1F("mbb", "b-jets system mass", 100, 0, 1000)
    bpt = r.TH1F("bpt", "W' b-jet pt", 100, 0, 1000)
    mtb = r.TH1F("mtb", "tb system mass", 500, 0, 5000)
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        evt = tree.event
        if not(evt == pre_evt):
            W = b_W + top
            bb = b_t + b_W 
            mtb.Fill(W.M())
            mbb.Fill(bb.M())
        if (abs(tree.id) == 5):
            if(tree.parent1 == 1 or tree.parent1 == 1):
                bpt.Fill(tree.p4.Pt())
                b_W.SetPtEtaPhiM(tree.p4.Pt(), tree.p4.Eta(), tree.p4.Phi(), tree.p4.M())
            else:
                b_t.SetPtEtaPhiM(tree.p4.Pt(), tree.p4.Eta(), tree.p4.Phi(), tree.p4.M())
        if (abs(tree.id) == 6):
            if(tree.parent1 == 1 or tree.parent1 == 1):
                top.SetPtEtaPhiM(tree.p4.Pt(), tree.p4.Eta(), tree.p4.Phi(), tree.p4.M())

        pre_evt = tree.event

    rfout = r.TFile(filename + '_out.root', 'RECREATE')
    mbb.Write()
    mtb.Write()
    bpt.Write()
    rfout.Close()

if __name__ == "__main__":

    analyzer(path+filename)
