import fileinput, string, sys, os, time, subprocess, shutil
from inputpaths_2J1T1_el_mu import *

filepaths = file_paths 
for i in range(0,len(filepaths)):
	line = filepaths[i]
	#os.mkdir("temp")
	#os.chdir("temp")
	#cmd_cp = "cp ../hadd* ."
	#os.system(cmd_cp)

	a, b, c, d,e,f,g,h,i,j ,k = line.split("/",10)
	pwd = os.getcwd()
	cmd_crab_report = "./hadd.sh "+ line.strip() +" "+pwd+" Minitree_"+j+"_"+i
	print cmd_crab_report 
	#os.system(cmd_crab_report)

	#cmd_ls = "ls -ltr"
	#os.system(cmd_ls)

	cmd_mv = "mv Minitree* ../"
	#os.system(cmd_mv)

	#os.chdir("..")
	#shutil.rmtree("temp")
#from input_paths import *
