#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
import sys
import re
import PSet
print "ARGV:",sys.argv
JobNumber=sys.argv[1]
crabFiles=PSet.process.source.fileNames
print crabFiles
firstInput = crabFiles[0]
tested=False
forceaaa=False
print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
for i in xrange(0,len(crabFiles)) :
     if os.getenv("GLIDECLIENT_Group","") != "overflow" and  os.getenv("GLIDECLIENT_Group","") != "overflow_conservative" and not forceaaa:
       print "Data is local"
       pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read()
       pfn=re.sub("\n","",pfn)
       print crabFiles[i],"->",pfn
       if not tested:
         print "Testing file open"
         import ROOT
         testfile=ROOT.TFile.Open(pfn)
         if testfile and testfile.IsOpen() :
            print "Test OK"
            crabFiles[i]=pfn
            testfile.Close()
            #tested=True
         else :
            print "Test open failed, forcing AAA"
            crabFiles[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]
            forceaaa=True
       else :
            crabFiles[i]=pfn


     else:
       print "Data is not local, using AAA/xrootd"
       crabFiles[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]

from  PhysicsTools.NanoAODTools.postprocessing.examples.mhtProducer import *
p=PostProcessor("Output/",crabFiles,"Jet_pt>200",modules=[mht()],provenance=True)
p.run()
print "DONE"
#print PSet.process.output.fileName
os.system("ls -lR")
os.system("./haddnano.py tree.root Output/*.root")
#os.system("mv Output/*.root tree.root")
os.system("ls -lR")

import ROOT
f=ROOT.TFile.Open('tree.root')
entries=1 #f.Get('Events').GetEntries()

fwkreport='''<FrameworkJobReport>
<ReadBranches>
</ReadBranches>
<PerformanceReport>
  <PerformanceSummary Metric="StorageStatistics">
    <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
    <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
    <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
    <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
    <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
    <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
  </PerformanceSummary>
</PerformanceReport>

<GeneratorInfo>
</GeneratorInfo>

<InputFile>
<LFN>%s</LFN>
<PFN></PFN>
<Catalog></Catalog>
<InputType>primaryFiles</InputType>
<ModuleLabel>source</ModuleLabel>
<GUID></GUID>
<InputSourceClass>PoolSource</InputSourceClass>
<EventsRead>1</EventsRead>
<Runs>
<Run ID="1">
   <LumiSection ID="47805"/>
</Run>

</Runs>

</InputFile>

<File>
<LFN></LFN>
<PFN>tree.root</PFN>
<Catalog></Catalog>
<ModuleLabel>HEPPY</ModuleLabel>
<GUID></GUID>
<OutputModuleClass>PoolOutputModule</OutputModuleClass>
<TotalEvents>%s</TotalEvents>
<DataType></DataType>

<BranchHash>dc90308e392b2fa1e0eff46acbfa24bc</BranchHash>

<Runs>
<Run ID="1">
   <LumiSection ID="47805" NEvents="0"/>
</Run>

</Runs>

</File>

</FrameworkJobReport>''' % (firstInput,entries)

f1=open('./FrameworkJobReport.xml', 'w+')
f1.write(fwkreport)
