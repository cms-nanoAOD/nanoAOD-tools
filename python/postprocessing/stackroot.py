import ROOT
import ROOT.TMath as TMath
import math
import os
import optparse
import sys
#from os import path
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import PhysicsTools.NanoAODTools.postprocessing.samples.samples as losamples

ROOT.gROOT.SetBatch()

class variabile(object):
    def __init__(self, name, title, taglio, nbins, xmin, xmax):
        self._name = name
        self._title = title
        self._cut = taglio
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax

    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)

def cutToTag(cut):
    newstring = cut.replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("((", "[").replace("))", "]").replace("(","").replace(")","").replace("==","_EQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

lumi = {
    "2016": 35.9,
    "2017": 4.82,#41.53, <- overall integrated luminosity!
    "2018": 57.3,
}

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/"
findsamples = open(str(sys.argv[1]), "r")
findplots = open(str(sys.argv[2]), "r")

samples = []
plots = []

for line in findsamples:
    samples.append(line.split())

for line in findplots:
    plots.append(line.split())

findsamples.close()
findplots.close()

for sample in samples:
    sampledir = inputpath + sample[0] + "/"
    rootfiles = os.listdir(sampledir)
    print "Sample: " + sampledir
    sobj = "losamples."+sample[0]
    x = "scard"
    exec("%s = %s" % (x, sobj))

    histos = []

    for plot in plots:
        var = None
        hlist = None
        name = "h_" + plot[0]
        title = plot[0]
        cut = None
        if plot[1] == 'nocut':
            cut = ""
        else:
            cut = plot[1]
            name = name + "_" + cutToTag(cut)
        nbins = int(float(plot[2]))
        nmin = float(plot[3])
        nmax = float(plot[4])
        var = variabile(name, title, cut, nbins, nmin, nmax)
        hlist = []
        hlist.append(copy.deepcopy(var))
        hlist.append(ROOT.TH1F(name, title, nbins, nmin, nmax))
        histos.append(copy.deepcopy(hlist))
        hlist = None

    for k, rootfile in enumerate(rootfiles):
        if k > 0:
            break
        print "\trootfile #%i" % (k)
        infile = ROOT.TFile.Open(sampledir + rootfile)        
        tree = InputTree(infile.Events)
        nentries = tree.GetEntries()
        #for h in histos:
            #print h[1], h[1].GetEntries()
        
        for i in xrange(0, nentries):
            
            if (i % int(nentries/20)) == 0:
                perc = float(i)/float(nentries) * 100.
                sys.stdout.write("\r\t\tPercentage wrt total: {0}%".format(math.ceil(perc)))
                sys.stdout.flush()
            event = Event(tree,i)
            electrons = Collection(event, "Electron")
            muons = Collection(event, "Muon")
            jets = Collection(event, "Jet")
            PV = Object(event, "PV")
            #goodMu = get_Mu(muons)
            #goodEle = get_Ele(electrons)
            goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)

            if sample[1] == 'mu' or sample[1] == 'muon':
                if not isMu:#(len(goodMu) > 0 and len(goodEle) == 0):
                    continue
            elif sample[1] == 'ele' or sample[1] == 'electron':
                if not isEle:#(len(goodMu) == 0 and len(goodEle) > 0):
                    continue

            for h in histos:
                htemp = None
                newname = "htemp_" + h[0]._title
                htemp = h[1].Clone(newname)
                htemp.Reset()
                tree.Project(newname, str(h[0]._title), str(h[0]._cut), "HIST", 1, i)
                h[1].Add(htemp)
                htemp = None

        infile.Close()
        print "rootfile closed"

    if 'Data' not in sample[0]:
        for h in histos:
            print "\tBefore scaling: " + str(h[1].GetEntries())
            scalefac = 1. / h[1].GetEntries()
            for k, v in lumi.items():
                if k in rootfile:
                    scalefac = scalefac*v
                    break
            scalefac = scalefac * scard.sigma * 1000.
            h[1].Scale(scalefac)
            print "\tAfter scaling: " + str(h[1].GetEntries())
    outname = sample[0]+'_'+sample[1]
    print "\tSaving " + outname#sample[0], sample[1]#outname
    save_hist(outname, "Plots", h[1])

        

'''
usage:
python stackroot.py samples.txt plots.txt
'''
