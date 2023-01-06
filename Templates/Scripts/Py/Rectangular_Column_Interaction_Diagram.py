#!"C:\Users\wlynes\Documents\Python\streng\Scripts\python"

import math
import numpy as np
import matplotlib.pyplot as plt
from sectionproperties.pre.library.concrete_sections import concrete_column_section
import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section
from prettytable import PrettyTable
import xlwings as xw

""" BEGIN USER INPUT
===================== 
fc = 3.5                             # Compressive strength concrete, ksi
fy = 53.7                            # Yield strength steel, ksi
bcol = 34                             # column dimension in the X direction, in
hcol = 34                            # column dimension in the X direction, in
dbar = 1.5                           # bar diameter, in
cc = 2.5                             # distance from edge to center of rebar, in

rebar_layout = np.array([[1, 1],
                         [1, 1]])

 END USER INPUT
===================== """

# import from Excel
sheet = xw.sheets.active
fc = sheet.range("G2").value
fy = sheet.range("G3").value
bcol = sheet.range("G4").value
hcol = sheet.range("G5").value
cc = sheet.range("G6").value
dbar = sheet.range("G7").value
nbtop = int(sheet.range("G8").value)
nbbottom = int(sheet.range("G9").value)
sbpresent = sheet.range("G10").value

# Constants
ec = 0.003 # Maximum compressive strain of concrete
E = 29000 # ksi, Young's modulus of steel
rebar_layout = np.ones([2,nbtop], dtype=int)

# Functions

def steel_props(y=hcol):
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
    
    # Calculate the first values of axial and moment arrays
    P0 = 0.85 * fc * (Ag - (AstTop + AstBottom)) + fy * (AstTop + AstBottom)
    Pnx.append(0.80*P0)
    Mnx.append(0.)
    Pax.append(0.80*P0/(1.50/0.65))
    Max.append(0.)

   
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
        c -= y/1000

    # Analyze section
    # section_analysis(x, y)
    return Pax, Max

"""
MAIN PROGRAM
============
"""
# Print the input values
#input_echo(bcol,hcol)

# X-X Axis
# print("\nRESULTS FOR BENDING ABOUT THE X-X AXIS\n")
Pax, Max = main(bcol, hcol)

# Y-Y Axis
# print("\nRESULTS FOR BENDING ABOUT THE Y-Y AXIS\n")
Pay, May = main(hcol, bcol)

# Print Interaction
fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
fig.suptitle('Interaction Diagrams')
ax1.plot(Max, Pax)
ax1.set(xlabel = 'Mnx / \u03A9 (kip-ft)', ylabel = 'Pnx / \u03A9 (kip)')
ax1.grid()
ax2.plot(May, Pay)
ax2.set(xlabel = 'Mny / \u03A9 (kip-ft)', ylabel = 'Pny / \u03A9 (kip)')
ax2.grid()
plt.show()