from math import hypot, pi

#### ========= UTILITIES =======================
def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))

def closest(obj,collection,presel=lambda x,y: True):
    ret = None; drMin = 999
    for x in collection:
        if not presel(obj,x): continue
        dr = deltaR(obj,x)
        if dr < drMin: 
            ret = x; drMin = dr
    return (ret,drMin)

def matchObjectCollection(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        ( bm, dR ) = closest(obj, [ mobj for mobj in collection if presel(obj,mobj) ])
        if dR < dRmax:
            pairs[obj] = bm
        else:
            pairs[obj] = None
    return pairs

def matchObjectCollectionMultiple(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        matched = [] 
        for c in collection :
            if presel(obj,c) and deltaR( obj, c ) < dRmax :
                matched.append( c )
        pairs[obj] = matched
    return pairs
