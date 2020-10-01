#!/usr/bin/env python
# imported from https://github.com/CERN-PH-CMG/cmg-cmssw/blob/0c11a5a0a15c4c3e1a648c9707b06b08b747b0c0/PhysicsTools/Heppy/scripts/heppy_report.py
from optparse import OptionParser
import json
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


def root2map(tree):
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("run", 1)
    tree.SetBranchStatus("luminosityBlock", 1)
    jsonind = {}
    for e in range(tree.GetEntries()):
        tree.GetEntry(e)
        run, lumi = tree.run, tree.luminosityBlock
        if run not in jsonind:
            jsonind[run] = [lumi]
        else:
            jsonind[run].append(lumi)
    # remove duplicates
    for run in jsonind:
        jsonind[run] = list(set(jsonind[run]))

    nruns = len(jsonind)
    nlumis = sum(len(v) for v in jsonind.values())
    jsonmap = {}
    for r, lumis in jsonind.items():
        if len(lumis) == 0:
            continue  # shouldn't happen
        lumis.sort()
        ranges = [[lumis[0], lumis[0]]]
        for lumi in lumis[1:]:
            if lumi == ranges[-1][1] + 1:
                ranges[-1][1] = lumi
            else:
                ranges.append([lumi, lumi])
        jsonmap[r] = ranges
    return (jsonmap, nruns, nlumis)


if __name__ == '__main__':
    parser = OptionParser(usage='%prog [options] nanoAOD-files',
                          description='Check the output of the LuminosityBlocks and produce a json file of the processed runs and lumisections')
    parser.add_option("-t", "--tree", dest="treeName", default="LuminosityBlocks",
                      help="Name of the TTree with the luminosity blocks")
    parser.add_option("-o", "--out", dest="outputFile",
                      default="lumiSummary.json", help="Name of the output file")
    (options, args) = parser.parse_args()
    if len(args) == 0:
        print('provide at least one input file in argument. Use -h to display help')
        exit()
    chain = ROOT.TChain(options.treeName)
    for a in args:
        chain.Add(a)
    summary = root2map(chain)
    if summary:
        jmap, runs, lumis = summary
        json.dump(jmap, open(options.outputFile, 'w'))
        print("Saved %s (%d runs, %d lumis)" % (options.outputFile, runs, lumis))
