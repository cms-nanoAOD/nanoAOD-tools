function run_test()
{
    touch /var/lib/rpm/* || return 1
    yum -y install wget rsync yum-plugin-ovl || return 1
    yum -y install glibc-devel.x86_64 --disablerepo=adobe* || return 1
    cd ~
    source ~/.bashrc
    export SCRAM_ARCH=slc6_amd64_gcc630 || return 1
    scramv1 project CMSSW CMSSW_10_2_0_pre2 || return 1
    cd CMSSW_10_2_0_pre2/src || return 1
    eval `scramv1 runtime -sh` || return 1
    mkdir -p PhysicsTools/NanoAODTools
    rsync -r --stats /scripts/ PhysicsTools/NanoAODTools/. || return 1
    scram b || return 1
    
    wget -nv https://github.com/LLPDNNX/test-files/raw/master/nanoaod/RunIISummer16NanoAODv2_MC.root || return 1
    python PhysicsTools/NanoAODTools/test/LLP/processNANOX.py --isData --input=https://github.com/LLPDNNX/test-files/raw/master/nanoaod/RunIISummer16NanoAODv2_MC.root || return 1
}


run_test
