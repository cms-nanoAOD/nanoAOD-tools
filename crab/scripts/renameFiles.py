import subprocess
import os

nprocesses = 10

from datasets2016 import data2016, mc2016
from datasets2017 import data2017, mc2017
from datasets2018 import data2018, mc2018

datasetsNames = ["data2018", "mc2018", "data2017", "mc2017", "data2016", "mc2016"]

from checker import checkDatasets
checkDatasets(datasetsNames, globals())

server = "t2-xrdcms.lnl.infn.it:7070"
haddPath = "/home/users/sdonato/scratchssd/Skim/CMSSW_10_2_6/src/PhysicsTools/NanoAODTools/scripts/haddnano.py"

version = "PROD_2_0"
folder = "/home/users/sdonato/scratchssd/fileSkimFromNanoAOD"
#suffix = "_nano"+Y+".root"
#year = "_" + Y
#suffix = ".root"
#year = "

outputFolder = folder + "/" + version

os.system("mkdir -p %s"%outputFolder)

allSamples = []
for datasetsName in datasetsNames:
    datasets = globals()[datasetsName]
    suffix = "_nano%s"%datasetsName[-4:]
    samples = datasets.keys()
    for sample in samples:
        command = "mv  %s/%s.root %s/%s_%s.root "%(outputFolder,sample,outputFolder,sample,suffix)
        print command
#        os.popen ( command )
