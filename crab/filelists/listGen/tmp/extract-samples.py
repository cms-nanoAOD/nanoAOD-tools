#!/bin/python

from jacopo import sample

print "Length of dictionary : %d" % len (sample)

SM = open("SM.py","w")
SM.write("#!/usr/bin/env python\n")
SM.write(' \n')
SM.write('FIXME="1"\n')
SM.write(' \n')
SM.write("processes =    {\n")

BSM = open("BSM.py","w")
BSM.write("#!/usr/bin/env python\n")
BSM.write(' \n')
BSM.write('FIXME="1"\n')
BSM.write(' \n')
BSM.write("processes =    {\n")

data = open("data.py","w")
data.write("#!/usr/bin/env python\n")
data.write(' \n')
data.write('FIXME="1"\n')
data.write(' \n')
data.write("processes =    {\n")


for key in sorted(sample.iterkeys()):

    #seperate signal
    if any([x in key for x in ['BBbarDMJets','TTbarDMJets','Radion','prime','Grav','Wp','GluGlu','HW','HZ','HH','WG','ZG','Wm']]):
        BSM.write("\t'%s':('MC',%s,%s,%s,%s),\n" %(key,sample[key]['nevents'],sample[key]['xsec'],sample[key]['matcheff'],sample[key]['kfactor']) )
    #seperate data
    elif any([x in key for x in ['Run']]):
        data.write("\t'%s':('MC',%s,%s,%s,%s),\n" %(key,sample[key]['nevents'],sample[key]['xsec'],sample[key]['matcheff'],sample[key]['kfactor']) )
    else:
        SM.write("\t'%s':('MC',%s,%s,%s,%s),\n" %(key,sample[key]['nevents'],sample[key]['xsec'],sample[key]['matcheff'],sample[key]['kfactor']) )
    #print key
    #print sample[key]['nevents']
    #print sample[key]['xsec']
    #print sample[key]['matcheff']
    #print sample[key]['kfactor']

SM.write(' \n')
SM.write("}\n")
SM.close()

BSM.write(' \n')
BSM.write("}\n")
BSM.close()

data.write(' \n')
data.write("}\n")
data.close()
