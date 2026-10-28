import os
import glob
import multiprocessing as mp
import fileinput, string, sys, time, datetime

def run_cmd(run_command):
    os.system(run_command)

def replacemachine(fileName, sourceText, replaceText):
    print( "editing ",fileName,)
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
                line = replaceText
        sys.stdout.write(line)
    print("All went well, the modifications are done")

def fix_hadd_cmd_with_split_postfix_old(hadd_cmd, base_output_dir, Channel):
    """
    crab_script_Minitree_local.py actually names its outputs
    tree_<num><postfix>.root, where <postfix> (e.g. "_0_123456") comes from
    check_and_rerun()'s event-count splitting -- not the "tree_<num>_Skim.root"
    placeholder hadd_cmd was built with. Each job's log (log/log_*.txt under
    the channel's output dir) reprints its own "-p <input_file>" invocation
    and a "postfix :  <value>" line per output chunk (one or two, depending
    on whether the input got split), so read those back out and substitute
    the real filename(s) in place of each placeholder.

    local_script_output_dir is rebuilt here from base_output_dir + Channel
    rather than passed in directly, since callers loop over multiple
    channels and a stale directory from a previous iteration would silently
    scan the wrong channel's logs.

    A log with no "postfix :" line at all means that job crashed or never
    finished -- deliberately left as the original _Skim.root placeholder
    (which will never exist) instead of being dropped, so hadd fails loudly
    on it rather than silently hadding fewer files.
    """
    import re

    local_script_output_dir = base_output_dir + Channel + '/'
    log_dir = local_script_output_dir + 'log/'
    log_files = glob.glob(log_dir + 'log_*.txt')

    missing_logs = []
    for log_file in log_files:
        with open(log_file) as f:
            content = f.read()

        p_match = re.search(r'-p\s+(\S+\.root)', content)
        if not p_match:
            missing_logs.append(log_file)
            continue
        input_path = p_match.group(1)
        num = input_path.split('/')[-1].split('.')[0].split('_')[-1]

        postfixes = re.findall(r'postfix\s*:\s*(_\d+_\d+)', content)
        if not postfixes:
            missing_logs.append(log_file)
            continue

        placeholder = local_script_output_dir + 'tree_' + num + '_Skim.root '
        real_files = ''.join(local_script_output_dir + 'tree_' + num + pf + '.root ' for pf in postfixes)
        hadd_cmd = hadd_cmd.replace(placeholder, real_files)

    if missing_logs:
        print(f"WARNING: {len(missing_logs)} job(s) never printed a postfix (crashed or still running) -- their tree_<num>_Skim.root placeholder was left in place so hadd will fail on them instead of silently skipping:")
        for lf in missing_logs:
            print("  ", lf)

    return hadd_cmd

