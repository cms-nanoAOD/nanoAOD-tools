import ROOT
import ROOT.TMath as TMath
import math
import os
import optparse
import sys
 
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import PhysicsTools.NanoAODTools.postprocessing.samples.samples as losamples
import multiprocessing as mp

inputpath = "/eos/home-a/adeiorio/Wprime/nosynch/"

def getsampleslist(nfile):
    findsamples = open(str(nfile), "r")
    samples = []
    for line in findsamples:
        samples.append(line.split())
    findsamples.close()
    return samples

def repinstring(string, oldtonewdict):
    newstring = copy.deepcopy(string)
    for old, new in oldtonewdict.items():
        newstring = newstring.replace(str(old), str(new))
    return newstring

def getfilelist(sample):
    sampledir = inputpath + sample + "/"
    rootfiles = os.listdir(sampledir)
    return rootfiles
        
def checknofiles(sample, n):
    rstr = {
        "tree": "",
        "hadd": "",
        "_": "",
        ".root": ""
    }

    rootfiles = getfilelist(sample)
    numrfiles = []
    missing = []
    isEveryIn = False

    for rootfile in rootfiles:
        numrfile = repinstring(rootfile, rstr)
        try:
            k = int(numrfile)
        except:
            continue
        numrfiles.append(k)

    numrfiles.sort()
    
    if len(numrfiles) == n:
        print 'Great!'
        isEveryIn = True
    else:
        print 'Not great!'
        nomiss = 0
        for i in range(n):
            num = numrfiles[i - nomiss]
            j = i + 1
            if num != j:
                nomiss += 1
                missing.append(j)

    return isEveryIn, missing

def haddfiles(sample, size):
    pystring = "python /afs/cern.ch/work/a/apiccine/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/scripts/haddnano.py"
    rootfiles = getfilelist(sample)
    sdir = inputpath + sample + "/"
    if len(rootfiles) == 1:
        return 'hadd completed!'
    else:
        k = 0
        shelllist = []
        isEndedBefore = False

        while(not isEndedBefore):
            k += 1
            shellstring = pystring + " " + sdir + sample +"_" + str(k) + ".root"
            for i in range(size):
                try:
                    toadd = rootfiles.pop(0)
                except IndexError:
                    print toadd
                    isEndedBefore = True
                    break
                shellstring = shellstring + " " + sdir + toadd
            print shellstring
            shelllist.append(shellstring)
            
        for shellstring in shelllist:
            os.system(shellstring)

    '''    
        for process in shelllist:
    
    try:
        k = float(sample)
    except:
        print "Sample name contains not only numbers!"
        raise ValueError
    '''


samples = getsampleslist(sys.argv[1])

for sample in samples:
    areAllIn, missing = checknofiles(sample[0], int(sample[1]))
    #if not areAllIn:
    haddfiles(sample[0], 30)
