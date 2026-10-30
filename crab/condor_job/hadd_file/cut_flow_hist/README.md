# Genral Instraction
* ./submitCondor require inputs to run 
* i.e ./submitCondor.sh <input_file> <output_dir> 
* this scripts create tempMerge_N.root file as intermidiate file and finaly gives out putroot file acc to last charctor in the path in the input file
 
##Run hadd Minitree
* All the paths and to be in put file which has to have the same name convestion as you file existing file because in file name string it slef has been used internally
* for Mintree hadd following line has not to be commented out 
        1. submitCondor.sh  L63 i.e  input="$ntupleT2Path Minitree_$(cut..........
        2. runAtCondor.sh   L36 i.e  rsync -avz ${_CONDOR_SCRATCH_DIR}/tryout/Minitree*.root $myArg3
        3. runAtCondor.sh   L25 i.e  ./hadd.sh $myArg1 . $myArg2 -j4    
##Run had Cutflow
* All the paths and to be in put file which has to have the same name convestion as you file existing file because in file name string it slef has been used internally
* for Cuflow hadd following line has not to be commented out
        1. submitCondor.sh  L64 i.e  input="$ntupleT2Path Cutflow_$(cut..........
        2. runAtCondor.sh   L37 i.e  rsync -avz ${_CONDOR_SCRATCH_DIR}/tryout/Cutflow*.root $myArg3
        3. runAtCondor.sh   L26 i.e  ./hadd_hist.sh $myArg1 . $myArg2 -j4
