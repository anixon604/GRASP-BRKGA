import math
import random

def grasp(fx,gx,maxitr,xprime):
    xprime = sys.maxsize
    for i in range(maxitr):
        # x param (psuedo) is only a reference. function can
        # remove the argument and return a value instead
        x = construct(gx,alpha)
        x = local(fx,x) # see if var name ok
        if fx(x) < fx(xprime):
            xprime = x


def constGrasp(gx,alpha):
    x = []
    C = []
    while C != []:
        solList = [gx(x) for x in C]
        smin = min(solList)
        smax = max(solList)
        RCL = [s for s in C if g(s) <= smin+alpha*(smax-smin)]
        s = random.choice(RCL)
        x.append(s)
        C.remove(s)
    return x
