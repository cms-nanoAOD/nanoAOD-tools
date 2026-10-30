import ROOT as R
import numpy as np
import sys
import os
import glob
import argparse as arg

parser = arg.ArgumentParser(description='stack plot after BDT')
parser.add_argument('-f_in', '--inputFile', dest='InFile', default=['Nomi.root','up.root','down.root'], type=str, nargs=3, help="Input File with Nominal, up variation, and down variation of pileup hiostogram in same order")
parser.add_argument('-f_out', '--outputFile', dest='OutFile', default=['outputfilename.root'], type=str, nargs=1, help="Output File with all tree hiostogram ")

args = parser.parse_args()

Nomi_File = args.InFile[0]
Up_File = args.InFile[1]
Down_File = args.InFile[2]
Out_File = args.OutFile[0]

print "Nomi : ", Nomi_File
print "Up   : ", Up_File
print "Down : ", Down_File
print "Out  : ", Out_File

if __name__ == "__main__":

	Nomi_file = R.TFile.Open(Nomi_File,'Read')
	Nomi_hist = Nomi_file.Get('pileup')

	Up_file	= R.TFile.Open(Up_File,'Read')
	Up_hist = Up_file.Get('pileup')
	Up_hist.SetName('pileup_plus')
	Up_hist.SetLineColor(R.kRed)

	Down_file = R.TFile.Open(Down_File,'Read')
        Down_hist = Down_file.Get('pileup')
        Down_hist.SetName('pileup_minus')
	Down_hist.SetLineColor(R.kGreen)

	Out_file = R.TFile.Open(Out_File,'RECREATE')
	Nomi_hist.Write()
	Up_hist.Write()
	Down_hist.Write()
	Out_file.Close()

