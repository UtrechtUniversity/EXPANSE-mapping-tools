import re
import os
from settings import LOCAL_PATH, BUILT_PREFIXES, FOOD_PREFIXES, PHYSICAL_CHEMICAL_PREFIXES
from reproject_raster import reproject_raster
from compress_raster import compress_raster
from divide_raster import divide_raster
from pathlib import Path
import shutil
import time
import subprocess
# import rasterio
import numpy as np
from osgeo import gdal

def is_tiff(file_path):
    return Path(file_path).suffix in ['.tif', '.tiff']

def build_new_name(file_name):
    # Get the prefix
    for prefix in BUILT_PREFIXES + FOOD_PREFIXES + PHYSICAL_CHEMICAL_PREFIXES:
        if prefix in file_name:
            found_prefix = prefix
            break
    
    date_part = re.split(found_prefix, file_name)[1]
    # Rearrange the date section
    if date_part:
        date_part = re.split("_v\d+", date_part)[0] # Get rid of anything that looks like v_ followed by a digit
    else:
        if found_prefix in FOOD_PREFIXES: #Foods are available only for one year
            rearranged_time_part = 20200101
            new_name = f"{found_prefix}_{rearranged_time_part}"
            return new_name           

    year = date_part[-2:]

    if int(year) < 0:
        year = f"19{year}"
    else:
        year = f"20{year}"

    month = date_part[-5:-3]
    day = date_part[-8:-6]

    # Recreate date part and replace any missing days or months represented by XX with January 01
    rearranged_time_part = year+month+day
    rearranged_time_part = rearranged_time_part.replace("XX", "01") 

    new_name = f"{found_prefix}_{rearranged_time_part}"
    return new_name

def rename_tiff(src_path):
    original_tiff_name = Path(src_path).stem
    new_tiff_name = build_new_name(original_tiff_name)

    if not "XX" in original_tiff_name: # It's already been renamed
        print(f"Already renamed: {src_path}")
        return False
    
    parent = Path(src_path).parent
    new_path = parent / f"{new_tiff_name}.tif"
    os.rename(src_path, new_path)

    return new_path


def preprocess_tiff(file_path):
    renamed = rename_tiff(file_path)
    if not renamed: # If the file was already renamed, it's been preprocessed
        print(f"Skipping {file_path}, already preprocessed.")
        return
    else:
        file_path = renamed

    temp_reprojected_path = f"{os.path.splitext(file_path)[0]}_temp_reprojected.tiff"
    reproject_raster(file_path, temp_reprojected_path, update_nodata=False, nodata_value=np.nan)

    # if "NDV" in str(file_path) or "MVI" in str(file_path):
    #     temp_divided_path = f"{os.path.splitext(file_path)[0]}_temp_divided.tiff"
    #     divide_raster(file_path, temp_divided_path, divisor=10000)


    # # temp_compressed_path = f"{os.path.splitext(file_path)[0]}_temp_compressed.tiff"
    compress_raster(file_path, temp_compressed_path, level=9)


def main():
    # for path, subdirs, files in os.walk(LOCAL_PATH):
    for path, subdirs, files in os.walk(r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD1\Albania\testing"):
        for name in files:
            file_path = os.path.join(path, name)
            
            if is_tiff(file_path):
                preprocess_tiff(file_path)

if __name__ == "__main__":
    main()

