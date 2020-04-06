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
import multiprocessing as mp

ROOT.gROOT.SetBatch()

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/"
lumi = {
    "2016": 35.9,
    "2017": 4.82,#41.53, <- overall integrated luminosity!
    "2018": 57.3,
}

results = []

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
    newstring = cut.replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("((", "_").replace("))", "_").replace("(","").replace(")","").replace("==","_EQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_").replace("-", "neg")
    return newstring

def collect_result(result):
    global results
    results.append(result)

def getsampleslist(nfile):
    findsamples = open(str(nfile), "r")
    samples = []
    for line in findsamples:
        samples.append(line.split())
    findsamples.close()
    return samples

def getplotslist(nfile):
    findplots = open(str(nfile), "r")
    plots = []
    for line in findplots:
        plots.append(line.split())
    findplots.close()
    return plots

def createhlist(plot):
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
    return hlist
        
def projectperevent(sample, plot):
    h = None
    h = createhlist(plot) 

    sampledir = inputpath + sample[0] + "/"
    rootfiles = os.listdir(sampledir)
    print "Sample: " + sampledir
    print rootfiles
    scard = None
    if 'Data' not in sample[0]:
        sobj = "losamples."+sample[0]
        x = "scard"
        exec("%s = %s" % (x, sobj))

    for k, rootfile in enumerate(rootfiles):
        print "\trootfile #%i" % (k)
        infile = ROOT.TFile.Open(sampledir + rootfile)        
        tree = InputTree(infile.Events)
        nentries = tree.GetEntries()
        
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
            goodEvt, isMu, isEle = presel(PV, muons, electrons, jets)

            if sample[1] == 'mu' or sample[1] == 'muon':
                if not isMu:
                    continue
            elif sample[1] == 'ele' or sample[1] == 'electron':
                if not isEle:
                    continue
                
            htemp = None
            newname = "htemp_" + h[0]._title
            htemp = h[1].Clone(newname)
            htemp.Reset()
            tree.Project(newname, str(h[0]._title), str(h[0]._cut), "HIST", 1, i)
            h[1].Add(htemp)
            htemp = None

        infile.Close()
        print "\trootfile closed"

    if 'Data' not in sample[0]:
        print h[1].GetEntries()
        scalefac = 1. / h[1].GetEntries()
        for k, v in lumi.items():
            if k in sample[0]:
                scalefac = scalefac*v
                break
        scalefac = scalefac * scard.sigma * 1000.
        h[1].Scale(scalefac)
        print scalefac, h[1].GetEntries()
        
    outname = sample[0]+'_'+sample[1]
    return [h[1], outname]

pool = mp.Pool(mp.cpu_count())

samples = getsampleslist(sys.argv[1])
plots = getplotslist(sys.argv[2])    
for sample in samples:
    for plot in plots:
        pool.apply_async(projectperevent, args=(sample, plot), callback=collect_result)

pool.close()
pool.join()

for result in results:
    print result[0], result[1]
    save_hist(result[1], "Plots_par", result[0])

'''
pool = mp.Pool(mp.cpu_count())
f = pool.map_async(createplots, [sample for sample in samples])
pool.close()
print f


print "\tSaving " + outname#sample[0], sample[1]#outname
save_hist(outname, "Plots", h[1])

return None

usage:
python stackroot.py samples.txt plots.txt
'''
