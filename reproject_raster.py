from osgeo import gdal
import numpy as np
import os
import time

def reproject_raster(src_path, temp_reprojected_path, update_nodata=True, nodata_value=np.nan):
    """ Reproject raster to EPSG:3857 using gdalwarp for faster geoserver requests."""
    print(f"Reprojecting {src_path}")
    if update_nodata:
        warpoptions = gdal.WarpOptions(dstSRS="EPSG:3857", dstNodata=nodata_value, resampleAlg='near', format='GTiff', xRes=100, yRes=100)
    else:
        warpoptions = gdal.WarpOptions(dstSRS="EPSG:3857", resampleAlg='near', format='GTiff')
    
    gdal.Warp(temp_reprojected_path, src_path, options=warpoptions)
    
    # Delete the original file and rename the reprojected file to the original file name
    # os.remove(src_path)
    # os.rename(temp_reprojected_path, src_path)
    # sleep
    time.sleep(1)

if __name__ == "__main__":
    path = r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD1\France\NDV_MD1_XX_XX_05_v2.tif"
    target_path = r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD1\France\NDV_MD1_XX_XX_05_v2_reprojected_near.tif"
    reproject_raster(path, target_path)

