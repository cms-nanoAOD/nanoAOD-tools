import os
import sys
import math
import json
import ROOT
import random
import hashlib
import json
import struct

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class EventDump(Module):

    def __init__(
        self,
        inputCollections = [
            [lambda event: Collection(event, "Electron"),["pt"]]
        ],
        saveAs = None,
        compareTo = None
    ):
        self.inputCollections = inputCollections
        self.saveAs = saveAs
        self.compareTo = compareTo
       
    def beginJob(self):
        self.nEvents = 0
        self.blockchain = {}#{-1:{"chain":hashlib.md5("123456")}}
        self.blockchain_ref = None
        if self.compareTo and os.path.exists(self.compareTo):
            f = open(self.compareTo)
            self.blockchain_ref = json.load(f)
            print self.blockchain_ref.keys()
        self.matched = 0
        self.missing = 0
        self.mismatched = 0
        
    def floatToBits(self,f):
        s = struct.pack('>f', f)
        return struct.unpack('>l', s)[0]
        
    def endJob(self):
        print "Total events with objects: ",self.nEvents
        #print "Final hash: ",self.blockchain[-1]["chain"].hexdigest()
        if self.saveAs:
            #for k in self.blockchain.keys():
            #    self.blockchain[k]["chain"] = self.blockchain[k]["chain"].hexdigest()
            f = open(self.saveAs,"w")
            json.dump(self.blockchain,f,ensure_ascii=True,indent=2)
            f.close()
        if self.blockchain_ref:
            print "matched: %i, mismatched: %i, missing: %i"%(self.matched,self.mismatched,self.missing)
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        #print "Event:",event._entry
        hasObjs = 0
        block = {"collections":[]}
        eventHash = hashlib.md5("%07i"%event._entry)
        for inputCollection in self.inputCollections:
            collection = inputCollection[0](event)
            collectionBlock = {"name":collection._prefix,"len":len(collection),"objs":[]}
            eventHash.update("%s%02i"%(collection._prefix,len(collection)))
            if len(collection)>0:
                hasObjs += len(collection)
                #print " - collection %s:"%collection._prefix, len(collection)
                for i,obj in enumerate(collection):
                    objBlock = {}
                    #print " - - %i:"%i,
                    for feature in inputCollection[1]:
                        objBlock[feature] = getattr(obj,feature)
                        eventHash.update("%20i"%self.floatToBits(objBlock[feature]))
                        #print feature+"="+str(objBlock[feature]),
                    #print
                    collectionBlock["objs"].append(objBlock)
            block["collections"].append(collectionBlock)
        block["hash"] = eventHash.hexdigest()
        if self.blockchain_ref:
            
            if not self.blockchain_ref.has_key('%i'%event._entry):
                print "missing in ref: ",event._entry
                print block
                self.missing += 1
            elif self.blockchain_ref['%i'%event._entry]["hash"]!=block["hash"]:
                print "mismatched: ",event._entry
                print "--- ref ---"
                print self.blockchain_ref['%i'%event._entry]
                print "--- here ---"
                print block
                self.mismatched += 1
            else:
                self.matched += 1
        #block["chain"] = self.blockchain[event._entry-1]["chain"].copy()
        #block["chain"].update(eventHash.hexdigest())
        self.blockchain[event._entry] = block
        if hasObjs:
            self.nEvents+=1
        return True
        
