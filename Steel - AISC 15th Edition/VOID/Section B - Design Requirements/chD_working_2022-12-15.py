import chB

"""
Variables:
===d1== 
    Lrlim = 300
d2: Pn, Fy, Fu, Ag, Ae, phi_ty=0.90, phi_tr=0.75, W_ty=1.67, W_tr=2.00
d3: Ae,An,U


"""

def sec_d1(L, r):
    Lr_suggested_limit = 300.
    Lr = L / r
    if Lr <= Lr_suggested_limit:
        expl = 'Slenderness ratio does not exceed' + ' ' + '{:.0f}'.format(Lr_suggested_limit)
    else:
        expl = 'Slenderness ratio exceeds' + ' ' + '{:.0f}'.format(Lr_suggested_limit)
    return Lr_suggested_limit, Lr, expl


class sec_d2:
    def __init__(self, Fy, Fu):
        self.Fy = Fy
        self.Fu = Fu
    
    


def sec_d2(Fy, Ag):
    # a) Tensile yielding in the gross section
    phi = 0.90  ;   W = 1.67
    Pn = Fy * Ag
    phiPn = phi * Pn    ;   PnW = Pn / W
    return Pn, phiPn, PnW


