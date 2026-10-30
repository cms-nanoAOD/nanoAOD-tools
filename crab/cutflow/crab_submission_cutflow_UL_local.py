

import os
import glob
import multiprocessing as mp
import fileinput, string, sys, time, datetime,  subprocess
from contextlib import closing

def run_cmd(run_command):
    os.system(run_command)

def replacemachine(fileName, sourceText, replaceText):
    print( "editing ",fileName,)
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
                line = replaceText
        sys.stdout.write(line)
    print("All went well, the modifications are done")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='mu', help="lepton flavor [ el , mu ]")
    parser.add_argument('-r', '--region', dest='region', type=str, default='2J1T1', help="region of caluation [ 2J1T1 , 2J1T0 ]")
    parser.add_argument('-y', '--year', dest='year', type=str, default='UL2017', help=" UL2017 UL2016preVFP UL2016postVFP UL2018 ")
    parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")
    parser.add_argument('-resub',"--ISresub", action="store_true", help="enbale this feature when resubmitting the jobs")
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default='/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/', help="Set Dir for the output files")

    args = parser.parse_args()

    Lep = args.lepton
    region = args.region
    year = args.year
    MC_Data = "data" if args.ISDATA else "mc"
    year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}
    tag =   region+'_'+Lep + '_' + MC_Data + '_' + year
    Out_dir = args.out_dir
    print(args.ISDATA," ",MC_Data)
    if(MC_Data=="mc"):
	    Channels_commom = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','DYJetsToLL'] 
	    #if(year=='UL2017'): Channels_commom = Channels_commom + ['WJetsToLNu_0J_lagecy','WJetsToLNu_2J_lagecy','WJetsToLNu_2J_ext_lagecy']
	    if(year=='UL2017'): Channels_commom = Channels_commom + ['WJetsToLNu_0J_v2']
	    if(Lep=="mu"): Channel_QCD = ['QCD_Pt-15To20_MuEnriched', 'QCD_Pt-20To30_MuEnriched', 'QCD_Pt-30To50_MuEnriched', 'QCD_Pt-50To80_MuEnriched', 'QCD_Pt-80To120_MuEnriched', 'QCD_Pt-120To170_MuEnriched', 'QCD_Pt-170To300_MuEnriched', 'QCD_Pt-300To470_MuEnriched', 'QCD_Pt-470To600_MuEnriched', 'QCD_Pt-600To800_MuEnriched', 'QCD_Pt-800To1000_MuEnriched', 'QCD_Pt-1000_MuEnriched']

	    elif(Lep=="el"): Channel_QCD = ['QCD_Pt-15to20_EMEnriched', 'QCD_Pt-20to30_EMEnriched', 'QCD_Pt-30to50_EMEnriched', 'QCD_Pt-50to80_EMEnriched', 'QCD_Pt-80to120_EMEnriched', 'QCD_Pt-120to170_EMEnriched' , 'QCD_Pt-170to300_EMEnriched', 'QCD_Pt-300toInf_EMEnriched' ]

	    Channel_sys = ['Tchannel_QCDinspired', 'Tchannel_Gluonmove', 'Tchannel_TuneCP5up', 'Tchannel_TuneCP5down', 'Tchannel_erdON', 'Tchannel_PSweights', 'Tbachannel_QCDinspired', 'Tbachannel_Gluonmove', 'Tbachannel_TuneCP5up', 'Tbachannel_TuneCP5down', 'Tbachannel_erdON', 'Tbarchannel_PSweights', 'ttbar_FullyLeptonic_QCDinspired', 'ttbar_FullyLeptonic_Gluonmove', 'ttbar_FullyLeptonic_erdON', 'ttbar_FullyLeptonic_TuneCPup', 'ttbar_FullyLeptonic_TuneCPdown', 'ttbar_FullyLeptonic_PSweights', 'ttbar_SemiLeptonic_QCDinspired', 'ttbar_SemiLeptonic_Gluonmove', 'ttbar_SemiLeptonic_erdON', 'ttbar_SemiLeptonic_TuneCP5up', 'ttbar_SemiLeptonic_TuneCP5down', 'ttbar_SemiLeptonic_PSweights']

	    Channels = Channels_commom + Channel_QCD #+Channel_sys 

    elif(MC_Data=="data"):
        if(year=='UL2016preVFP'): Channels = [ 'Run2016B_ver1_'+Lep, 'Run2016B_ver2_'+Lep, 'Run2016C_HIPM_'+Lep, 'Run2016D_HIPM_'+Lep, 'Run2016E_HIPM_'+Lep, 'Run2016F_HIPM_'+Lep]
        if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+Lep, 'Run2016G_'+Lep, 'Run2016H_'+Lep]
        if(year=='UL2017'): Channels = [ 'Run2017B_'+Lep, 'Run2017C_'+Lep, 'Run2017D_'+Lep, 'Run2017E_'+Lep, 'Run2017F_'+Lep]
        if(year=='UL2018'): Channels = [ 'Run2018A_'+Lep,'Run2018B_'+Lep, 'Run2018C_'+Lep, 'Run2018D_'+Lep] 

    #Channels = ['Tchannel']#,'tw_antitop','ttbar_FullyLeptonic','ttbar_SemiLeptonic']#,'WWTo2L2Nu']# + Channel_QCD #[]#, 'ttbar_SemiLeptonic']

    print(Channels)

    run_commands = []
    Hadd_N_createoutfile_cmd = {}
    
    for Channel in Channels:
        print(Channel)
       	local_script_output_dir = Out_dir + year_folder[year]+'/'+region+'/'+Lep+'/'+Channel + '/' 
       	os.makedirs(local_script_output_dir+'log/', exist_ok = True)
       	if(MC_Data=="mc"): 
            in_files = glob.glob('/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/MC/' + Channel + '/**/**/**/**/*.root')
            print(' files beeing read from /nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'_new_Mintu/MC/' + Channel + '/**/**/**/**/*.root')
        elif(MC_Data=="data"):  
            in_files = glob.glob('/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'_new_Mintu/Data_' + Lep + '/' + Channel + '/**/**/**/**/*.root')
            print(' files beeing read from /nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'_new_Mintu/Data_' + Lep + '/' + Channel + '/**/**/**/**/*.root')
       	print("total file selected : ",len(in_files))
       	Hadded_out_file_name = 'Cutflow_'+ Channel+'_'+region+'_'+Lep+ '.root '
       	print(in_files)
       	inputFiles = [i for i in in_files if i != '']
       	Hadd_N_createoutfile_cmd[Channel] = 'hadd -f ' + Out_dir +year_folder[year]+'/'+region+'/'+Hadded_out_file_name
        i=0
       	if(MC_Data=="mc"): commom_run_cmd = ' cmsenv; python3 crab_script_cutflow_local.py  -d ' + Channel + ' -t ' + tag + ' -o ' + local_script_output_dir
        elif(MC_Data=="data"): commom_run_cmd = ' cmsenv; python3 crab_script_cutflow_local.py  -data -d ' + Channel + ' -t ' + tag + ' -o ' + local_script_output_dir
       	total_file_in_set = 1
        fileSetcounter = 0
        infils = ''
        Error= "Done"
       	for count,fil in enumerate(inputFiles):
            fileSetcounter+=1
            num = fil.split('/')[-1].split('.')[0].split('_')[-1]
            infils = infils+fil+" "
            if(fileSetcounter%total_file_in_set==0 or count+1==len(inputFiles)):
                #infils = infils+"]"
                Hadd_N_createoutfile_cmd[Channel] += local_script_output_dir + 'Cutflow_hist_' + str(count+1) + '.root '
                #print(Hadd_N_createoutfile_cmd[Channel])
                if(args.ISresub):
                    cmd_grep = 'grep "'+Error+'" '+local_script_output_dir + 'log/log_' +str(count+1) + '.txt'
                    #print(cmd_grep)
                    p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
                    (output, err) = p.communicate()
                    p_status = p.wait()
                    output = str(output)
                    #print(output.count(Error))
                    if(output.count(Error)<1):
                        #print(local_script_output_dir + 'log/log_' +str(count+1) + '.txt')
                        run_commands.append(commom_run_cmd + ' -p ' + infils + ' -n ' + str(count+1) +' &> ' + local_script_output_dir + 'log/log_' +str(count+1) + '.txt' )
                else:
                    run_commands.append(commom_run_cmd + ' -p ' + infils + ' -n ' + str(count+1) +' &> ' + local_script_output_dir + 'log/log_' +str(count+1) + '.txt' )
                fileSetcounter = 0
                infils = ''
            i=i+1
            #if(i==5): break
            #if(i==total_file_in_set): break #switch of test perpose take only two file and the scripts
    print(run_commands)
    print("running ...", len(run_commands),"jobs")
    #for command in run_commands:
    #    run_cmd(command)
    #del run_commands
    #print(Hadd_N_createoutfile_cmd[Channel])
    
    """pool = mp.Pool(processes=15)
    pool.map(run_cmd, run_commands)
    del run_commands
    pool.close()"""

    for Channel in Channels:
        Hadded_out_file_name = 'Cutflow_'+ Channel+'_'+region+'_'+Lep+ '.root '
        print("check if exists "+Out_dir + year_folder[year]+'/'+region+'/'+ Hadded_out_file_name)
        print(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name))
        if(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)):
                keyinput = input(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name+ '  is exit should delete and recreate enter "yes" other wise press eneter key i will skip the hadd command' )
                if(keyinput=='yes'):os.system('rm ' + Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)
                else: exit(0)
        #print("runing....", Hadd_N_createoutfile_cmd[Channel])
        #os.system(Hadd_N_createoutfile_cmd[Channel])
