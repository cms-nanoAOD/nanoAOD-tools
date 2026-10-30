import math
import cmath
import ROOT
def poly1(x):
    return x 

def poly2(x):
    return (0.5*(3*x*x - 1))

def poly3(x):
    return (0.5*(5*x*x*x-3*x))

def wolformvalue2J(p,Pt1,Pt2):
    r=0
    if(Pt1 < Pt2): r=(Pt1/Pt2)
    else:  r=(Pt2/Pt1)
    return ((1+2*r*p+r*r)/((1+r)*(1+r)))

def wolformvalue3J(v1,v2,v3 ):
        
        #print 'function called'
        if(v1.Pt() <= v2.Pt() and v2.Pt() <= v3.Pt()): 
            Jet1_4v=v3
            Jet2_4v=v2
            Jet3_4v=v1
        elif(v1.Pt() <= v3.Pt() and v3.Pt() <= v2.Pt()): 
            Jet1_4v=v2
            Jet2_4v=v3
            Jet3_4v=v1
        elif(v2.Pt() <= v1.Pt() and v1.Pt() <= v3.Pt()): 
            Jet1_4v=v3
            Jet2_4v=v1
            Jet3_4v=v2
        elif(v2.Pt() <= v3.Pt() and v3.Pt() <= v1.Pt()):
            Jet1_4v=v1
            Jet2_4v=v3
            Jet3_4v=v2
        elif(v3.Pt() <= v2.Pt() and v2.Pt() <= v1.Pt()):
            Jet1_4v=v1
            Jet2_4v=v2
            Jet3_4v=v3
        elif(v3.Pt() <= v1.Pt() and v1.Pt() <= v2.Pt()):
            Jet1_4v=v2
            Jet2_4v=v1
            Jet3_4v=v3
        #print "Jet2_4v/Jet1_4v = ",Jet2_4v.Pt()/Jet1_4v.Pt(),";Jet3_4v/Jet1_4v = ",Jet3_4v.Pt()/Jet1_4v.Pt()
        else: print("v1Pt = %s v2Pt = %s v3Pt = %s"%(v1.Pt(),v2.Pt(),v3.Pt()))
        delta_12= Jet1_4v.Angle(Jet2_4v.Vect())
        delta_23= Jet2_4v.Angle(Jet3_4v.Vect())
        delta_13= Jet1_4v.Angle(Jet3_4v.Vect())

        r2=Jet2_4v.Pt()/Jet1_4v.Pt()
        r3=Jet3_4v.Pt()/Jet1_4v.Pt();


        foxvalue1= ((1+r2*r2+r3*r3+2*r2*poly1(math.cos(delta_12))+2*r3*poly1(math.cos(delta_13))+2*r2*r3*poly1(math.cos(delta_23)))/((1+r2+r3)*(1+r2+r3)));
        foxvalue2= ((1+r2*r2+r3*r3+2*r2*poly2(math.cos(delta_12))+2*r3*poly2(math.cos(delta_13))+2*r2*r3*poly2(math.cos(delta_23)))/((1+r2+r3)*(1+r2+r3)));
        foxvalue3= ((1+r2*r2+r3*r3+2*r2*poly3(math.cos(delta_12))+2*r3*poly3(math.cos(delta_13))+2*r2*r3*poly3(math.cos(delta_23)))/((1+r2+r3)*(1+r2+r3)));
        return [foxvalue1,foxvalue2,foxvalue3] 


#def CollectJetInfo(jet):
#       return [jet.mass,jet.pt,jet.eta,abs(jet.eta),jet.phi,jet.btagDeepFlavB,jet.hadronFlavour,jet.p4()]

def CollectJetInfo(jet):
        return [jet.mass,jet.pt,jet.eta,abs(jet.eta),jet.phi,jet.btagDeepFlavB,jet.p4()]

def cbrt(num):
    if(num>=0):
        return (num)**(1./3.) 
    else:
        return (-(-num)**(1./3.))
    
