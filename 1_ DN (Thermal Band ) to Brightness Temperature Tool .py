import os
import tarfile
import arcpy
import os, arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
main_time = time.time()
start_time = time.time()
imgNewDir = arcpy.GetParameterAsText(0)
imgMain = arcpy.GetParameterAsText(5)
imgIndexOut = os.path.join(imgNewDir, imgMain)
ML_Const = arcpy.GetParameter(1)
AL_const = arcpy.GetParameter(2)
k1_Constant = arcpy.GetParameter(3)
k2_Constant = arcpy.GetParameter(4)
arcpy.env.workspace = imgIndexOut

start_time = time.time()
print("Creating the LST image.....")

    # Check for ArcGIS Spatial Analyst Extension
arcpy.AddMessage("Checking for ArcGIS Spatial Analyst Extension")
if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension("Spatial")
    arcpy.AddMessage("Checked out \"Spatial\" Extension")
else:
    # Raise a custom exception
    raise LicenseError

arcpy.AddMessage("Loading Input Raster: {0}".format(imgNewDir))
inRas = Raster(imgNewDir)

imgIndexOut = os.path.join(imgNewDir, imgMain)
Band10 = os.path.join(imgNewDir, arcpy.GetParameterAsText(0))
arcpy.SetRasterProperties_management(Band10, nodata="1 0")
# ========================== At Satellite Temp for each band = K2/Ln(K1/RAD - 1) - 273.15 =======================================================
Band10RAD = arcpy.sa.Float( ML_Const* Raster(Band10)+AL_const)
Band10RAD.save("RAD10.img")
Band10AtSat = arcpy.sa.Float((k2_Constant/ (Ln(k1_Constant / (Band10RAD) + 1)))- 273.15)
Band10AtSat.save("AtSat10.img")
#Band11AtSat.save("AtSat11.img")
print("Performing Cell Statistics for averaging of Band 10 and Band 11 At Satellite Temperature......")
inRast1 = Raster("AtSat10.img")
