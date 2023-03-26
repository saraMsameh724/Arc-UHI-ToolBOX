import os
import tarfile
import arcpy
import os, arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
main_time = time.time()
start_time = time.time()
imgNewDir2 = arcpy.GetParameterAsText(0)
imgMain = arcpy.GetParameterAsText(4)
imgIndexOut = os.path.join(imgNewDir2, imgMain)
# Get the Input Parameters
#inRasPath = arcpy.GetParameterAsText(0)
MLF_Temp = arcpy.GetParameter(1)
ADF_Temp = arcpy.GetParameter(2)

arcpy.env.workspace = imgIndexOut
imgIndexOut = os.path.join(imgNewDir2, imgMain)
inRas = os.path.join(imgNewDir2, arcpy.GetParameterAsText(0))
arcpy.SetRasterProperties_management(inRas, nodata="1 0")
# The algorithm to calculate at sensor spectral radiance (Lλ)
# Lλ = ML * Qcal + AL
    # without correction for solar angle. (Unitless)
outRas_Celu = arcpy.sa.Float((MLF_Temp * Raster(inRas) + ADF_Temp)-273.15)
outRas_Celu.save('OUT_CEL.img')
inRastoutRas_Celu = arcpy.GetParameterAsText(4)

inMaskDir = arcpy.GetParameterAsText(3)
inMask = arcpy.GetParameterAsText(3)
inMaskData = os.path.join(inMaskDir,inMask)
outExtractByMask = ExtractByMask(outRas_Celu, inMaskData)
outExtractByMask.save('OUT_CEL_cut.img')

















