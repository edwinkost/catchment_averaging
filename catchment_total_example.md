
1. Install the necessary software by following the instruction on https://github.com/UU-Hydro/PCR-GLOBWB_model#how-to-install

2. Obtain the cell_area and ldd (river network) files from the following location. In this example, we will use 0.5 deg files of PCR-GLOBWB.

cell_area: https://opendap.4tu.nl/thredds/fileServer/data2/pcrglobwb/version_2019_11_beta/pcrglobwb2_input/global_30min/routing/ldd_and_cell_area/cellarea30min.nc

ldd: https://opendap.4tu.nl/thredds/fileServer/data2/pcrglobwb/version_2019_11_beta/pcrglobwb2_input/global_30min/routing/ldd_and_cell_area/lddsound_30min.nc

wget https://opendap.4tu.nl/thredds/fileServer/data2/pcrglobwb/version_2019_11_beta/pcrglobwb2_input/global_30min/routing/ldd_and_cell_area/cellarea30min.nc
wget https://opendap.4tu.nl/thredds/fileServer/data2/pcrglobwb/version_2019_11_beta/pcrglobwb2_input/global_30min/routing/ldd_and_cell_area/lddsound_30min.nc

3. Crop the ldd and cell_area files to the bounding box of your study area

# convert the files to tif so that you can use gdal
gdal_translate cellarea30min.nc  cellarea30min.tif
gdal_translate lddsound_30min.nc lddsound_30min.tif

# crop it to your bounding box extent, for example for the Rhine-Meuse basin extent
gdalwarp -te 3.5 46. 12. 52.5 cellarea30min.tif  cellarea30min_rhine_meuse.tif
gdalwarp -te 3.5 46. 12. 52.5 lddsound_30min.tif lddsound_30min_rhine_meuse.tif

# convert it back to PCRaster map
gdal_translate -of PCRaster cellarea30min_rhine_meuse.tif  cellarea30min_rhine_meuse.map
gdal_translate -of PCRaster lddsound_30min_rhine_meuse.tif lddsound_30min_rhine_meuse.map

# - remove xml files (as we do not need them)
rm '*.xml'

3. Convert the file to a drainage direction type

# convert ldd file to a drainage direction type
pcrcalc lddsound_30min_rhine_meuse.ldd = "lddrepair(ldd(lddsound_30min_rhine_meuse.map))"

# - visualize it
aguila lddsound_30min_rhine_meuse.ldd

4. Calculate the catcment area for every pixel, see

# calculate catchment area (m2), note that the unit in cellarea30min.nc is m
pcrcalc catchmant_area.map = "catchmenttotal(cellarea30min_rhine_meuse.map, lddsound_30min_rhine_meuse.ldd)"

# - visualize it
aguila catchmant_area.map