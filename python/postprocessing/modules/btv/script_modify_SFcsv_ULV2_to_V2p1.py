import fileinput, string, sys, os, time, datetime
import csv
from array import array
import math
import argparse as arg

parser = arg.ArgumentParser(description='input and output file discription')
parser.add_argument('-f', '--inout', dest='files', default=('dummy_ori_wp_deepJet_106XUL18_v2.csv',' check.csv'), type=str, nargs=2, help="input and output files ['dummy_ori_wp_deepJet_106XUL18_v2.csv','check.csv']")
args = parser.parse_args()
print(args.files[0],args.files[1])

def csv_reader_N_writter(filetoRead,filetowrite):
    OperatingPoint, measurementType, sysType, jetFlavor, etaMin, etaMax, ptMin, ptMax, discrMin, discrMax, formula = ([]  for i in range(11))
    with open(filetoRead,mode='r') as in_csv_file:
        csv_reader = csv.reader(in_csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (line_count == 0):
                line_count = 1
            else:
                OperatingPoint.append(row[0])
                measurementType.append(row[1])
                sysType.append(row[2])
                jetFlavor.append(row[3])
                etaMin.append(row[4])
                etaMax.append(row[5])
                ptMin.append(row[6])
                ptMax.append(row[7])
                discrMin.append(row[8])
                discrMax.append(row[9])
                formula.append(row[10])
                
        #print OperatingPoint ," type : ",type(OperatingPoint[0])," len: ",len(OperatingPoint)
        """print measurementType ," type : ",type(measurementType[0])
        print sysType ," type : ",type(sysType[0])
        print jetFlavor ," type : ",type(jetFlavor[0])
        print etaMin ," type : ",type(etaMin[0])
        print etaMax ," type : ",type(etaMax[0])
        print ptMin ," type : ",type(ptMin[0])
        print ptMax ," type : ",type(ptMax[0])
        print discrMin ," type : ",type(discrMin[0])
        print discrMax ," type : ",type(discrMax[0])
        print formula ," type : ",type(formula[0])"""

    with open(filetowrite, mode='w') as out_csv_file:
        csv_writer = csv.writer(out_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["OperatingPoint", "measurementType", "sysType", "jetFlavor", "etaMin", "etaMax", "ptMin", "ptMax", "discrMin", "discrMax", "formula"])
        #print "len write mode : ",len(OperatingPoint)
        for i in range(0, len(OperatingPoint)):

            if(OperatingPoint[i]=="L"):OperatingPoint[i]="0"
            elif(OperatingPoint[i]=="M"):OperatingPoint[i]="1"
            elif(OperatingPoint[i]=="T"):OperatingPoint[i]="2"
            elif(OperatingPoint[i]=="shape"):OperatingPoint[i]="3"

            if(jetFlavor[i]=="5"):jetFlavor[i]="0"
            elif(jetFlavor[i]=="4"):jetFlavor[i]="1"
            elif(jetFlavor[i]=="0"):jetFlavor[i]="2"

            pars = [OperatingPoint[i], measurementType[i], sysType[i], jetFlavor[i], etaMin[i], etaMax[i], ptMin[i], ptMax[i], discrMin[i], discrMax[i], formula[i]]
            # print(cordinate)
            csv_writer.writerow(pars) 

if __name__ == "__main__":
        csv_reader_N_writter(args.files[0],args.files[1])
