# Dependencies
import win32com.client
import numpy as np

#Instantiate the active object
os = win32com.client.GetActiveObject("StaadPro.OpenSTAAD")

# Define the OpenSTAAD Modules
geometry = os.Geometry
prop = os.Property
support = os.Support
load = os.Load
table = os.Table
view = os.View
output = os.Output
design = os.Design

# Flag as methods
geometry._FlagAsMethod("GetGroupEntities")
geometry._FlagAsMethod("GetGroupEntityCount")
geometry._FlagAsMethod("GetGroupEntities")

col_reax_group_entities = []
ncol_reax = geometry.GetGroupEntityCount("_COL_REAX")
print(geometry)


