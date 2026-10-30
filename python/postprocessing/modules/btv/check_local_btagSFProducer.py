import ROOT
import timeit
# from within CMSSW:

libstart = timeit.default_timer()

#ROOT.gSystem.Load('libCondFormatsBTauObjects')
#ROOT.gSystem.Load('libCondToolsBTau')
for library in ["libCondFormatsBTauObjects", "libCondToolsBTau"]:
            if library not in ROOT.gSystem.GetLibraries():
                print("Load Library '%s'" % library.replace("lib", ""))
                ROOT.gSystem.Load(library)


libstop = timeit.default_timer()

print('Time to load library: ', libstop - libstart)


# OR using standalone code:
#ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

csvstart = timeit.default_timer()

# get the sf data loaded
calib = ROOT.BTagCalibration ('deepjet', '/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/btv/reshaping_deepJet_106XUL16postVFP_v3_modified.csv')#dummy_wp_deepJet_106XUL18_v2.csv')#DeepJet_106XUL17SF_V2p1.csv')

csvstop = timeit.default_timer()

print('Time to read csv : ', csvstop - csvstart)


reststart = timeit.default_timer()


v_sys = getattr(ROOT, 'vector<string>')()
#v_sys.push_back('up')
#v_sys.push_back('down')

# make a reader instance and load the sf data
#reader = ROOT.BTagCalibrationReader(2, 'central', v_sys)
reader = ROOT.BTagCalibrationReader(3, 'central', v_sys)

#reader = ROOT.BTagCalibrationReader (
#    3,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
#    v_sys,          # vector of other sys. types
#    "central",      # central systematic type
#) 

#reader.load(calib, 0, "mujets")
reader.load(calib, 0, 'iterativefit')

#reader.load(
#    calib,
#    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG
#    "comb"      # measurement type
#)

# in your event loop
sf = reader.eval_auto_bounds(
    'central',      # systematic (here also 'up'/'down' possible)
    0,              # jet flavor
    1.2,            # absolute value of eta
    31.             # pt
)


reststop = timeit.default_timer()

print('Time for rest code : ', reststop - reststart)

print(sf) 
