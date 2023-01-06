#!"C:\Users\wlynes\Documents\Python\streng\Scripts\python"
"""
Trying to make a cool code of the Steel Manual dude.

© William Lynes, P.E.
2022-12-15

"""

# Import dependencies
import math




# B4 MEMBER PROPERTIES

# B4.1 CLASSIFICATION OF SECTIONS FOR LOCAL BUCKLING

def TableB41a(chez, b, t, E=29000, Fy=50):
    lam = b/t
    efy = math.sqrt(E/Fy)
    
    if chez == 1:
        lamr = 0.56 * efy
    elif chez == 2:
        lamr = 0.64 * efy * math.sqrt(0.35)
    elif chez == 3:
        lamr = 0.45 * efy
    elif chez == 4:
        lamr = 0.75 * efy
    elif chez == 5:
        lamr = 1.49 * efy
    elif chez == 6:
        lamr = 1.40 * efy
    elif chez == 7:
        lamr = 1.40 * efy
    elif chez == 8:
        lamr = 1.49 * efy
    elif chez == 9:
        lamr = 0.11 * efy**2
    
    if lam <= lamr:
        cat = "Nonslender"
    else:
        cat = "Slender"

    return lam, lamr, cat

def TableB41b(chez, b, t, E=29000, Fy=50, hc=1, hp=1, Mp=1, My=1):
    lam = b/t
    efy = math.sqrt(E/Fy)
    
    if chez == 10:
        lamp = 0.38 * efy
        lamr = 1.00 * efy
    elif chez == 11:
        lamp == 0.38 * efy
        lamr = 0.95 * efy * math.sqrt(0.35)
    elif chez == 12:
        lamp = 0.54 * efy
        lamr = 0.91 * efy
    elif chez == 13:
        lamp = 0.38 * efy
        lamr = 1.00 * efy
    elif chez == 14:
        lamp = 0.84 * efy
        lamr = 1.52 * efy
    elif chez == 15:
        lamp = 3.76 * efy
        lamr = 5.70 * efy
    elif chez == 16:
        lamp = ((hc/hp)*efy) / (0.54 *  (Mp / My) - 0.09)**2
        lamr = 5.72 * efy
    elif chez == 17:
        lamp = 1.12 * efy
        lamr = 1.40 * efy
    elif chez == 18:
        lamp = 1.12 * efy
        lamr = 1.40 * efy
    elif chez == 19:
        lamp = 2.42 * efy
        lamr = 5.70 * efy
    elif chez == 20:
        lamp = 0.07 * efy**2
        lamr = 0.31 * efy**2
    else:
        lamp = 1.12 * efy
        lamr = 1.49 * efy
    if lam <= lamp:
        cat = "Compact"
    elif lam <= lamr:
        cat = "Noncompact"
    else:
        cat = "Slender"

    return lam, lamr, cat

