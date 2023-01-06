"""
Companion script to RC Interaction Diagram Mathcad Worksheet
Makes really heavy use of Matt Woodhead's 'MathcadPy' library
https://github.com/MattWoodhead/MathcadPy

© William Lynes, P.E.
2022-12-14
High Structural Erectors, LLC

"""

# import libraries
from MathcadPy import Mathcad
from pathlib import Path
import numpy as np
import math
from sectionproperties.pre.library.concrete_sections import concrete_column_section
import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section

# instantiate mathcad class
mcd = Mathcad(visible=False)

# open the mathcad worksheet
ws = mcd.open(Path.cwd() / "RC_Interaction.mcdx")
ws.activate()

""" BEGIN USER INPUT
===================== """
fc = 3.5                             # Compressive strength concrete, ksi
fy = 53.7                            # Yield strength steel, ksi
bcol = 34                             # column dimension in the X direction, in
hcol = 34                            # column dimension in the X direction, in
dbar = 1.5                           # bar diameter, in
cc = 2.5                             # distance from edge to center of rebar, in

rebar_layout = np.array([[1, 1],
                         [1, 1]])

""" END USER INPUT
===================== """

# Constants
ec = 0.003 # Maximum compressive strain of concrete
E = 29000 # ksi, Young's modulus of steel
ey =fy / E # steel yield strain

# Functions

def steel_props(y=hcol):
    """
    INPUT:
        x = dimension in the STRONG AXIS direction
        y = dimension in the WEAK AXIS direction
    
    
    """
    Ast = math.pi / 4 * dbar**2
    Ast_layout = Ast * rebar_layout
    nby, nbx = np.shape(Ast_layout)
    AstTop = np.sum(Ast_layout, axis = 1)[0]
    AstBottom = np.sum(Ast_layout, axis = 1)[-1]
    dsTop = cc
    dsBottom = y - cc
    ey = fy / E
    return Ast, Ast_layout, nby, nbx, ey, AstTop, AstBottom, dsTop, dsBottom

def conc_props(x, y):
    Ec = 57000 * math.sqrt(fc * 1000)
    if fc <= 4.:
        beta1 = 0.85
    elif fc < 8:
        beta1 = 0.85 - 0.05*(fc-4)
    else:
        beta1 = 0.65
    Ag = x * y
    return Ec, beta1, Ag

def safety_factor(e):
    ey = fy / E
    if abs(e) <= ey:
        phi, classification = 0.65, 'CC'
    elif abs(e) < ey + 0.003:
        phi, classification = 0.65+0.25*(abs(e)-ey)/(0.003), 'Tr'
    else:
        phi, classification = 0.90, 'TC'
    return 1.5/phi, classification

def stress_strain(ysBottom, ysTop, AstTop, AstBottom, c, a, x, y):
    if c > ysBottom + dbar / 2:
        Acc = x * a - (AstTop - AstBottom)
        esBottom = ec / c * (c - ysBottom)
        fsBottom = min(fy, esBottom * E)
        esTop =ec / c * (c - ysTop)
        fsTop = min(fy, esTop * E)             
    elif c > ysTop + dbar / 2:
        Acc = x * a - AstTop
        esBottom = -1 * ec / c * (ysBottom - c)
        fsBottom = max(-fy, esBottom * E)  
        esTop =ec / c * (c - ysTop)
        fsTop = min(fy, esTop * E) 
    else:
        Acc = x * a
        esBottom = -1 * ec / c * (ysBottom - c)
        fsBottom = max(-fy, esBottom * E) 
        esTop = -1 * ec / c * (ysTop - c)
        fsTop = max(-fy, esTop * E) 
    return Acc, fsBottom, fsTop, esBottom

def calc_forces(y, Acc, fsTop, AstTop, fsBottom, AstBottom, ysTop, ysBottom, a, P0):
    Cc = 0.85 * fc * Acc
    FsTop = fsTop * AstTop
    FsBottom = fsBottom * AstBottom
    P = min(0.80*P0, Cc + FsTop + FsBottom)
    M = Cc*(y/2 - a/2) + FsTop*(y/2 - ysTop) + FsBottom*(y/2 - ysBottom)
    return P, M

def section_analysis(x, y):
    geometry = sections.rectangular_section(b=x, d=y)
    geometry.create_mesh(mesh_sizes=[0.1])
    section = Section(geometry)
    section.calculate_geometric_properties()
    section.display_results(fmt='.3f')
    # section.plot_centroids()

def rc_section_plot(x, y, nbx, nby):
    geometry = concrete_column_section(x, y, cc-dbar/2, nbx, nby, dbar, math.pi/4 * dbar**2, n_circle=20)
    geometry.plot_geometry()

