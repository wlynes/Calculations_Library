from pathlib import Path

# External library Imports
from MathcadPy import Mathcad

mathcad_app = Mathcad()  # creates an instance of the Mathcad class - this object represents the Mathcad application
mathcad_worksheet = mathcad_app.open(r"C:/Users/wlynes/OneDrive -  high.net/Calculation Library/Steel - AISC 15th Edition/F2Flexure.mcdx")
mathcad_worksheet.set_real_input("willie", 28.,"m",preserve_worksheet_units=False)