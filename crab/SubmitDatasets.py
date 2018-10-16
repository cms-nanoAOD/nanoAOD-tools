import getpass
import os
import sys

import imp, os, json
from optparse import OptionParser,OptionGroup

parser = OptionParser()
g1 = OptionGroup(parser,"Analysis options")
g1.add_option("-c", "--cfg-file", dest="cfg_file", help="Config file containing PostProcessor instance", default="")
parser.add_option_group(g1)

g2 = OptionGroup(parser,"Stageout options")
g2.add_option("-s", "--storage-site", dest="storageSite", help="site where the output should be staged out (T2_XX_YYYY)")
g2.add_option("-d", "--output-dir", dest="outputDir", help="name of the directory where files will be staged out", default="nanoAOD")
g2.add_option("-l", "--production-label", dest="production_label", help="production label", default="myHeppyCrabProdDummy")

parser.add_option_group(g2)
g2.add_option("--only-unpacked", dest="only_unpacked", default=False, action="store_true", help="Only return the unpacked files, not the whole compressed output directory")

parser.add_option("-n", "--dryrun", dest="dryrun", action="store_true",default=False, help="dryrun")
parser.add_option("-w", "--siteWhitelist", dest="siteWhitelist", type="string", action="append", default=[], help="Sites whitelist")
parser.add_option("-N", dest="maxevents", default=-1, help="maximum number of events to process per run (for debugging purposes)")

(options,args) = parser.parse_args()



os.environ["PROD_LABEL"]  = options.production_label
os.environ["STAGEOUTREMDIR"] = options.outputDir
os.environ["CFG_FILE"] = options.cfg_file
os.environ["OUTSITE"] = options.storageSite
if len(options.siteWhitelist)>0: os.environ["WHITESITES"] = ','.join(options.siteWhitelist)
if options.maxevents>0: os.environ["MAXNUMEVENTS"] = str(options.maxevents)
os.environ["ONLYUNPACKED"] = str(options.only_unpacked)

from PhysicsTools.NanoAODTools.postprocessing.datasets.tests2017 import samples


for dataset in samples:
    os.environ["DATASET"] = str(dataset)
    #os.environ["NJOBS"] = str(len(split([comp])))
    os.system("crab submit %s -c crab_config_env.py"%("--dryrun" if options.dryrun else ""))

