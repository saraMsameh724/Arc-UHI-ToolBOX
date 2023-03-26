import os
import tarfile
import arcpy
import os, arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
main_time = time.time()
start_time = time.time()
imgNewDir2 = arcpy.GetParameterAsText(0)
imgNewDir3 = arcpy.GetParameterAsText(1)
AtSat = os.path.join(imgNewDir2, arcpy.GetParameterAsText(0))
LSE = os.path.join(imgNewDir3, arcpy.GetParameterAsText(1))
LST = Raster(AtSat) /(1 + (0.00115 * (Raster(AtSat) / 1.4380)) * Ln(Raster(LSE)))
LST.save(arcpy.GetParameterAsText(2))
inRasterLST = arcpy.GetParameterAsText(2)
imgMain2 = arcpy.GetParameterAsText(2)
imgIndexOut2 = os.path.join(imgNewDir3, imgMain2)
arcpy.env.workspace = imgIndexOut2
inMaskDir = arcpy.GetParameterAsText(3)
inMask = arcpy.GetParameterAsText(3)
inMaskData = os.path.join(inMaskDir,inMask)
outExtractByMask = ExtractByMask(inRasterLST, inMaskData)
outExtractByMask.save(arcpy.GetParameterAsText(4))
LSTmin = arcpy.GetRasterProperties_management(inRasterLST, "MINIMUM")
LSTmin= float(LSTmin.getOutput(0))
print(LSTmin)
LSTmax = arcpy.GetRasterProperties_management(inRasterLST, "MAXIMUM")
LSTmax = float(LSTmax.getOutput(0))
print(LSTmax)
LSTmean = arcpy.GetRasterProperties_management(inRasterLST, "MEAN")
LSTmean = float(LSTmean.getOutput(0))
print(LSTmean)
LSTSTD = arcpy.GetRasterProperties_management(inRasterLST, "STD")
LSTSTD = float(LSTSTD.getOutput(0))
print(LSTSTD)
print("Generating the LST for this scene took %s seconds...." % (time.time() - start_time))

UHINum = Raster(inRasterLST) - LSTmean
UHIDenom = LSTSTD
UHI = arcpy.sa.Divide(UHINum, UHIDenom)
UHI.save(arcpy.GetParameterAsText(5))
inRasterUHI = arcpy.GetParameterAsText(5)
inMaskDir = arcpy.GetParameterAsText(3)
inMask = arcpy.GetParameterAsText(3)
inMaskData = os.path.join(inMaskDir,inMask)
outExtractByMask = ExtractByMask(inRasterUHI, inMaskData)
print("Generating the LST for this scene took %s seconds...." % (time.time() - start_time))
#outExtractByMask = ExtractByMask(inRasterUHI, inMaskData)
#outGreaterThan = (Raster(inRasterLST))>((LSTmean + (0.5*LSTSTD)))
#outGreaterThan.save(arcpy.GetParameterAsText(6))
#inRasteroutGreaterThan = arcpy.GetParameterAsText(6)
#inMaskDir = arcpy.GetParameterAsText(3)
#inMask = arcpy.GetParameterAsText(3)
#inMaskData = os.path.join(inMaskDir,inMask)

inRasterLST1 =Raster(arcpy.GetParameterAsText(4)) + 273.15
LSTmin1 = arcpy.GetRasterProperties_management(inRasterLST1, "MINIMUM")
LSTmin1= float(LSTmin1.getOutput(0))
print(LSTmin1)
LSTmax1 = arcpy.GetRasterProperties_management(inRasterLST1, "MAXIMUM")
LSTmax1 = float(LSTmax1.getOutput(0))
print(LSTmax1)
LSTmean1 = arcpy.GetRasterProperties_management(inRasterLST1, "MEAN")
LSTmean1 = float(LSTmean1.getOutput(0))
print(LSTmean1)
LSTSTD1 = arcpy.GetRasterProperties_management(inRasterLST1, "STD")
LSTSTD1 = float(LSTSTD1.getOutput(0))
print(LSTSTD1)
UTFVINum = (inRasterLST1) - LSTmean1
UTFVIDenom = LSTmean1
UTFVI = arcpy.sa.Divide(UTFVINum, UTFVIDenom)
UTFVI.save(arcpy.GetParameterAsText(6))
inRasterUTFVI = arcpy.GetParameterAsText(6)
inMaskDir = arcpy.GetParameterAsText(3)
inMask = arcpy.GetParameterAsText(3)
inMaskData = os.path.join(inMaskDir,inMask)
outExtractByMask = ExtractByMask(inRasterUTFVI, inMaskData)
print("Generating the LST for this scene took %s seconds...." % (time.time() - start_time))