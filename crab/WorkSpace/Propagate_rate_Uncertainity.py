
def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) >= 0:
            #hist.SetBinContent(i, hist.GetBinContent(i))
            #print(f" {hist.GetBinContent(i)}",f"bin : {i}")
            #print(f" {hist.GetBinContent(i) * uncert * 0.01}",f"bin : {i}")
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)
            #print(f" {hist.GetBinContent(i)}",f"bin : {i}")
        else:
            print(f"{uncert = }")
            print("Hist with bin with negative entry found")
            print(f"Hist Name : {hist.GetName()}",f"bin : {i}", f"containt : {hist.GetBinContent(i)}")
            hist.SetBinContent(i,0)
            print(f"set constant zero for the bin: {i}")
