import fileinput, string, sys, os, time, subprocess
import argparse as arg
import multiprocessing as mp
import glob
import re

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

	sample = args.samples[0]
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

		if(sample =="Mc_Nomi"): Channels = Channels_commom + Channel_QCD #+
		elif(sample =="Mc_Sys"): Channels  = Channel_sys

	elif(MC_Data=="data"):
		if(year=='UL2016preVFP'): Channels = [ 'Run2016B-ver1_'+lep, 'Run2016B-ver2_'+lep, 'Run2016C-HIPM_'+lep, 'Run2016D-HIPM_'+lep, 'Run2016E-HIPM_'+lep, 'Run2016F-HIPM_'+lep]
		if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+lep, 'Run2016G_'+lep, 'Run2016H_'+lep]
		if(year=='UL2017'): Channels = [ 'Run2017B_'+lep, 'Run2017C_'+lep, 'Run2017D_'+lep, 'Run2017E_'+lep, 'Run2017F_'+lep]
		if(year=='UL2018'): Channels = [ 'Run2018A_'+lep,'Run2018B_'+lep, 'Run2018C_'+lep, 'Run2018D_'+lep]


	print()
	print("-----------------------------------------    chacking     --------------------------------")
	print()

	rerun_list = []
	missing_output_files = []
	cwd = os.getcwd()

	#Channels = ['ttbar_SemiLeptonic','ttbar_FullyLeptonic']

	# --- V2 detection logic -------------------------------------------------
	# crab_script_Minitree_local.py no longer writes a fixed "_Skim" postfix --
	# it always calls check_and_rerun() first (splitting=2, threshold=500000)
	# and then runs PostProcessor once per resulting chunk with an explicit
	# postfix = "_<start>_<end>" (e.g. "_0_123456"), printed as a
	# "postfix :  <value>" line per chunk. So:
	#   - "No splitting needed."          -> 1 chunk expected  -> 1 postfix line
	#   - "Splitting into N chunks: ..."  -> N chunks expected -> N postfix lines
	# A job that crashed/never finished won't have printed either of those two
	# check_and_rerun() lines, or will be missing postfix lines relative to
	# what it announced, or the tree_<num><postfix>.root file it announced
	# won't actually exist on disk (crashed mid-PostProcessor.run()).
	SPLIT_RE = re.compile(r'Splitting into (\d+) chunks')
	NO_SPLIT_RE = re.compile(r'No splitting needed\.')
	POSTFIX_RE = re.compile(r'postfix\s*:\s*(_\d+_\d+)')
	# Captures every filename after "-p", not just the first: data jobs batch
	# 5 input files behind one "-p" (MC batches 1), and each of those files
	# gets the job's postfix(es) applied to it independently, so each needs
	# its own on-disk check -- checking only the first silently misses a job
	# that crashed partway through writing the rest of its batch.
	INPUT_FILE_RE = re.compile(r'-p\s+((?:\S+\.root\s+)+)')
	RERUN_CMD_RE = re.compile(r'^\s*python3 crab_script_Minitree_local\.py.*$', re.MULTILINE)

	for channel in Channels:
		print("----------------------\n"+channel+"\n-----------------------\n")
		channel_dir = LocalDir + '/' + lep + '/' + channel + '/'
		outputDir = channel_dir + 'log'
		log_files = glob.glob(outputDir + '/log_*.txt')
		print(outputDir + '/log_*.txt')
		print("Total log files : ",len(log_files))
		#print("All log files list : ",log_files)
		for log_file in log_files:
			with open(log_file) as f:
				content = f.read()

			failed_reason = None

			split_match = SPLIT_RE.search(content)
			if split_match:
				expected_chunks = int(split_match.group(1))
			elif NO_SPLIT_RE.search(content):
				expected_chunks = 1
			else:
				expected_chunks = None
				failed_reason = "job never reached check_and_rerun()'s split decision (crashed early / still running)"

			postfixes = POSTFIX_RE.findall(content)

			if failed_reason is None and len(postfixes) < expected_chunks:
				failed_reason = f"expected {expected_chunks} chunk(s) but only {len(postfixes)} postfix line(s) printed"

			if failed_reason is None:
				input_match = INPUT_FILE_RE.search(content)
				if not input_match:
					failed_reason = "could not find the '-p <input_file>' line to verify outputs"
				else:
					input_paths = input_match.group(1).split()
					for input_path in input_paths:
						num = input_path.split('/')[-1].split('.')[0].split('_')[-1]
						for pf in postfixes:
							out_file = channel_dir + 'tree_' + num + pf + '.root'
							if not os.path.isfile(out_file):
								missing_output_files.append(out_file)
								failed_reason = f"output file missing on disk: {out_file}"

			if failed_reason is not None:
				print(log_file, " -- FAILED:", failed_reason)
				rerun_match = RERUN_CMD_RE.search(content)
				if rerun_match:
					rerun_list.append(rerun_match.group(0).strip())
				else:
					print("   WARNING: could not recover the rerun command from this log")

	print(rerun_list)
	print("runing "+str(len(rerun_list))+ " jobs .... .... ")
	if missing_output_files:
		print(f"\n{len(missing_output_files)} expected output file(s) missing on disk:")
		for f in missing_output_files:
			print("  ", f)
	# pool = mp.Pool(processes=3)
	# pool.map(run_cmd, rerun_list)
