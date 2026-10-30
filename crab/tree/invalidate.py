import fileinput, string, sys, os, time

Datasets = ['/SingleElectron/mikumar-Tree_october_Seventeen_Run2016B_vert2_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016C_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016D_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016E_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016F_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016G_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016H_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER']

"""from dataset_UL2016preVFP_phy3_to_invalidate import *
Datasets = Datasets_SingleElectron_data_UL2016APV
RequestName = Datasets.keys()

print Datasets"""

cms_source_crab3 = "source /cvmfs/cms.cern.ch/crab3/crab.sh"
os.system(cms_source_crab3)

for i in range(0,len(Datasets)):  #RequestName:  #range(0,len(Datasets)):
    cmd_crab_invalidate = "python $DBS3_CLIENT_ROOT/examples/DataOpsScripts/DBS3SetDatasetStatus.py --url=https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter --status=INVALID --recursive=False --dataset="+Datasets[i] #[0]
    os.system(cmd_crab_invalidate)
