import osgeo
import rasterio
import os
import numpy as np
import time

def divide_raster(src_path, temp_divided_path, divisor=10000):
    print(f"Dividing {src_path} by {divisor}")
    with rasterio.open(src_path) as src:
        array = src.read(1)
        profile = src.profile.copy()
        old_nodata  = src.nodata

    print("Original min:", np.nanmin(array))
    print("Original max:", np.nanmax(array))
    print("Nodata:", src.nodata)

    # if old_nodata is not None:
    #     array[np.isclose(array, old_nodata)] = np.nan # TO assign as nodata later

    if np.nanmax(array) <= 1.0:
        print("Already divided, skipping.")
        return

    divided_array = np.round(array / divisor, 2)

    print("New min:", np.nanmin(divided_array))
    print("New max:", np.nanmax(divided_array))

    # if nodata is not None:
    #     mask = ~np.isclose(array, nodata)
    #     divided_array = np.full_like(array, nodata, dtype=np.float32)
    #     divided_array[mask] = np.round(array[mask] / divisor, 2)
    # else:
    #     divided_array = np.round(array / divisor, 2)


    # Create a temporary file to save the divided raster
    with rasterio.open(temp_divided_path, 'w', **profile) as dst:
        dst.write(divided_array, 1)

    # os.remove(src_path)
    # os.rename(temp_divided_path, src_path)
    # # time.sleep(1)

if __name__ == "__main__":
    divide_raster(r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD1\Albania\NDV_MD1_XX_XX_20_v2.tif", r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD1\Albania\NDV_MD1_XX_XX_20_v2_divided3.tif", divisor=10000)