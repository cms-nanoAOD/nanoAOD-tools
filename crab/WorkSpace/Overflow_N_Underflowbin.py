import numpy as np
import ROOT as rt
def DrawOverflow(h):
    nx = h.GetNbinsX()+1 # original histogram bin + 1 
    xbins=[]  # array for bins               
    for i in range(0,nx):
        xbins.append(h.GetBinLowEdge(i+1))    # set the bin array by getting the lower edges of histogram of interest
    xbins.append(xbins[nx-1]+h.GetBinWidth(nx)) # add one more entry = last entry in array + histogram last bin width
    npxbins =  np.array(xbins)  #conver in numpy array
    htmp = rt.TH1F("", "", nx, npxbins)  # define new hisogram with added bin
    #print "hsitogram new bins : ", npxbins
    for  i in range(0,nx+1):  #nx+1 bin contect will be over flow bin
        htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(i)),h.GetBinContent(i))
        htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(i)),h.GetBinError(i))
    htmp.SetEntries(h.GetEffectiveEntries())
    return htmp

def DrawUnderflow(h):
    nx = h.GetNbinsX()+1
    xbins = nx+1
    xbins=[]
    for i in range(0,nx):
        xbins.append(h.GetBinLowEdge(i+1))
    lowestbin=xbins[0]-h.GetBinWidth(1) # this bin has to be added lover side of array

    npxbins =  np.array(xbins)
    npxbins = np.insert(npxbins,0,lowestbin) #inserting new bin edge at 0th element
    htmp = rt.TH1F("", "", nx, npxbins)
    #print "hsitogram new bins : ", npxbins
    for  i in range(0,nx+1): #0-1 bin contect will be underflow bin
        htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(i+1)),h.GetBinContent(i))
        htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(i+1)),h.GetBinError(i))
    htmp.SetEntries(h.GetEffectiveEntries())
    return htmp

def DrawOverflow_N_DrawUnderflow(h):
    #rt.gROOT.cd()
    nx = h.GetNbinsX()  # original histogram bin + 1 
    xbins=[]  # array for bins
    lowestbin=h.GetBinLowEdge(1)-h.GetBinWidth(1)
    xbins.append(lowestbin) 
    for i in range(0,nx+1):
        xbins.append(h.GetBinLowEdge(i+1))    # set the bin array by getting the lower edges of histogram of interest
    xbins.append(h.GetBinLowEdge(nx+1)+h.GetBinWidth(nx)) # add one more entry = last entry in array + histogram last bin width
    npxbins =  np.array(xbins)  #conver in numpy array
    htmp = rt.TH1F("", "", nx+2, npxbins)  # define new hisogram with added bin
    #print("hsitogram new bins : ", xbins)
    for  i in range(0,nx+2):  #nx+1 bin contect will be over flow bin
        htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(i+1)),h.GetBinContent(i))
        htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(i+1)),h.GetBinError(i))
    htmp.SetEntries(h.GetEffectiveEntries())
    #print htmp.GetNbinsX()
    return htmp

