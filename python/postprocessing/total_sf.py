import os
import sys
import ROOT
import math
import copy
from array import array

ROOT.gROOT.SetBatch()

def lumitot(sample, lumi_dict):
    lumi = 0.
    for k, v in lumi_dict.items():
        if k in sample:
            lumi = lumi + v
    return lumi

inpdir = "./data/leptonSF/"

lumi = {
    'B': 5.8,
    'C': 2.6,
    'D': 4.2,
    'E': 4.0,
    'F': 3.1,
    'G': 7.5,
    'H': 8.6,
}

mu_f = {
    "Mu_RunBCDEF_SF_ID_2016_syst.root": ["BCDEF", 0.],
    "Mu_RunGH_SF_ID_2016_syst.root": ["GH", 0.],
}

for k in mu_f.keys():
    mu_f[k][1] = round(lumitot(mu_f[k][0], lumi), 2)

tot_lumi = round(lumitot("BCDEFGH", lumi), 2)

mu_h = [
    "NUM_TightID_DEN_genTracks_eta_pt",
]

h_tosum = []
#h_tot = ROOT.TH1F()

for f in mu_f.keys():
    tempfile = ROOT.TFile.Open(str(inpdir + f))
    for h in mu_h:
        temphist = None
        tempdict = None
        weight = None
        temphist = tempfile.Get(str(h))
        temphist.SetName(temphist.GetName() + "_" + mu_f[f][0])
        temphist.SetTitle(temphist.GetTitle() + "_" + mu_f[f][0])
        weight = mu_f[f][1]/tot_lumi
        tempdict = [copy.deepcopy(temphist), weight]
        h_tosum.append(copy.deepcopy(tempdict))
    tempfile.Close()

h_tot = copy.deepcopy(h_tosum[0][0])

for v in mu_f.values():
    delname = "_" + v[0] 
    h_tot.SetName(str(h_tot.GetName()).replace(delname, ""))
    h_tot.SetTitle(str(h_tot.GetTitle()).replace(delname, ""))

h_tot.Reset()

print h_tosum

for i in range(1, h_tot.GetNbinsX()+1):
    for j in range(1, h_tot.GetNbinsY()+1):
        bc_tot = 0.
        berr_tot = 0.
        for x in range(len(h_tosum)):
            bc_tot = bc_tot + h_tosum[x][1] * h_tosum[x][0].GetBinContent(i, j)
            berr_tot = berr_tot + h_tosum[x][1]**2. * h_tosum[x][0].GetBinError(i, j)**2.

        h_tot.SetBinContent(i, j, bc_tot)

        berr_tot = berr_tot**0.5
        h_tot.SetBinError(i, j, berr_tot)

totrun = ""
for v in mu_f.values():
    totrun = totrun + str(v[0])

outname = None

for key, value in mu_f.items():
    outname = key.replace(str(value[0]), totrun)
    break

outname = inpdir + outname

outfile = ROOT.TFile(outname, "RECREATE")

h_tot.Write()
outfile.Close()

