import fileinput, string, sys, os, time, datetime
import csv
from array import array
import math
import argparse as arg

parser = arg.ArgumentParser(description='input discription')
parser.add_argument('-y', '--Year', dest='yeardataset', default=('2016'), type=str, nargs=1, help="Run2 year out of ['UL2016preAPV', 'UL2016postAPV','UL2017','UL2018']")
args = parser.parse_args()

if args.yeardataset[0] not in ['UL2016preAPV', 'UL2016postAPV','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()
    


year = args.yeardataset[0]
print year
#dataset = __import__(dataset_file)

if(year=="UL2016preAPV"):
	from dataset_UL2016preAPV import * 
	datasets = Datasets_MC_2016APV+Datasets_Alt_MC_2016APV+Datasets_sys_MC_2016APV+Datasets_SingleMuon_data_2016APV+Datasets_SingleElectron_data_2016APV
elif(year=="UL2016postAPV"):
        from dataset_UL2016postAPV import * 
        datasets = Datasets_MC_2016+Datasets_Alt_MC_2016+Datasets_sys_MC_2016
elif(year=="UL2017"):
        from dataset_UL2017 import * 
        datasets = Datasets_MC_2017+Datasets_Alt_MC_2017+Datasets_sys_MC_2017+Datasets_SingleMuon_data_2017+Datasets_SingleElectron_data_2017
elif(year=="UL2018"):
        from dataset_UL2018 import * 
        datasets = Datasets_MC_2018+Datasets_Alt_MC_2018+Datasets_sys_MC_2018+Datasets_SingleMuon_data_2018+Datasets_SingleElectron_data_2018
 
if __name__ == "__main__":
	for dataset in datasets:
		cmd_transfer_request = 	'rucio add-rule --ask-approval cms:'+dataset+' 1 T2_IN_TIFR --lifetime 31536000 --asynchronous'
		#os.system(cmd_transfer_request)  	
		#print cmd_transfer_request
		print dataset
