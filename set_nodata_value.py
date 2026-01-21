from osgeo import gdal
import numpy as np

def set_nodata_value(tiff_path, nodata_value=np.nan):
    ds = gdal.Open(tiff_path,1) # The 1 means that you are opening the file to edit it)
    rb = ds.GetRasterBand(1) #assuming your raster has 1 band. 
    rb.SetNoDataValue(nodata_value)
    rb= None 
    ds = None
    print("NoData value set successfully.")