def EquationSolve( a, b, c,d):
    #print "EquationA = %s EquationB = %s EquationC = %s EquationD = %s" % (a,b,c,d)
    result=[]
    if(a != 0):
        q = (3*a*c-b*b)/(9*a*a)
        r = (9*a*b*c - 27*a*a*d - 2*b*b*b)/(54*a*a*a)
        Delta = q*q*q + r*r
        #print "q = %s r = %s Delta = %s " % (q,r,Delta)
        if( Delta<=0):
            # print "discriminet less than zero"
             rho = math.sqrt(-(q*q*q))
             #print "r/rho = ",r/rho
             theta = math.acos(r/rho)
             #print "rho = %s theta = %s"%(rho,theta)   
             thetabythree = theta/3.0
             s = cmath.rect(math.sqrt(-q),theta/3.0)
             #print "s = ",s
             t = cmath.rect(math.sqrt(-q),-theta/3.0)
             #print "t = ",t
        
        if(Delta>0):
             s = complex(cbrt(r+math.sqrt(Delta)),0) 
             #print s
             t = complex(cbrt(r-math.sqrt(Delta)),0)
      
        i = complex(0,1.0)
        x1 = s+t+complex(-b/(3.0*a),0)
        x2 = (s+t)*complex(-0.5,0)-complex(b/(3.0*a),0)+(s-t)*i*complex(math.sqrt(3)/2.0,0)
        x3 = (s+t)*complex(-0.5,0)-complex(b/(3.0*a),0)-(s-t)*i*complex(math.sqrt(3)/2.0,0)
        
        if(abs(x1.imag)<0.0001):result.append(x1.real)
        if(abs(x2.imag)<0.0001):result.append(x2.real)
        if(abs(x3.imag)<0.0001):result.append(x3.real)

        return result
    else:
        return result

