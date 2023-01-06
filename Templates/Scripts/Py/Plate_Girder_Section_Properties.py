import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section
import numpy as np
from datetime import datetime

# Input the dimensions
bf_top = 18
tf_top = 1.125
hw = 74
tw = 0.375
bf_bot = 22
tf_bot = 2.

#create plate sections
bot_flange = sections.rectangular_section(bf_bot, tf_bot)
web = sections.rectangular_section(tw, hw)
web = web.shift_section(x_offset = bf_bot / 2 - tw / 2, y_offset = tf_bot)
top_flange = sections.rectangular_section(bf_top, tf_top)
top_flange = top_flange.shift_section(x_offset = bf_bot / 2 - bf_top / 2, y_offset = tf_bot + hw)

#create geometry and plot
geometry = bot_flange + web + top_flange
geometry.plot_geometry()

#create mesh
geometry.create_mesh(mesh_sizes=[0.25, 0.25, 0.25])
section = Section(geometry)


#analyze
section.calculate_geometric_properties()
section.calculate_warping_properties()
section.calculate_plastic_properties()

#centroids
section.plot_centroids()

#results
#section.display_results(fmt='.3f')
results = np.array([["Ag",section.get_area()],
                    ["Qx",section.get_q()[0]],
                    ["Qy",section.get_q()[1]],
                    ["c top",tf_bot+hw+tf_top-section.get_c()[1]],
                    ["c bottom",section.get_c()[1]],
                    ["Ix",section.get_ic()[0]],
                    ["Iy",section.get_ic()[1]],
                    ["Sx top",section.get_z()[0]],
                    ["Sx bottom",section.get_z()[1]],
                    ["Sy", section.get_z()[2]],
                    ["rx", section.get_rc()[0]],
                    ["ry", section.get_rc()[1]],
                    ["J", section.get_j()],
                    ["Cw", section.get_gamma()],
                    ["Zx", section.get_s()[0]],
                    ["Zy", section.get_s()[1]],
                    ["yp top", tf_bot+hw+tf_top-section.get_pc()[1]],
                    ["yp bottom", section.get_pc()[1]]])



print(results)


