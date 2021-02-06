import math
import copy
from array import array
from ROOT import *
import sympy

def getIntegral(function, bmin, bmax):
    return function.Integral(bmin,bmax)/(bmax-bmin)

def totalError(func, npars, pars, sigmas, cov_matrix, bmin, bmax):
    errorup = 0.
    errordown = 0.
    for i in range(npars):
        for j in range(npars):
            if i<= j:
                print 'cov matrix element ', i, j, cov_matrix[i][j]
                print 'pars' ,  pars[i], 'sigmas ', sigmas[i]
                print 'pars' ,  pars[j], 'sigmas ', sigmas[j]
                print 'func param ', i, func.GetParameter(i)
                print 'func param ', j, func.GetParameter(j)
                nominal = getIntegral(func, bmin, bmax)
                print 'nominal ' , nominal
                func.SetParameter(i, pars[i] + sigmas[i])
                iup = getIntegral(func, bmin, bmax)
                func.SetParameter(i, pars[i])
                print 'iup ', iup
                func.SetParameter(j, pars[j] + sigmas[j])
                jup = getIntegral(func, bmin, bmax)
                func.SetParameter(j, pars[j])
                print 'jup ', jup
                print 'func param ', i, func.GetParameter(i)
                print 'func param ', j, func.GetParameter(j)
                errorup += (iup - nominal)/sigmas[i]*(jup - nominal)/sigmas[j]*cov_matrix[i][j]
                func.SetParameter(i, pars[i])
                print 'error up ', errorup
                func.SetParameter(i, pars[i] - sigmas[i])
                idown = getIntegral(func, bmin, bmax)
                func.SetParameter(i, pars[i])
                print 'idown ', idown
                func.SetParameter(j, pars[j] - sigmas[j])
                jdown = getIntegral(func, bmin, bmax)
                func.SetParameter(j, pars[j])
                print 'jdown ', jdown
                print 'func param ', i, func.GetParameter(i)
                print 'func param ', j, func.GetParameter(j)
                errordown += (nominal - idown)/sigmas[i]*(nominal - jdown)/sigmas[j]*cov_matrix[i][j]
                print 'error down ', errordown
    return math.sqrt(errorup), math.sqrt(errordown)

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


def fittedHisto(histo,function,npars=-1,onlyCentral=False,behavior="nominal",doRemove=True,verbose=True,fitrange=None):
    if fitrange is None: 
        fitresults=histo.Fit(function,"SI")
    else:
        fitresults=histo.Fit(function,"SI","",fitrange[0],fitrange[1])
    covmatrix=fitresults.GetCovarianceMatrix()
    corrmatrix=fitresults.GetCorrelationMatrix()
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
        content_x= getIntegral(function, minb, maxb)
        if not (fitrange is None):
            isOutOfBounds=(maxb<=fitrange[0] ) or ( minb>=fitrange[1] )   
            if isOutOfBounds:
                content_x=histo.GetBinContent(b)
        if(verbose):print "bin ",b," min , max ",minb," , ",maxb," orig ",histo.GetBinContent(b)," fit ", content_x 
        h_ret.SetBinContent(b,content_x)
    hs_ret[0]=h_ret    
    if(behavior=="shape_only"):
        if(hs_ret[0].Integral()):
            hs_ret[0].Scale(histo.Integral()/hs_ret[1*(0)].Integral())
    if onlyCentral:
        return hs_ret
    if(verbose):print "zero integral ",h_ret.Integral()
    h_ret_up=copy.deepcopy(histo)
    h_ret_up.SetName((str(histo.GetName()+"TFup")))
    h_ret_down=copy.deepcopy(histo)
    h_ret_down.SetName((str(histo.GetName()+"TFdown")))
    h_ret_up.Reset("ICES")
    h_ret_down.Reset("ICES")
    for b in xrange(1,histo.GetNbinsX()+1):
        minb=histo.GetBinLowEdge(b)
        maxb=histo.GetBinLowEdge(b+1)
        content_x= getIntegral(function, minb, maxb)
        
        isOutOfBounds=False
        if not (fitrange is None):
            isOutOfBounds=(maxb<=fitrange[0] ) or ( minb>=fitrange[1] )   
        content_x_up, content_x_down = totalError(function, npars, pars, variations, covmatrix, minb, maxb)
        print '********************************************************************************************************************'
        if(verbose): print "bin ",b," min , max ",minb," , ",maxb," orig ",histo.GetBinContent(b)," fit up ", content_x_up , " nominal, ", content_x, " fit down ",content_x_down
        h_ret_down.SetBinContent(b,content_x - content_x_down)
        h_ret_up.SetBinContent(b,content_x + content_x_up)
        print 'h_ret_down bin content ', h_ret_down.GetBinContent(b), 'h_ret_up bin content ', h_ret_up.GetBinContent(b)
        print '********************************************************************************************************************'

    hs_ret[1]=h_ret_up
    hs_ret[2]=h_ret_down
    return hs_ret

