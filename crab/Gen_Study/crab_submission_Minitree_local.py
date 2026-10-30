

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

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-y', '--year', dest='year', type=str, default='UL2017', help=" UL2016 UL2016preVFP")
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default='/nfs/home/common/RUN2_UL/Minitree_trial/', help="Set Dir for the output files")

    args = parser.parse_args()

    year = args.year
    Out_dir = args.out_dir
    Channels = ["Tbarchannel_wtop1p3",]#"Tbarchannel_Nomi","Tchannel_wtop1p3","Tchannel_Nomi","ttbar_SemiLeptonic_wtop1p3","ttbar_SemiLeptonic_Nomi","ttbar_FullyLeptonic_widthx1p3","ttbar_FullyLeptonic_Nomi"]
    print(Channels)

    run_commands = []
    Hadded_out_file_name = {}
    Hadd_N_createoutfile_cmd = {}
    
    for Channel in Channels:
        print(Channel)
       	local_script_output_dir = Out_dir +'/'+Channel + '/' 
       	os.makedirs(local_script_output_dir+'log/', exist_ok = True)
       	print(' files beeing read from /nfs/home/common/RUN2_UL/Tree_crab/SIXTEEN_Gen/Mc_NANOGEN_v9/'+ Channel + '/**/**/**/**/*.root')
       	in_files = glob.glob('/nfs/home/common/RUN2_UL/Tree_crab/SIXTEEN_Gen/Mc_NANOGEN_v9/' + Channel + '/**/**/**/**/*.root')
       	print("total file selected : ",len(in_files))
       	Hadded_out_file_name[Channel] = 'Minitree_'+ Channel+'_Mc.root'
       	#print(in_files)
       	inputFiles = [i for i in in_files if i != '']
       	Hadd_N_createoutfile_cmd[Channel] = 'python3 ../../scripts/haddnano.py ' + Out_dir +Hadded_out_file_name[Channel]
        i=0
        commom_run_cmd = 'pwd; cmsenv; python3 crab_script_NanoGen_minitree_local.py  -o ' + local_script_output_dir
        total_file_in_set = 1
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
    #print(Hadd_N_createoutfile_cmd[Channel])

    pool = mp.Pool(processes=15)
    pool.map(run_cmd, run_commands)
    del run_commands
    pool.close()


    for Channel in Channels:
        print("check if exists "+Out_dir + Hadded_out_file_name[Channel])
        print(os.path.isfile(Out_dir +Hadded_out_file_name[Channel]))
        if(os.path.isfile(Out_dir +Hadded_out_file_name[Channel])):
                keyinput = input(Out_dir +Hadded_out_file_name+ '  is exit should delete and recreate enter "yes" other wise press eneter key i will skip the hadd command' )
                if(keyinput=='yes'):os.system('rm ' + Out_dir +Hadded_out_file_name)
                else: exit(0)
        print("runing....", Hadd_N_createoutfile_cmd[Channel],"\n")
        os.system(Hadd_N_createoutfile_cmd[Channel])
