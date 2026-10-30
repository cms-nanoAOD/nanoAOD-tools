import ROOT as R
import numpy as np
import sys
import os
import glob
import argparse as arg

parser = arg.ArgumentParser(description='stack plot after BDT')
parser.add_argument('-f_in', '--inputFile', dest='InFile', default=['mc.root'], type=str, nargs=1, help="Input File with pileup hiostogram ")
parser.add_argument('-f_out', '--outputFile', dest='OutFile', default=['outputfilename.root'], type=str, nargs=1, help="Output File with all tree hiostogram ")

args = parser.parse_args()

Nomi_File = args.InFile[0]
Out_File = args.OutFile[0]

print "Nomi : ", Nomi_File
print "Out  : ", Out_File

if __name__ == "__main__":

	Nomi_file = R.TFile.Open(Nomi_File,'Read')
	Nomi_hist = Nomi_file.Get('h_mc')
        Nomi_hist.SetName('pu_mc')

	Out_file = R.TFile.Open(Out_File,'RECREATE')
	Nomi_hist.Write()
	Out_file.Close()

