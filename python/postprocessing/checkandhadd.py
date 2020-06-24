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

def repinstring(string, oldtonewdict):
    newstring = copy.deepcopy(string)
    for old, new in oldtonewdict.items():
        newstring = newstring.replace(str(old), str(new))
    return newstring

def getfilelist(sampledir):
    print sampledir
    files = [fil for fil in os.listdir(sampledir) if os.path.isfile(os.path.join(sampledir, fil))]
    return files
        
def checknofiles(sample, n):
    rstr = {
        "tree": "",
        "hadd": "",
        "_": "",
        ".root": ""
    }

    sampledir = inputpath + sample
    rootfiles = getfilelist(sampledir)
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

def stringtoshell(command):
    os.system(command)

def haddfiles(sample, size):
    pystring = ''
    if 'Data' in sample[0]:
        pystring = "nohup python /afs/cern.ch/work/a/apiccine/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/scripts/haddnano.py "
    else:
        pystring = "nohup hadd -f "
    sampledir = inputpath + sample[0] + "/merged2/"
    print sampledir
    rootfiles = getfilelist(sampledir)
    print rootfiles
    sdir = inputpath + sample[0] + "/merged2/"
    
    print rootfiles
    
    '''
    for t, rootfile in enumerate(rootfiles):
        if 'tree_hadd' in rootfile:
            rootfiles.pop(t)
        #if t >= 200:
            #rootfiles.pop(t)
    print rootfiles
    '''

    if len(rootfiles) == 1:
        return 'hadd completed!'
    
    k = 0
    shelllist = []
    isEndedBefore = False

    while(not isEndedBefore):
        k += 1
        #print "dim: ", len(rootfiles), sample[1]        
        shellstring = pystring + " " + sdir + "merged/" + sample[0]
        if len(rootfiles) < size and k == 1:
            shellstring = shellstring + ".root"
            isEndedBefore = True
        else:
            shellstring = shellstring +"_" + str(k) + ".root"

        for i in range(size):
            try:
                toadd = rootfiles.pop(0)
            except IndexError:
                isEndedBefore = True
                break
            shellstring = shellstring + " " + sdir + toadd
        
        print shellstring
        shellstring = shellstring +  " > " + sample[0] +".out 2> " + sample[0] + "_err.err &"
        shelllist.append(shellstring)
 
    for shellstring in shelllist:
        stringtoshell(shellstring)

    return "Great!"
    
samples = getsampleslist(sys.argv[1])
results = []

#pool = mp.Pool(mp.cpu_count())

for sample in samples:
    print sample
    areAllIn, missing = checknofiles(sample[0], int(sample[1]))
    print "ok1"
   
    #if "Data" in sample[0]:
        #pool.apply_async(haddfiles, args=(sample, 60), callback=collect_result)
    #else:
        #pool.apply_async(haddfiles, args=(sample, 10), callback=collect_result)
   
    haddfiles(sample, 2)


#pool.close()
#pool.join()

