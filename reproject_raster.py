from osgeo import gdal
import numpy as np
import os
import time

def reproject_raster(src_path, temp_reprojected_path, update_nodata=False, nodata_value=np.nan):
    start_time = time.time()
    """ Reproject raster to EPSG:3857 using gdalwarp for faster geoserver requests."""
    print(f"Reprojecting {src_path}")
    if update_nodata:
        warpoptions = gdal.WarpOptions(dstSRS="EPSG:3857", dstNodata=nodata_value, resampleAlg='cubic', format='GTiff', xRes=25, yRes=25, creationOptions=["COMPRESS=ZSTD", "ZSTD_LEVEL=9"])
    else:
        warpoptions = gdal.WarpOptions(dstSRS="EPSG:3857", resampleAlg='cubic', format='GTiff', xRes=25, yRes=25, creationOptions=["COMPRESS=ZSTD", "ZSTD_LEVEL=9"])
    
    gdal.Warp(temp_reprojected_path, src_path, options=warpoptions)
    
    # Delete the original file and rename the reprojected file to the original file name
    os.remove(src_path)
    os.rename(temp_reprojected_path, src_path)
    print(f"Time to reproject: {time.time() - start_time}")
    # sleep
    # time.sleep(1)

if __name__ == "__main__":
    path = r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\NO2B25_AAV\Romania\NO2B25_AAV_XX_XX_01_v2.tif"
    target_path = r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\NO2B25_AAV\Romania\NO2B25_AAV_XX_XX_01_v2_reprojected_yesupdatenocompress.tif"
    reproject_raster(path, target_path, update_nodata=True)

