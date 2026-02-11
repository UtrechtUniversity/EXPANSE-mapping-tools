import re
import os

from pathlib import Path
import subprocess
# import rasterio
import numpy as np
from osgeo import gdal
from pathlib import Path

data_folder = Path("C:/Users/5298954/Documents/Projects/Exposure_Map/project_geoserver/data_dir/data/")

def find_tiffs(product_name, granuals_name):
    product_folder = data_folder / product_name

    granule_paths = []
    for path, subdirs, files in os.walk(product_folder):
        for name in files:
            file_path = os.path.join(path, name)
            if granuals_name in file_path and file_path.endswith(".tif"):
                granule_paths.append(file_path)
                
    
    return granule_paths


def combine_tiffs(product_name, granuals_names_list, nodata_value):
    for granule in granuals_names_list:
        os.makedirs(data_folder/product_name/"merged", exist_ok=True)

        granule_paths = find_tiffs(product_name, granule)
        print(granule_paths)

        
        subprocess.run([
            "python",
            r"C:\ProgramData\Anaconda\envs\gdal_env\Scripts\gdal_merge.py",
            "-o", str(data_folder / product_name / "merged" / f"{granule}.tif"),
            "-n", str(nodata_value),
            "-a_nodata", str(nodata_value)
        ] + granule_paths,
        check=True)


def main():
    combine_tiffs("BSW_DIS",  ["BSW_DIS_20130101"], nodata_value=255)


    # for path, subdirs, files in os.walk(LOCAL_PATH):
    # for path, subdirs, files in os.walk("C:/Users/5298954/Documents/Projects/Exposure_Map/project_geoserver/data_dir/data"):
    #     for name in files:
    #         file_path = os.path.join(path, name)
    #         print(file_path)
            
    #         if is_tiff(file_path):
    #             preprocess_tiff(file_path)

if __name__ == "__main__":
    main()

