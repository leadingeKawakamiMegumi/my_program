import numpy as np

#点と直線 ka*x + kb の距離
def my_kyori(xp,yp,ka,kb):
    '''
    input----------------------
    (xp,yp)
    ka:slope 
    kb:intercept 
    output--------------------
    kyori (float64)
    '''
    kyori = (ka*xp -yp + kb)/np.sqrt(ka*ka + 1)
    return kyori