def solveNu4Momentum(lep_, metpx, metpy):
  
    useNegativeDeltaSolutions_ = True
    usePositiveDeltaSolutions_ = True
  
    # in case of real solution use the abs min pz
    usePzMinusSolutions_ = False
    usePzPlusSolutions_ = False
    usePzAbsValMinimumSolutions_ = True
  
    #vary px,py to find the solution in complex case
    usePxMinusSolutions_ = True
    usePxPlusSolutions_ = True
  
    #set root=0 in complex case
    useMetForNegativeSolutions_ = False
  
    mW = 80.38
    MisET2 = (metpx*metpx + metpy*metpy)
    labda= (mW*mW)/2 + metpx*lep_.Px() + metpy*lep_.Py()
    #print lep_.Pz()
    #print lep_.Energy()
    #print lep_.Energy()*lep_.Energy() - lep_.Pz()*lep_.Pz()
    a = (labda*lep_.Pz())/(lep_.Energy()*lep_.Energy() - lep_.Pz()*lep_.Pz()) #ignoring the mass of the lepton
    a2 = pow(a,2.);
    b = (pow(lep_.Energy(),2.)*(MisET2) - pow(labda,2.))/(pow(lep_.Energy(),2) - pow(lep_.Pz(),2));

    #print "mW =%s MisET2 =%s labda =%s  a =%s a2 =%s b =%s "%(mW, MisET2,labda,a,a2,b)
    pz1=0.0
    pz2=0.0
    pznu=0.0
    Enu = 0.0 
    #bool realRoot=false; bool iRoot=false;
    p4nu_rec=ROOT.TLorentzVector() #math::XYZTTLorentzVector p4lep_rec;
    #print "a2-b = ",a2-b 
    if((a2-b >=0)  and usePositiveDeltaSolutions_):  #   realRoot
        #print "real root"
        root = math.sqrt(a2-b)
        pz1 = a + root
        pz2 = a - root
    
        if(usePzPlusSolutions_): pznu = pz1
        if(usePzMinusSolutions_): pznu = pz2
        if(usePzAbsValMinimumSolutions_):
            pznu = pz1
            if(abs(pz1)>abs(pz2)): pznu = pz2
        Enu = math.sqrt(MisET2 + pznu*pznu)
        p4nu_rec.SetPxPyPzE(metpx,metpy,pznu,Enu)
    elif((a2-b < 0) and  useNegativeDeltaSolutions_): #imaganry sloutions
        #print "imaganry root"
        ptlep = lep_.Pt()
        pxlep = lep_.Px()
        pylep = lep_.Py()
        EquationA = 1;
        EquationB = -3*pylep*mW/(ptlep);
        EquationC = mW*mW*(2*pylep*pylep)/(ptlep*ptlep)+mW*mW-4*pxlep*pxlep*pxlep*metpx/(ptlep*ptlep)-4*pxlep*pxlep*pylep*metpy/(ptlep*ptlep);
        EquationD = 4*pxlep*pxlep*mW*metpy/(ptlep)-pylep*mW*mW*mW/ptlep;
   #    print "EquationA = %s EquationB = %s EquationC = %s EquationD = %s" % (EquationA,EquationB,EquationC,EquationD) 
        solutions = EquationSolve(float(EquationA),float(EquationB),float(EquationC),float(EquationD))
        solutions2 = EquationSolve(float(EquationA),-float(EquationB),float(EquationC),-float(EquationD))
        #print "solutions = %s solutions2 = %s"%(solutions[0],solutions2[0])
        deltaMin = 14000*14000;
        zeroValue = -mW*mW/(4*pxlep);
        minPx=0;
        minPy=0;
    
        # print "a = %s b = %s c = %s d = %s "%f (EquationA,EquationB,EquationC,EquationD)
    
        if(usePxMinusSolutions_):
            for i in range(0,len(solutions)):
                if(solutions[i]<0 ): continue
                p_x = (solutions[i]*solutions[i]-mW*mW)/(4*pxlep)
                p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x -mW*ptlep*solutions[i])/(2*pxlep*pxlep)
                Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy)
                #print "intermediate solution1 met x = %s min px = %s metpy = %s min py = %s" %f (metpx,p_x,metpy,p_y)
            
                if(Delta2< deltaMin and Delta2 > 0):
                    deltaMin = Delta2
                    minPx=p_x
                    minPy=p_y
            #print "intermediate solution1 met x = %s min px = %s metpy = %s min py = %s" %f (metpx,p_x,metpy,p_y)
        if(usePxPlusSolutions_):
            for i in range(0,len(solutions2)):
                if(solutions2[i]<0): continue
                p_x = (solutions2[i]*solutions2[i]-mW*mW)/(4*pxlep)
                p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x +mW*ptlep*solutions2[i])/(2*pxlep*pxlep)
                Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy)
                #print "intermediate solution1 met x = %s min px = %s metpy = %s min py = %s" %f (metpx,p_x,metpy,p_y)

                if(Delta2< deltaMin and Delta2 > 0):
                    deltaMin = Delta2
                    minPx=p_x
                    minPy=p_y
                #print "intermediate solution1 met x = %s min px = %s metpy = %s min py = %s" %f (metpx,p_x,metpy,p_y)
        pyZeroValue = ( mW*mW*pxlep + 2*pxlep*pylep*zeroValue)
        delta2ZeroValue= (zeroValue-metpx)*(zeroValue-metpx) + (pyZeroValue-metpy)*(pyZeroValue-metpy)
    
        if(deltaMin<14000*14000):
            if(delta2ZeroValue < deltaMin):
                deltaMin = delta2ZeroValue
                minPx=zeroValue
                minPy=pyZeroValue
        
            #print " MtW2 from min py and min px  = ", math.sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy) 
            mu_Minimum = (mW*mW)/2 + minPx*pxlep + minPy*pylep
            a_Minimum = (mu_Minimum*lep_.Pz())/(lep_.Energy()*lep_.Energy() - lep_.Pz()*lep_.Pz())
            pznu = a_Minimum
        
            if not (useMetForNegativeSolutions_):
                Enu = math.sqrt(minPx*minPx+minPy*minPy + pznu*pznu)
                p4nu_rec.SetPxPyPzE(minPx,minPy,pznu,Enu)
            else:
                pznu = a
                Enu = math.sqrt(metpx*metpx+metpy*metpy + pznu*pznu)
                p4nu_rec.SetPxPyPzE(metpx,metpy,pznu,Enu)
  
    #print "metpx = %s metpy = %s pznu = %s Enu = %s"%(p4nu_rec.Px(),p4nu_rec.Py(),p4nu_rec.Pz(),p4nu_rec.E())
    return p4nu_rec   


#nut4v = ROOT.TLorentzVector()
#muon4v = ROOT.TLorentzVector()

#muon4v.SetPtEtaPhiE(104.081771851 ,0.272705078125 ,0.98046875, 107.975999494)
#nut4v = solveNu4Momentum(muon4v,-3.64258581356,292.429890046)
#print nut4v.Pt()," ",nut4v.Eta()," ",nut4v.Phi()," ",nut4v.M()," ",nut4v.E()

