import fileinput, string, sys, os, time, subprocess
import argparse as arg
import multiprocessing as mp
import glob
import ROOT

def run_cmd(run_command):
    os.system(run_command)


if __name__ == '__main__':
	parser = arg.ArgumentParser(description='inputs discription')  
	parser.add_argument('-d', '--dir', dest='LocalDir', type=str, default=['/nfs/home/common/RUN2_UL/Minitree_crab/SEVENTEEN/2J1T1/'], nargs=1, help="condor directory")
	parser.add_argument('-s', '--sample', dest='samples', type=str, default=['Mc_Nomi'], nargs=1, help="sample [ Mc_Nomi , Mc_Alt , Mc_sys , Data ]")
	parser.add_argument('-l', '--lepton', dest='leptons', type=str, default=['mu'], nargs=1, help="sample [ mu , el ]")
	parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")

	args = parser.parse_args()

	if args.LocalDir == None:
		print("USAGE: %s [-h] [-d <condor directory>]"%(sys.argv [0]))
		exit(1) 
	if args.leptons[0] not in ['mu','el']:
		print('Error: Incorrect choice of lepton type, use -h for help')
		exit(1)
	if args.samples[0] not in ['Mc_Nomi', 'Mc_Alt', 'Mc_sys', 'Data']:
		print('Error: Incorrect choice of sample type, use -h for help')
		exit()


	LocalDir=args.LocalDir[0]
	if not (os.path.isdir(LocalDir)):
		print("Dir", " '",LocalDir,"' "," does not exist")
		exit()

	year_folder = {'SIXTEEN_preVFP':'UL2016preVFP', 'SIXTEEN_postVFP':'UL2016postVFP', 'SEVENTEEN':'UL2017', 'EIGHTEEN':'UL2018'}
	#print("year : ",year_folder[LocalDir.split('/')[-3]])
	year = year_folder[LocalDir.split('/')[6]] 

	lep = args.leptons[0]
	sample = args.samples[0]
	print(year)

	MC_Data = "data" if args.ISDATA else "mc"
	print(args.ISDATA," ",MC_Data)

	if(MC_Data=="mc"):
		Channels_commom = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','DYJetsToLL']
		if(year=='UL2017'): Channels_commom = Channels_commom + ['WJetsToLNu_0J_lagecy','WJetsToLNu_2J_lagecy','WJetsToLNu_2J_ext_lagecy']
		if(lep=="mu"): Channel_QCD = ['QCD_Pt-15To20_MuEnriched', 'QCD_Pt-20To30_MuEnriched', 'QCD_Pt-30To50_MuEnriched', 'QCD_Pt-50To80_MuEnriched', 'QCD_Pt-80To120_MuEnriched', 'QCD_Pt-120To170_MuEnriched', 'QCD_Pt-170To300_MuEnriched', 'QCD_Pt-300To470_MuEnriched', 'QCD_Pt-470To600_MuEnriched', 'QCD_Pt-600To800_MuEnriched', 'QCD_Pt-800To1000_MuEnriched', 'QCD_Pt-1000_MuEnriched']

		elif(lep=="el"): Channel_QCD = ['QCD_Pt-15to20_EMEnriched', 'QCD_Pt-20to30_EMEnriched', 'QCD_Pt-30to50_EMEnriched', 'QCD_Pt-50to80_EMEnriched', 'QCD_Pt-80to120_EMEnriched', 'QCD_Pt-120to170_EMEnriched' , 'QCD_Pt-170to300_EMEnriched', 'QCD_Pt-300toInf_EMEnriched' ]

		Channel_sys = ['Tchannel_QCDinspired', 'Tchannel_Gluonmove', 'Tchannel_TuneCP5up', 'Tchannel_TuneCP5down', 'Tchannel_erdON', 'Tbarchannel_QCDinspired', 'Tbarchannel_Gluonmove', 'Tbarchannel_TuneCP5up', 'Tbarchannel_TuneCP5down', 'Tbarchannel_erdON', 'ttbar_FullyLeptonic_QCDinspired', 'ttbar_FullyLeptonic_Gluonmove', 'ttbar_FullyLeptonic_erdON', 'ttbar_FullyLeptonic_TuneCP5up', 'ttbar_FullyLeptonic_TuneCP5down', 'ttbar_SemiLeptonic_QCDinspired', 'ttbar_SemiLeptonic_Gluonmove', 'ttbar_SemiLeptonic_erdON', 'ttbar_SemiLeptonic_TuneCP5up', 'ttbar_SemiLeptonic_TuneCP5down']

		Channels = Channels_commom + Channel_QCD #+
		#Channels  = Channel_sys

	elif(MC_Data=="data"):
		if(year=='UL2016preVFP'): Channels = [ 'Run2016B-ver1_'+lep, 'Run2016B-ver2_'+lep, 'Run2016C-HIPM_'+lep, 'Run2016D-HIPM_'+lep, 'Run2016E-HIPM_'+lep, 'Run2016F-HIPM_'+lep]
		if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+lep, 'Run2016G_'+lep, 'Run2016H_'+lep]
		if(year=='UL2017'): Channels = [ 'Run2017B_'+lep, 'Run2017C_'+lep, 'Run2017D_'+lep, 'Run2017E_'+lep, 'Run2017F_'+lep]
		if(year=='UL2018'): Channels = [ 'Run2018A_'+lep,'Run2018B_'+lep, 'Run2018C_'+lep, 'Run2018D_'+lep]


	print()
	print("-----------------------------------------    chacking     --------------------------------")
	print()

	rerun_list = []
	root_file = []
	cwd = os.getcwd()

	#Channels = ['ttbar_SemiLeptonic','ttbar_FullyLeptonic']
	Error = "Skim"
	if(MC_Data=="mc"): No_of_file_per_job = 1
	elif(MC_Data=="data"): No_of_file_per_job = 1 # though the number of file per job are 5 but still when number of file are not desial of 5 then file less 5 are submitted 
	for channel in Channels:
		print("----------------------\n"+channel+"\n-----------------------\n")
		outputDir = LocalDir + '/' + lep + '/' + channel + '/log'
		log_files = glob.glob(outputDir + '/log_*.txt')
		print(outputDir + '/log_*.txt') 
		print("Total log files : ",len(log_files))
		#print("All log files list : ",log_files)
		for log_file in log_files:
			cmd_grep = 'grep "'+Error+'" '+log_file
			#print(cmd_grep)
			p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			p_status = p.wait()
			skip_tranfer_check = False
			output = str(output)
			if(output.count(Error)<No_of_file_per_job):
				#print(output.count(Error))
				print(log_file)
				cmd_grep2 = 'grep "python3 crab_script_Minitree_local.py" '+log_file
				p2 = subprocess.Popen(cmd_grep2, stdout=subprocess.PIPE, shell=True)
				(output2, err2) = p2.communicate()
				rerun_list.append(str(output2)[3:-3]) # remove /n and b' using python3
				root_file.append(str(output2).rsplit(" ")[-5])
				#rerun_list.append(str(output2)[1:-1]) # remove /n and b' using python2
	print(rerun_list)
	print("runing "+str(len(rerun_list))+ " jobs .... .... ")
	#pool = mp.Pool(processes=4) 
	#pool.map(run_cmd, rerun_list)