def fix_hadd_cmd_with_split_postfix(hadd_cmd, base_output_dir, Channel):
    """
    Same purpose as fix_hadd_cmd_with_split_postfix_old, but handles jobs that
    batch multiple input files behind a single "-p" (data runs 5 files per
    job; MC runs 1). The old version's regex only captured the first filename
    after "-p", so for a batched job only that one file's placeholder got
    patched to its real tree_<num><postfix>.root name(s) -- the other files
    in the same job kept their never-created tree_<num>_Skim.root placeholder,
    which made hadd abort as soon as it reached one of them. This version
    captures every filename following "-p" and applies the job's postfix(es)
    (shared across all files in that job, since the splitting cut is applied
    uniformly to the whole job) to each one individually.

    A log with no "-p" files or no "postfix :" line at all means that job
    crashed or never finished -- deliberately left as the original
    _Skim.root placeholder(s) (which will never exist) instead of being
    dropped, so hadd fails loudly on it rather than silently hadding fewer
    files.
    """
    import re

    local_script_output_dir = base_output_dir + Channel + '/'
    log_dir = local_script_output_dir + 'log/'
    log_files = glob.glob(log_dir + 'log_*.txt')

    missing_logs = []
    for log_file in log_files:
        with open(log_file) as f:
            content = f.read()

        p_match = re.search(r'-p\s+((?:\S+\.root\s+)+)', content)
        if not p_match:
            missing_logs.append(log_file)
            continue
        input_paths = p_match.group(1).split()

        postfixes = re.findall(r'postfix\s*:\s*(_\d+_\d+)', content)
        if not postfixes:
            missing_logs.append(log_file)
            continue

        for input_path in input_paths:
            num = input_path.split('/')[-1].split('.')[0].split('_')[-1]
            placeholder = local_script_output_dir + 'tree_' + num + '_Skim.root '
            real_files = ''.join(local_script_output_dir + 'tree_' + num + pf + '.root ' for pf in postfixes)
            hadd_cmd = hadd_cmd.replace(placeholder, real_files)

    if missing_logs:
        print(f"WARNING: {len(missing_logs)} job(s) never printed a postfix (crashed or still running) -- their tree_<num>_Skim.root placeholder(s) were left in place so hadd will fail on them instead of silently skipping:")
        for lf in missing_logs:
            print("  ", lf)

    return hadd_cmd

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='mu', help="lepton flavor [ el , mu ]")
    parser.add_argument('-r', '--region', dest='region', type=str, default='2J1T1', help="region of caluation [ 2J1T1 , 2J1T0 ]")
    parser.add_argument('-y', '--year', dest='year', type=str, default='UL2017', help=" UL2017 UL2016preVFP UL2016postVFP UL2018 ")
    parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default='/nfs/home/common/RUN2_UL/Minitree_trial/', help="Set Dir for the output files")

    args = parser.parse_args()

    Lep = args.lepton
    region = args.region
    year = args.year
    MC_Data = "data" if args.ISDATA else "mc"
    year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}
    tag =   region+'_'+Lep + '_' + MC_Data + '_' + year
    Out_dir = args.out_dir
    print(f'{Out_dir = }')
    print(args.ISDATA," ",MC_Data)
    if(MC_Data=="mc"):
        #'ttbar_SemiLeptonic','ttbar_FullyLeptonic'
        Channels_commom = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','DYJetsToLL','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
        #'WWTolnulnu',
        #if(year=='UL2017'): Channels_commom = Channels_commom + ['WJetsToLNu_0J_lagecy','WJetsToLNu_2J_lagecy','WJetsToLNu_2J_ext_lagecy']
        if(year=='UL2017'): Channels_commom = Channels_commom + ['WJetsToLNu_0J_v2']
        if(Lep=="mu"): Channel_QCD = ['QCD_Pt-15To20_MuEnriched', 'QCD_Pt-20To30_MuEnriched', 'QCD_Pt-30To50_MuEnriched', 'QCD_Pt-50To80_MuEnriched', 'QCD_Pt-80To120_MuEnriched', 'QCD_Pt-120To170_MuEnriched', 'QCD_Pt-170To300_MuEnriched', 'QCD_Pt-300To470_MuEnriched', 'QCD_Pt-470To600_MuEnriched', 'QCD_Pt-600To800_MuEnriched', 'QCD_Pt-800To1000_MuEnriched', 'QCD_Pt-1000_MuEnriched']
        elif(Lep=="el"): Channel_QCD = ['QCD_Pt-15to20_EMEnriched', 'QCD_Pt-20to30_EMEnriched', 'QCD_Pt-30to50_EMEnriched', 'QCD_Pt-50to80_EMEnriched', 'QCD_Pt-80to120_EMEnriched', 'QCD_Pt-120to170_EMEnriched' , 'QCD_Pt-170to300_EMEnriched', 'QCD_Pt-300toInf_EMEnriched' ]
        Channel_sys = [
                       'Tchannel_QCDinspired', 'Tchannel_Gluonmove', 'Tchannel_TuneCP5up', 'Tchannel_TuneCP5down', 'Tchannel_erdON',  
                       'Tbarchannel_QCDinspired', 'Tbarchannel_Gluonmove', 'Tbarchannel_TuneCP5up', 'Tbarchannel_TuneCP5down', 'Tbarchannel_erdON',  
                       'ttbar_FullyLeptonic_QCDinspired', 'ttbar_FullyLeptonic_Gluonmove', 'ttbar_FullyLeptonic_erdON', 'ttbar_FullyLeptonic_TuneCP5up', 'ttbar_FullyLeptonic_TuneCP5down',
                       #'ttbar_SemiLeptonic_QCDinspired', 'ttbar_SemiLeptonic_Gluonmove', 'ttbar_SemiLeptonic_erdON', 'ttbar_SemiLeptonic_TuneCP5up', 'ttbar_SemiLeptonic_TuneCP5down'
        ]
        Channels = Channels_commom + Channel_QCD #+ Channel_sys
        # Channels = ['ttbar_SemiLeptonic','ttbar_FullyLeptonic']
        # Channels = Channel_sys 
        #Channels = ['ttbar_SemiLeptonic_QCDinspired', 'ttbar_SemiLeptonic_Gluonmove', 'ttbar_SemiLeptonic_erdON', 'ttbar_SemiLeptonic_TuneCP5up', 'ttbar_SemiLeptonic_TuneCP5down']

    elif(MC_Data=="data"):
        if(year=='UL2016preVFP'): Channels = [ 'Run2016B_ver1_'+Lep, 'Run2016B_ver2_'+Lep, 'Run2016C_HIPM_'+Lep, 'Run2016D_HIPM_'+Lep, 'Run2016E_HIPM_'+Lep, 'Run2016F_HIPM_'+Lep]
        if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+Lep, 'Run2016G_'+Lep, 'Run2016H_'+Lep]
        if(year=='UL2017'): Channels = [ 'Run2017B_'+Lep, 'Run2017C_'+Lep, 'Run2017D_'+Lep, 'Run2017E_'+Lep, 'Run2017F_'+Lep]
        if(year=='UL2018'): Channels = [ 'Run2018A_'+Lep,'Run2018B_'+Lep, 'Run2018C_'+Lep, 'Run2018D_'+Lep] 


    #
    #Channels = ['Tchannel']
    print(Channels)

    run_commands = []
    Hadd_N_createoutfile_cmd = {}
    base_output_dir = Out_dir + year_folder[year]+'/'+region+'/'+Lep+'/'

    for Channel in Channels:
        print(Channel)
       	local_script_output_dir = base_output_dir + Channel + '/'
       	print(f'{local_script_output_dir = }')
        os.makedirs(local_script_output_dir+'log/', exist_ok = True)

        if(MC_Data=="mc"):
            in_files_path = '/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/MC/' + Channel + '/**/**/**/**/*.root'
            #in_files_path = '/eos/home-m/mikumar/RUN2_UL/' + Channel + '/**/**/**/**/*.root'
        elif(MC_Data=="data"):
            in_files_path = '/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/Data_' + Lep + '/' + Channel + '/**/**/**/**/*.root'

       	print(' files beeing read from '+in_files_path)
        in_files = glob.glob(in_files_path)
       	print("total file selected : ",len(in_files))
       	Hadded_out_file_name = 'Minitree_'+ Channel+'_'+region+'_'+Lep+ '.root '
       	print(in_files)
       	inputFiles = [i for i in in_files if i != '']
       	Hadd_N_createoutfile_cmd[Channel] = 'python3 ../../scripts/haddnano.py ' + Out_dir +year_folder[year]+'/'+region+'/'+Hadded_out_file_name
        i=0
       	if(MC_Data=="mc"): 
            commom_run_cmd = 'pwd; cmsenv; python3 -u crab_script_Minitree_local.py  -d ' + Channel + ' -t ' + tag + ' -o ' + local_script_output_dir
            total_file_in_set = 1
        elif(MC_Data=="data"): 
            commom_run_cmd = 'pwd; cmsenv; python3 -u crab_script_Minitree_local.py  -data -d ' + Channel + ' -t ' + tag + ' -o ' + local_script_output_dir
       	    total_file_in_set = 5
        fileSetcounter = 0
        infils = ''
       	for count,fil in enumerate(inputFiles):
            fileSetcounter+=1
            num = fil.split('/')[-1].split('.')[0].split('_')[-1]
       	    Hadd_N_createoutfile_cmd[Channel] += local_script_output_dir + 'tree_' + num + '_Skim.root '
       	    #print(Hadd_N_createoutfile_cmd[Channel])
            infils = infils+fil+" "
            if(fileSetcounter%total_file_in_set==0 or count+1==len(inputFiles)):
                #infils = infils+"]"
                run_commands.append(commom_run_cmd + ' -p ' + infils + ' -n ' + str(count+1) +' &> ' + local_script_output_dir + 'log/log_' +str(count+1) + '.txt' )
                fileSetcounter = 0
                infils = ''
            i=i+1
            #if(i==total_file_in_set): break #switch of test perpose take only two file and the scripts
    
    print(run_commands,"\n")
    # print(Hadd_N_createoutfile_cmd[Channel])
    '''
    pool = mp.Pool(processes=15)
    pool.map(run_cmd, run_commands)
    del run_commands
    pool.close()

    for Channel in Channels:
        Hadd_N_createoutfile_cmd[Channel] = fix_hadd_cmd_with_split_postfix(Hadd_N_createoutfile_cmd[Channel], base_output_dir, Channel)
        #print("with real split postfixes:\n", Hadd_N_createoutfile_cmd[Channel])
        Hadded_out_file_name = 'Minitree_'+ Channel+'_'+region+'_'+Lep+ '.root '
        print("check if exists "+Out_dir + year_folder[year]+'/'+region+'/'+ Hadded_out_file_name)
        print(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name))
        if(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)):
               keyinput = input(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name+ '  is exit should delete and recreate enter "yes" other wise press eneter key i will skip the hadd command' )
               if(keyinput=='yes'):os.system('rm ' + Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)
               else: exit(0)
        print("runing....", Hadd_N_createoutfile_cmd[Channel],"\n")
        os.system(Hadd_N_createoutfile_cmd[Channel])'''
