import math
import copy
from array import array
from ROOT import *
def resizeHisto(histo,varbins,normalizeToBinWidth=True,addUnderflow=False,addOverflow=True,verbose=False):

    nbins=histo.GetNbinsX()
    mins={0:-14000}
    maxs={(len(varbins)):14000}
    if(verbose):print(len(varbins))
    for b in xrange(len(varbins)):
        if(verbose):print "b is ",b," varb ",varbins[b]
        mins[b+1]=varbins[b]
        maxs[b]=varbins[b]
    if(verbose):
        print "mins",mins
        print "maxs",maxs
    bincontent={}
    binerrors={}
    for bv in xrange(len(varbins)+1):
        sumbins =0
        sumerrs =0
#        print "bv ",bv," min,max ", mins[bv], " , ",maxs[bv]
        for b in xrange(nbins+2):#include underflow and overflow
            bb= histo.GetBinContent(b) 
            be= histo.GetBinError(b)

            minb=histo.GetBinLowEdge(b)
            maxb=histo.GetBinLowEdge(b+1)
#            print "bin ", b ," minb, maxb ",minb," , ",maxb, " cont ",bb
            if(bv>0):#bins at border are added to the b+1 bin except for the underflow, 
                if(maxb>mins[bv] and maxb<maxs[bv] and minb>mins[bv-1] and minb < mins[bv] ):
#                    if(verbose):print(" adding bc of edge")
                    sumbins=sumbins+bb
                    sumerrs=sumerrs+be*be
                if(maxb>mins[bv] and maxb<maxs[bv] and minb<mins[bv-1]):
                   print "warning! Histo has larger bins than resized binning! Check bin ",b," min, max ",minb," , ",maxb," vs previous resized min max", mins[bv-1]," , " ,maxs[bv-1]
                   print(" adding fractional content according to relative bin width, pray it works!")
                   fracb=(maxb-mins[bv])/(maxb-minb)#need to take only the fraction of bin in resized bin
                   sumbins=sumbins +bb *fracb
                   sumerrs=sumerrs+be*be*fracb*fracb
                   
            if(minb>=mins[bv] and maxb<=maxs[bv]):
#                if(verbose): print(" adding bc at center")
                sumbins=sumbins+bb
                sumerrs=sumerrs+be*be
            if(maxb>maxs[bv] and minb<mins[bv]):
                print "warning! Histo has larger bins than resized binning! Check bin ",b," min, max ",minb," , ",maxb," vs resized min max", mins[bv]," , " ,maxs[bv]
                print(" adding fractional content according to bin width, pray it works!")
                fracb=(maxs[bv]-mins[bv])/(maxb-minb)
                sumbins=sumbins +bb *fracb
                sumerrs=sumerrs+be*be*fracb*fracb

        bincontent[bv]=(sumbins)
        binerrors[bv]=(math.sqrt(sumerrs))
    if(addUnderflow): #NOT default behavior, add underflow to first bin
        bincontent[1]=bincontent[1]+bincontent[0] #default behavior, add overflow to last bin
        binerrors[1]=math.sqrt(binerrors[1]*binerrors[1]+binerrors[0]*binerrors[0])
        bincontent[0]=0
        binerrors[0]=0
    if(addOverflow):
        #print(bincontent.keys())
        bincontent[len(bincontent)-2]=bincontent[len(bincontent)-1]+bincontent[len(bincontent)-2] #default behavior, add overflow to last bin
        binerrors[len(bincontent)-2]=math.sqrt(binerrors[len(bincontent)-1]*binerrors[len(bincontent)-1]+binerrors[len(bincontent)-2]*binerrors[len(bincontent)-2])

        bincontent[len(bincontent)-1]=0
        binerrors[len(bincontent)-1]=0
    darray=array('d',varbins)
    #    print(darray)
    if(verbose):print"histoin name",histo.GetName()
    h_ret=TH1D(str(histo.GetName()),str(histo.GetTitle()),len(darray)-1,darray)
    for bv in xrange(len(varbins)+1):
        sf=1.0
        if normalizeToBinWidth:#default behavior: we assume same width bins and rescale to that.
            sf=histo.GetBinWidth(1)/(maxs[bv]-mins[bv])
        h_ret.SetBinContent(bv,bincontent[bv]*sf)
        h_ret.SetBinError(bv,binerrors[bv]*sf)
    return h_ret,maxs,mins,bincontent,binerrors    


