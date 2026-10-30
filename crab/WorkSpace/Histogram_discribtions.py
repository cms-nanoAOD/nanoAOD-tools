import math

def get_histogram_distciption(Variable="lntopMass"):

    if(Variable=="lntopMass"):
            Variable="TMath::Log(topMass)"
            X_axies="#zeta"#ln(m_{t} / 1 GeV)"
            Y_axies="Events/(0.0265)"
            lest_bin=math.log(110.0)
            max_bin=math.log(260.0)
            Num_bin = 30
            #Num_bin=35
    elif("lntopMass_" in Variable ):
            Variable = Variable.rsplit("_")[1]
            Variable="TMath::Log(topMass_"+Variable+")"
            print(f"{Variable = }")
            X_axies="#zeta"#ln(m_{t} / 1 GeV)"
            Y_axies="Events/(0.0265)"
            lest_bin=math.log(110.0)
            max_bin=math.log(260.0)
            Num_bin = 30
            #Num_bin=35
    elif(Variable=="topMass"):
            X_axies="m_{t} GeV"
            Y_axies="Events/(10)"
            lest_bin=100.0
            max_bin=300.0
            Num_bin=20

    elif(Variable=="mtwMass"):
            X_axies="m_{T} (GeV)"
            Y_axies="Events/(10)"
            lest_bin=50.0
            max_bin=150.0
            Num_bin=10
    elif(Variable=="MuonCharge"):
            X_axies="#mu charge"
            Y_axies="Events/bin"
            lest_bin=-1.1
            max_bin=1.1
            Num_bin=3

    elif(Variable=="ElectronCharge"):
            X_axies="e charge"
            Y_axies="Events/bin"
            lest_bin=-1.1
            max_bin=1.1
            Num_bin=3
    
    elif(Variable=="t_ch_CAsi+ttbar_CAsi"):
            X_axies="Signal+TopBkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
            
    elif(Variable=="t_ch_CAsi"):
            X_axies="Signal Corr. Assign DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
      
    elif(Variable=="t_ch_WAsi"):
            X_axies="Signal Wrong Assign DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
    
    elif(Variable=="ttbar_CAsi"):
            X_axies="top bkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
    
    elif(Variable=="ttbar_WAsi"):
            X_axies="top bkg Wrong Assign DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
    
    elif(Variable=="EWK"):
            X_axies="EWK bkg DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
    
    elif(Variable=="QCD"):
            X_axies="QCD bkg DNN Sore"
            Y_axies="Events/(0.1)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=10
                
    elif(Variable=="t_ch_CAsi"):
                X_axies="DNN Response for corr. assign top signal"
                Y_axies="Events/(0.1)"
                lest_bin=0.0
                max_bin=1.0
                Num_bin=10
    else:
        print("variable ", Variable," in not define in Create_Workspace_input_file.py" )
        exit()

    return Variable,X_axies,Y_axies, lest_bin, max_bin, Num_bin
