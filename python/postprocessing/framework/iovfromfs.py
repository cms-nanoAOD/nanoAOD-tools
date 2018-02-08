import os
import re


class IOVFromFileSystem:
    def __init__(self, baseDir,objectBuilder=lambda(x): x):
        self.baseDir = baseDir
        self.objectBuilder = objectBuilder
	self.instances={}
	subdirs=next(os.walk(self.baseDir))[1]
	for s in subdirs :
           m=re.match("([0-9]+)-([0-9])+)") 			    
	   if m :
		self.instances[(m.group(0),m.group(1))]=(baseDir+"/"+s,None)
	print "Found %d IOVs in folder %s"%(len(self.instances),baseDir)	

    def find(run):
	for first,last in self.instances.keys() :
	    if run >= first and run <= last :
	        return (first,last) 
	return None	
    def instance(self,run):
	if run==self.lastRun : return self.lastInstance
	self.lastRun=run
	runRange=self.find(run)
	if not runRange :
		print "Cannot find an IOV for run ", run, "in run ranges:",self.instances.keys()
	if  not self.instances[runRange][1] :
		self.instances[runRange][1]=self.objectBuilder( self.instances[runRange][0] )
	self.last=self.instances[runRange][1]	
	return self.lastInstance 
