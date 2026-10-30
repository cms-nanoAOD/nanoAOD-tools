# Condor job subamission
                                                                                                     
## Warning
* In the script we are comming the dataset list form the minitree folder                             
* Make sure the key is the dataset is same as what we are using in submitcondor.sh file              
* Make sure crab_script_minitree.py have at least one line which statrt with InputFiles i.e "#" other wise input file will not be overwritten in this file
                                                                                                     
##Uses                                                                                               
* Main file which submit the condor jobs is "submitCondor.sh"
* 4 input are required to run exicutable "submitCondor.sh" i.e  year sample lep region
* example ./submitCondor.sh UL2016preVFP Mc mu 2J1T1
~                                                                
