import os
import tarfile
import arcpy
import os, arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
main_time = time.time()
start_time = time.time()
imgNewDir = arcpy.GetParameterAsText(0)
imgNewDir1 = arcpy.GetParameterAsText(1)
imgMain = arcpy.GetParameterAsText(5)
Es_Constant = arcpy.GetParameter(3)
EV_Constant = arcpy.GetParameter(4)
imgIndexOut = os.path.join(imgNewDir, imgMain)
arcpy.env.workspace = imgIndexOut
RED = os.path.join(imgNewDir, arcpy.GetParameterAsText(0))
NIR = os.path.join(imgNewDir1, arcpy.GetParameterAsText(1))
arcpy.SetRasterProperties_management(NIR, nodata="1 0")
arcpy.SetRasterProperties_management(RED, nodata="1 0")
Num = arcpy.sa.Float(Raster(NIR)-Raster(RED))
Denom = arcpy.sa.Float(Raster(NIR)+Raster(RED))
ras1 = arcpy.sa.Divide(Num, Denom)
ras1.save("NDVI.img")
inRastNDVI = "NDVI.img"
arcpy.AddMessage("Generating the NDVI for this scene took %s seconds...." % (time.time() - start_time))
inMaskDir = arcpy.GetParameterAsText(2)
inMask = arcpy.GetParameterAsText(2)
inMaskData = os.path.join(inMaskDir,inMask)
outExtractByMask = ExtractByMask(inRastNDVI, inMaskData)
outExtractByMask.save("NDVICUT.img")
NDVImin = arcpy.GetRasterProperties_management(inRastNDVI, "MINIMUM")
NDVImin = float(NDVImin.getOutput(0))
arcpy.AddMessage(NDVImin)
NDVImax = arcpy.GetRasterProperties_management(inRastNDVI, "MAXIMUM")
NDVImax = float(NDVImax.getOutput(0))
arcpy.AddMessage(NDVImax)
start_time = time.time()
print("Creating the LST image.....")
print("Calculating Proportion of Vegetation.......")
inRastN = "NDVICUT.img"
NDVImin = arcpy.GetRasterProperties_management(inRastN, "MINIMUM")
NDVImin = float(NDVImin.getOutput(0))
print(NDVImin)
NDVImax = arcpy.GetRasterProperties_management(inRastN, "MAXIMUM")
NDVImax = float(NDVImax.getOutput(0))
print(NDVImax)
PvNum = Raster(inRastN) - NDVImin
PvDenom = NDVImax - NDVImin
PvDiv = arcpy.sa.Divide(PvNum, PvDenom)
PvSq = Square(PvDiv)
# Pv = Square((inRastN - NDVImin) / (NDVImax - NDVImin))
PvSq.save("Prop_Veg.img")
print("Calculating Emissivity......")
Emissivity = Con(Raster("NDVICUT.img")< 0.1,Es_Constant,Con((Raster("NDVICUT.img") >= 0.1) & (Raster("NDVICUT.img") <=  0.72),0.985*Raster("Prop_Veg.img")+0.96*(1-Raster("Prop_Veg.img")),Con(Raster("NDVICUT.img")> 0.72,EV_Constant)))
Emissivity.save("LSE.img")
# ======================================= Land Surface Temperature Final Calculation ==============================================================