def input_echo(x=bcol, y=hcol):
    echo = PrettyTable()
    nfmt = '{:.3f}'
    echo.title = "Input Echo"
    echo.field_names = ["Parameter", "Value", "Unit"]
    echo.add_rows(
        [
            ["Concrete compressive strength", nfmt.format(fc), "ksi"],
            ["Yield strength of reinforcement", nfmt.format(fy), "ksi"],
            ["Column gross width in X dimension", nfmt.format(x), "in"],
            ["Column gross height in Y dimension", nfmt.format(y), "in"],
            ["Diameter of reinforcement", nfmt.format(dbar), "in"],
            ["Distance from edge to center of reinforcement", nfmt.format(cc), "in"],
            ["Rebar pattern layout", rebar_layout, ""]
        ])
    echo.align["Value"] = "r"
    echo.align["Parameter"] = "r"
    echo.align["Unit"] = "l"
    print(echo)


def main(x=bcol, y=hcol, tol=0.001):
    # Calculate the steel and concrete properties
    Ast, Ast_layout, nby, nbx, ey, AstTop, AstBottom, ysTop, ysBottom = steel_props(y)
    Ec, beta1, Ag = conc_props(x, y)

    # Initialize arrays
    Pnx = []
    Mnx = []
    Pax = []
    Max = []
    esb = []
    
    # Calculate the first values of axial and moment arrays
    P0 = 0.85 * fc * (Ag - (AstTop + AstBottom)) + fy * (AstTop + AstBottom)
    Pnx.append(0.80*P0)
    Mnx.append(0.)
    Pax.append(0.80*P0/(1.50/0.65))
    Max.append(0.)
    esb.append(0.)

   
    # Iterate through depths of c, from bottom of section to top of section beginning with pure compression
    c = y
    while c >= 0.:
        a = beta1 * c
        Acc, fsBottom, fsTop, esBottom = stress_strain(ysBottom, ysTop, AstTop, AstBottom, c, a, x, y)
        W, classification = safety_factor(esBottom)
        P, M = calc_forces(y, Acc, fsTop, AstTop, fsBottom, AstBottom, ysTop, ysBottom, a, P0)
        Pnx.append(P)
        Mnx.append(M/12)
        Pax.append(P/W)
        Max.append((M/12)/W)
        esb.append(esBottom)
        c -= y/1000

    # Analyze section
    # section_analysis(x, y)
    return Pax, Max, Pnx, Mnx, esb

"""
MAIN PROGRAM
============
"""
# Print the input values
# input_echo(bcol,hcol)

# X-X Axis
# print("\nRESULTS FOR BENDING ABOUT THE X-X AXIS\n")
Pax, Max, Pnx, Mnx, esbx = main(bcol, hcol)

# Y-Y Axis
# print("\nRESULTS FOR BENDING ABOUT THE Y-Y AXIS\n")
Pay, May, Pny, Mny, esby = main(hcol, bcol)

# Get key values
# Pay = [round(i,2) for i in Pay]
# May = [round(i,2) for i in May]
# Pax = [round(i,2) for i in Pax]
# Max = [round(i,2) for i in Max]

# pax = Pax[0]    ;   pay = Pay[0]
# pacrx = Pax[1]  ;   pacry = Pay[1]
# macrx = Max[1]  ;   macry = May[1]
# pabalx = np.interp(-ec, esbx, Pax)  ;   pabaly = np.interp(-ec, esby, Pay)
# mabalx = np.interp(-ec, esbx, Max)  ;   mabaly = np.interp(-ec, esby, May)
# patlx = np.interp(-ey - 0.003, esbx, Pax)  ;   patly = np.interp(-ey - 0.003, esby, Pay)
# matlx = np.interp(-ey - 0.003, esbx, Max)  ;   matly = np.interp(-ey - 0.003, esby, May)
# mapbx = np.interp(0, Pax, Max)  ;   mapby = np.interp(0, Pay, May)
# paptx = Pax[-1] ;   papty = Pay[-1]




"""
SEND IT TO MATHCAD!!
====================
"""

# Populate inputs
ws.set_real_input("f'c", fc, "ksi", preserve_worksheet_units=False)
ws.set_real_input("fy", fy, "ksi", preserve_worksheet_units=False)
ws.set_real_input("b", bcol, "in", preserve_worksheet_units=False)
ws.set_real_input("h", bcol, "in", preserve_worksheet_units=False)
ws.set_real_input("dB", dbar, "in", preserve_worksheet_units=False)
ws.set_real_input("ds", cc, "in", preserve_worksheet_units=False)

print(type(Pnx))

# Populate key vals
# ws.set_real_input("Pax", pax, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Pay", pay, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Pacrx", pacrx, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Pacry", pacry, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Macrx", macrx, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Macry", macry, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Pabalx", pabalx, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Pabaly", pabaly, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Mabalx", mabalx, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Mabaly", mabaly, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Patlx", patlx, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Patly", patly, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Matlx", matlx, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Matly", matly, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Max", mapbx, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("May", mapby, "kip*ft", preserve_worksheet_units=False)
# ws.set_real_input("Patx", paptx, "kip", preserve_worksheet_units=False)
# ws.set_real_input("Paty", papty, "kip", preserve_worksheet_units=False)

# mcd.close_all(save_option="Save")
# mcd.quit(save_option="Save")