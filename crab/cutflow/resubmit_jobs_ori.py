import fileinput, string, sys, os, time, subprocess
import argparse as arg
import multiprocessing as mp
import glob

def run_cmd(run_command):
    os.system(run_command)


if __name__ == '__main__':
	parser = arg.ArgumentParser(description='inputs discription')  
	parser.add_argument('-f', '--file', dest='txtfile', type=str, default=['local_crab_report_mu_UL2017_2J1T1_MC.txt'], nargs=1, help="condor directory")
	
	args = parser.parse_args()
	
	if args.txtfile == None:
	    print("USAGE: %s [-h] [-f txt file]"%(sys.argv [0]))
	    exit(1) 
	
	txtfile=args.txtfile[0]

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
	rerun_list = []
	rerun_list.append('python3  crab_script_cutflow_local.py -d Tchannel -t 2J1T1_el_mc_UL2017 -o /nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/SEVENTEEN/2J1T1/el/Tchannel/ -p /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/Tchannel/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_10_Jul23_MCUL2017_Tchannel/230710_201319/0000/tree_37.root -n 128 &>/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/SEVENTEEN/2J1T1/el/Tchannel/log/log_128.txt')	
	print(rerun_list[0])
	#print(rerun_list[1])	
	print("runing "+str(len(rerun_list))+ " jobs .... .... ")
	pool = mp.Pool(15)
	pool.map(run_cmd, rerun_list)
	del rerun_list
	pool.close()
	pool.join()
	#with mp.Pool(2) as p:
	#	p.map(run_cmd, rerun_list,chunksize=1)