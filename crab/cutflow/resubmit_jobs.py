import fileinput, string, sys, os, time, subprocess
import argparse as arg
import multiprocessing as mp
import glob
from crab_script_cutflow_local_test import *
from functools import partial

def Get_argumets(txtfile):

	print()
	print("-----------------------------------------    chacking     --------------------------------")
	print()
	
	rerun_list = []
	cwd = os.getcwd()

	#Channels = Channel_QCD
	Error = "Killed"

	cmd_grep = 'grep "'+Error+'" '+txtfile
	print(cmd_grep)
	p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	skip_tranfer_check = False
	output = str(output)
	print(output.count(Error))
	if(output.count(Error)>=1):
		lines = output.split('Killed')
		for line in lines:
			if("python3" in line): rerun_list.append("python3 "+str(line.split('python3')[-1].split('txt')[0])+'txt')
			#print(rerun_list[-1])
			if(len(rerun_list)>=1):
				Error2 = "Done"
				newtxt = rerun_list[-1].split('&>')[1]
				cmd_grep2 = 'grep "'+Error2+'" '+newtxt
				#print(cmd_grep2)
				p2 = subprocess.Popen(cmd_grep2, stdout=subprocess.PIPE, shell=True)
				(output2, err2) = p2.communicate()
				p_status2 = p2.wait()
				skip_tranfer_check = False
				output2 = str(output2)
				if(output2.count(Error2)>=1):
					#print("DONE")
					del rerun_list[-1]
				else:
					print(rerun_list[-1])
					
		print(len(rerun_list))
		
	rerun_list.append(['Tchannel','2J1T1_el_mc_UL2017', '/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/SEVENTEEN/2J1T1/el/Tchannel/', '/nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/Tchannel/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_10_Jul23_MCUL2017_Tchannel/230710_201319/0000/tree_37.root' , 128, '/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/SEVENTEEN/2J1T1/el/Tchannel/log/log_128.txt'])	
	return rerun_list
	#print(rerun_list[0])	
	#print("runing "+str(len(rerun_list))+ " jobs .... .... ")
	
	#pool.map(run_cmd, rerun_list)

def sum(num, num2):
	print(num+num)

def run_cmd(num1,num2):
	pool = mp.Pool(processes=2)
	pool.map(partial(sum, num=1),num2)

    #os.system(run_command)

if __name__ == '__main__':
	parser = arg.ArgumentParser(description='inputs discription')  
	parser.add_argument('-f', '--file', dest='txtfile', type=str, default=['local_crab_report_mu_UL2017_2J1T1_MC.txt'], nargs=1, help="condor directory")
	
	args = parser.parse_args()
	
	if args.txtfile == None:
	    print("USAGE: %s [-h] [-f txt file]"%(sys.argv [0]))
	    exit(1) 
	
	txtfile=args.txtfile[0]
	arg_list = Get_argumets(txtfile)
	print(arg_list)
	num1=[1,2,3]
	num2=[3,4,5]
	run_cmd(num1,num2)
	