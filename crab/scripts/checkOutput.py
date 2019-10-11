version = "PROD_2_0"
folder = "/home/users/sdonato/scratchssd/fileSkimFromNanoAOD"

import os

from datasetFileCount import datasetFileCount as datasetFileDAS

from datasets2016 import data2016, mc2016
from datasets2017 import data2017, mc2017
from datasets2018 import data2018, mc2018
datasetsNames = ["data2018", "mc2018", "data2017", "mc2017", "data2016", "mc2016"]

from checker import checkDatasets
checkDatasets(datasetsNames, globals())

for datasetsName in datasetsNames:
    datasets = globals()[datasetsName]
    samples = datasets.keys()
    for sample in samples:
        print "#### SAMPLE: %s #### "%sample
        sampleFolder = folder + "/" + version + "/" + sample
        print sampleFolder
        for dataset in datasets[sample]:
            datasetPrimary = dataset.split("/")[1]
            datasetTag = dataset.split("/")[2]                
            command = 'ls  %s | grep %s | grep %s | wc -l '%(sampleFolder, datasetPrimary, datasetTag)
#            print command
            countLocal = int(os.popen ( command ).read().split("\n")[0])
            countDAS = datasetFileDAS[dataset]
            print "Done: %.1f\tDAS: %d\tLOCAL: %d. Dataset: %s"%(100.*countLocal/countDAS, countDAS, countLocal,dataset)
            
