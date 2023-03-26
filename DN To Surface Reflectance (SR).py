class LicenseError(Exception):
    pass


# Set desktop license used to Basic (keyword is arcview)

import os, sys, string, math, re
from posixpath import pardir
import arcpy
from arcpy import arc
from arcpy.sa import *

# Allow ArcPy to overwrite outputs
arcpy.env.overwriteOutput = True

# Get the Input Parameters
inRasPath = arcpy.GetParameterAsText(0)
Reflectance_MLF = arcpy.GetParameter(1)
Reflectance_ADF = arcpy.GetParameter(2)
SunElevation = arcpy.GetParameter(3)

# Set the default output path from parameter validation script
outRasPath = arcpy.GetParameterAsText(4)

try:
    # Define Output Format Based On Output Workspace
    output_format = ""
    if re.search(r'.mdb', outRasPath):
        # Final Raster Output - FGDB Raster
        arcpy.AddMessage("Output Format: PersonalGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.gdb', outRasPath):
        # Final Raster Output - FGDB Raster
        arcpy.AddMessage("Output Format: FileGeodatabase Raster")
        output_format = "GRID"
    elif re.search(r'.sde', outRasPath):
        # Final Raster Output - SDE Raster
        arcpy.AddMessage("Output Format: SDE Raster")
        output_format = "GRID"
    else:
        # Final Raster Output - Folder therfore GeoTIFF
        arcpy.AddMessage("Output Format: GeoTIFF file")
        output_format = "TIF"

    # Check for ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checking for ArcGIS Spatial Analyst Extension")
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        arcpy.AddMessage("Checked out \"Spatial\" Extension")
    else:
        # Raise a custom exception
        raise LicenseError

    # arcpy.env.workspace = ""
    arcpy.AddMessage("Loading Input Raster: {0}".format(inRasPath))
    inRas = Raster(inRasPath)

    arcpy.AddMessage("Calculating at sensor spectral reflectance")
    # The algorithm to calculate Top of Atmosphere Planetary Spectral Reflectance (ρλ’)
    # ρλ’ = Mρ * Qcal + Aρ
    # without correction for solar angle. (Unitless)
    outRas_NoSunAngle = Reflectance_MLF * inRas + (Reflectance_ADF)

    # Once a solar elevation angle is chosen
    # the algorith to calculate true TOA Reflectance is as follows
    # ρλ = ρλ’/ sin(θSE)
    outRas = outRas_NoSunAngle / Sin(SunElevation)

    # Determine the output format based on the output workspace
    if output_format == "TIF":
        outRasPath = outRasPath + ".tif"

    arcpy.AddMessage("Saving raster to: {0}".format(outRasPath))
    # Save raster to desired output folder or workspace
    outRas.save(outRasPath)

except LicenseError:
    arcpy.AddMessage("ArcGIS Spatial Analyst license is unavailable")
except arcpy.ExecuteError:
    arcpy.AddMessage(arcpy.GetMessages(2))
finally:
    # Check in the ArcGIS Spatial Analyst extension
    arcpy.AddMessage("Checked in \"Spatial\" Extension")
    arcpy.CheckInExtension("Spatial")