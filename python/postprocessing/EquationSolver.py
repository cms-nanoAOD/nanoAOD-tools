import math as math
import cmath
import string
import io

def eqsolv(a1, a2, a3, a4):
    if type(a1) != float and type(a1) != int:
        if type(a1) == list:
            a = a1[0]
            b = a1[1]
            c = a1[2]
            d = a1[3]
        elif type(a1) == dict:
            a = a1['a']
            b = a1['b']
            c = a1['c']
            d = a1['d']
    else:
        a = a1
        b = a2
        c = a3
        d = a4

    if a != 0:
        q = (3*a*c - b*b)/(9*a*a)
        r = (9*a*b*c - 27*a*a*d - 2*b**3)/(54*a**3)
        Delta = q**3 + r**2

        if Delta <= 0:
            rho = (-q**(3))**(0.5)
            theta = math.acos(r/rho)
            s = cmath.rect((-q)**(0.5), theta/3.0)
            t = cmath.rect((-q)**(0.5), -theta/3.0)
        if Delta > 0:
            s = complex((r+(Delta)**(0.5))**(1./3), 0)
            t = complex((r+(Delta)**(0.5))**(1./3), 0)

        rpar = b/(3.*a)
        x1 = s + t + complex(-rpar, 0)
        x2 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) + (s-t)*(1j)*complex((3**(0.5))/2, 0)
        x3 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) - (s-t)*(1j)*complex((3**(0.5))/2, 0)

        if abs(x1.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x1': x1})
            else:
                result.append(x1)
        if abs(x2.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x2': x2})
            else:
                result.append(x2)
        if abs(x3.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x3': x3})
            else:
                result.append(x3)            

        return result
    
    else:
        result = None
        return result
               
