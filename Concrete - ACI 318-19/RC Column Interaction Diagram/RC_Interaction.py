#!"C:\Users\wlynes\Documents\Python\streng\Scripts\python"
"""
Companion script to RC Interaction Diagram Excel Worksheet
Must have Python 3.7 (strongly recommended) with sectionproperties,
numpy, and xlwings (and add-in) installed.

In Excel, set Interpreter path to:  
          set PYTHONPATH to:        
          or wherever you have that shit saved.

© William Lynes, P.E.
2022-12-15
High Structural Erectors, LLC
"""

# import libraries
import numpy as np
import math
from sectionproperties.pre.library.concrete_sections import concrete_column_section
import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section
import xlwings as xw


# import from Excel
sheet = xw.sheets("RC Interaction Diagram")
fc = sheet.range("G9").value
fy = sheet.range("G10").value
bcol = sheet.range("G11").value
hcol = sheet.range("G12").value
cc = sheet.range("G13").value
dbar = sheet.range("G14").value
nbtop = int(sheet.range("G15").value)
nbbottom = int(sheet.range("G16").value)
sbpresent = sheet.range("G17").value

# Constants
ec = 0.003 # Maximum compressive strain of concrete
E = 29000 # ksi, Young's modulus of steel
ey =fy / E # steel yield strain
rebar_layout = np.ones([2,nbtop], dtype=int)

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


def calculate_values(x=bcol, y=hcol, tol=0.001):
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

def just_send_it(Pnx, Pny, Pax, Pay, Mnx, Mny, Max, May):
    shet = xw.sheets("Output")
    shet.clear_contents()
    shet.range("A1").value = "Results"
    shet.range("A2").value = Pnx
    shet.range("A3").value = Pny
    shet.range("A4").value = Pax
    shet.range("A5").value = Pay
    shet.range("A6").value = Mnx
    shet.range("A7").value = Mny
    shet.range("A8").value = Max
    shet.range("A9").value = May
    shet.range("A11").value = "Input Echo"
    shet.range("A12").value = np.array([['fc', fc],
                                         ['fy',fy],
                                         ['b',bcol],
                                         ['h',hcol],
                                         ['dB',dbar],
                                         ['ds',cc],
                                         ['εc',ec],
                                         ['εsy',fy/E]])
    
    shet.range("A21").value = "n_points"
    shet.range("B21").value = np.shape(Pnx)[0]
    
    shet.range("A24").value = "Rebar Layout"
    shet.range("A25").value = rebar_layout

    shet.range("C24").value, shet.range("D24").value = np.shape(rebar_layout)



def main(bcol=bcol, hcol=hcol):
    Pax, Max, Pnx, Mnx, esbx = calculate_values(bcol, hcol)
    Pay, May, Pny, Mny, esby = calculate_values(hcol, bcol)

    just_send_it(Pnx, Pny, Pax, Pay, Mnx, Mny, Max, May)

main()
# # Populate inputs
# ws.set_real_input("f'c", fc, "ksi", preserve_worksheet_units=False)
# ws.set_real_input("fy", fy, "ksi", preserve_worksheet_units=False)
# ws.set_real_input("b", bcol, "in", preserve_worksheet_units=False)
# ws.set_real_input("h", bcol, "in", preserve_worksheet_units=False)
# ws.set_real_input("dB", dbar, "in", preserve_worksheet_units=False)
# ws.set_real_input("ds", cc, "in", preserve_worksheet_units=False)

# print(type(Pnx))

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