def fittedHisto(histo,function,npars=-1,onlyCentral=False,behavior="nominal",doRemove=True,verbose=False):
    fitresults=histo.Fit(function,"S")
    corrmatrix=fitresults.GetCovarianceMatrix()
    if(verbose):
        print fitresults
        print corrmatrix
    hs_ret={}
    pars=[]
    variations=[]
    if npars==-1:
        npars=fitresults.NTotalParameters()
        if(verbose):        print "ntotal parameters ",npars
    for p in xrange(npars):
        if(verbose):print "parameter ", p, " value ",fitresults.Value(p), " error ",  fitresults.Error(p)
        pars.append(fitresults.Value(p))
        variations.append(fitresults.Error(p))
        
    if(doRemove):
        if(verbose):
            print histo.GetListOfFunctions().ls()
            print function
        hn = histo.GetListOfFunctions().FindObject(str(function.GetName()))
        histo.GetListOfFunctions().remove(hn)
        if(verbose):
            print histo.GetListOfFunctions().ls()
        
    #h_ret=histo.Clone((str(histo.GetName()+"nominal")))
    h_ret=copy.deepcopy(histo)
    h_ret.SetName((str(histo.GetName()+"nominal")))
    h_ret.Reset("ICES")
    for b in xrange(1,histo.GetNbinsX()+1):
        minb=histo.GetBinLowEdge(b)
        maxb=histo.GetBinLowEdge(b+1)
        content_x=function.Integral(minb,maxb)/(maxb-minb)
        if(verbose):print "bin ",b," min , max ",minb," , ",maxb," orig ",histo.GetBinContent(b)," fit ", content_x 
    
        h_ret.SetBinContent(b,content_x)
    hs_ret[0]=h_ret    
    if(behavior=="shape_only"):
        if(hs_ret[0].Integral()):
            hs_ret[0].Scale(histo.Integral()/hs_ret[1*(0)].Integral())
    if onlyCentral:
        return hs_ret
    if(verbose):print "zero integral ",h_ret.Integral()
    for p in xrange(npars):
#        h_ret_up=histo.Clone(str(histo.GetName()+"par"+str(p)+"up"))
#        h_ret_down=histo.Clone(str(histo.GetName()+"par"+str(p)+"down"))
        h_ret_up=copy.deepcopy(histo)
        h_ret_up.SetName((str(histo.GetName()+"par"+str(p)+"up")))
        h_ret_down=copy.deepcopy(histo)
        h_ret_down.SetName((str(histo.GetName()+"par"+str(p)+"down")))
        h_ret_up.Reset("ICES")
        h_ret_down.Reset("ICES")
        for b in xrange(1,histo.GetNbinsX()+1):
            minb=histo.GetBinLowEdge(b)
            maxb=histo.GetBinLowEdge(b+1)
            #
            function.SetParameter(p,pars[p]+variations[p])
            content_x_up=function.Integral(minb,maxb)/(maxb-minb)
            h_ret_up.SetBinContent(b,content_x_up)
            

            function.SetParameter(p,pars[p]-variations[p])
            content_x_down=function.Integral(minb,maxb)/(maxb-minb)
            h_ret_down.SetBinContent(b,content_x_down)

            function.SetParameter(p,pars[p])
            content_x=function.Integral(minb,maxb)/(maxb-minb)
            #            h_ret_up.SetBinContent(b,content_x_down)
            
            if(verbose): print "bin ",b," min , max ",minb," , ",maxb," orig ",histo.GetBinContent(b)," fit up ", content_x_up , " nominal, ", content_x, " fit down ",content_x_down

        hs_ret[p+1]=h_ret_up
        hs_ret[-1*(p+1)]=h_ret_down
        if(verbose):
            print "par ",p+1,"integral ",hs_ret[p+1].Integral()
            print "par ",-1*(p+1),"integral ",hs_ret[-1*(p+1)].Integral()
        if(behavior=="shape_only"):
            if(hs_ret[p+1].Integral()):
                hs_ret[p+1].Scale(histo.Integral()/hs_ret[1*(p+1)].Integral())
#                hs_ret[p+1].Scale(hs_ret[0].Integral()/hs_ret[1*(p+1)].Integral())
            if(hs_ret[-1*(p+1)].Integral()):
                hs_ret[-1*(p+1)].Scale(histo.Integral()/hs_ret[-1*(p+1)].Integral())
#                hs_ret[-1*(p+1)].Scale(hs_ret[0].Integral()/hs_ret[-1*(p+1)].Integral())

    return hs_ret

