#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pcraster as pcr

# set your working directory and go there
work_dir = "/scratch/depfg/sutan101/catchment_average_example/"
os.chdir(work_dir)

# cell_area and ldd files
cell_area_file = "/scratch/depfg/sutan101/catchment_average_example/cellarea30min_rhine_meuse.map"
ldd_file       = "/scratch/depfg/sutan101/catchment_average_example/lddsound_30min_rhine_meuse.ldd"

# calculate catchment area
# - set clone, the bounding box of your study area - here, we use ldd 
clone_file     = ldd_file
pcr.setclone(clone_file)
# - read cell_area and ldd files
cell_area = pcr.readmap(cell_area_file)
ldd       = pcr.readmap(ldd_file)
# - calculate catchment area
catchment_area = pcr.catchmenttotal(cell_area, ldd)
# - save catchment_area to a file - note the file output will be under the work_dir
catchment_area_file = "catchment_area.map"
pcr.report(catchment_area, catchment_area_file)

# input file - note that this is a single time step file
input_file     = "/scratch/depfg/sutan101/catchment_average_example/GHRM5C_1978-2021_timestep_1.nc"

# crop input file to our bounding box extent
# - gdalwarp -te xmin ymin xmax ymax -tr cellsize cellsize input output_file.tif
cmd = "gdalwarp -te 3.5 46. 12. 52.5 -tr 0.5 0.5 " + input_file + " " + input_file + ".tif"
print(cmd)
os.system(cmd)
# - convert to pcraster
cmd = "gdal_translate -of PCRaster " + input_file + ".tif " + input_file + ".map"
print(cmd)
os.system(cmd)
# - remove xml file
cmd = "rm *.xml"
print(cmd)
os.system(cmd)
# - make sure that the file has the same map attributes as the ldd file
cmd = "mapattr -c " + ldd_file + " " + input_file + ".map"
# - read the input file
file_to_be_read = input_file + ".map"
cell_value = pcr.readmap(file_to_be_read)

# calculate upstream/catchment average values
upstream_average_value = pcr.catchmenttotal(cell_value * cell_area, ldd) / catchment_area
pcr.report(upstream_average_value, "upstream_average_value.map")
