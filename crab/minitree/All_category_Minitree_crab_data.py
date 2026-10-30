import fileinput, string, sys, os, time

if len(sys.argv) != 3:
        print "USAGE: %s <Data year>  <lep flavour>"%(sys.argv [0])
        sys.exit (1)
year   = sys.argv [1]
lep    = sys.argv [2]

def replacemachine(fileName, sourceText, replaceText):
    print "editing ",fileName,
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################
regions = ['2J1T1','2J1T0']#['2J1T1','2J1T0']#['2J0T1','2J0T0']#['3J1T1','3J1T0']#['3J2T1','3J2T0'] 
for region in regions:
	region_tag = '    region_tag = "'+region+'"\n'
	replacemachine('crab_submission_Minitree_data.py','region_tag =',region_tag)
  	cmd_crab_submit = "python crab_submission_Minitree_data.py "+year+" "+lep 
	os.system(cmd_crab_submit)
	
