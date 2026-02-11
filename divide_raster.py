import osgeo
import rasterio
import os
import numpy as np
import time

# def divide_raster(src_path, temp_divided_path, divisor=10000):
#     print(f"Dividing {src_path} by {divisor}")
#     with rasterio.open(src_path) as src:
#         array = src.read(1)
#         profile = src.profile.copy()
#         nodata  = src.nodata

#         print("Original min:", np.nanmin(array))
#         print("Original max:", np.nanmax(array))
#         print("Nodata:", src.nodata)

#     if np.nanmax(array) <= 1.0:
#         print("Already divided, skipping.")
#         return

#     if nodata is not None:
#         mask = ~np.isclose(array, nodata)
#         divided_array = np.full_like(array, nodata, dtype=np.float32)
#         divided_array[mask] = np.round(array[mask] / divisor, 2)
#     else:
#         divided_array = np.round(array / divisor, 2)

#     # Create a temporary file to save the divided raster
#     with rasterio.open(temp_divided_path, 'w', **profile) as dst:
#         dst.write(divided_array, 1)

    # os.remove(src_path)
    # os.rename(temp_divided_path, src_path)
    # time.sleep(1)

    # if nodata is not None:
    #     print(np.isclose(array, nodata))
        # array[np.isclose(array, old_nodata)] = np.nan

    # divided_array = np.round(array / divisor, 2)

    # print("New min:", np.nanmin(divided_array))
    # print("New max:", np.nanmax(divided_array))


def divide_raster(src_path, temp_divided_path, divisor=10000):
    start_time = time.time()
    print(f"Dividing {src_path} by {divisor}")

    with rasterio.open(src_path) as src:
        data = src.read(1, masked=True)   # MaskedArray
        profile = src.profile.copy()
        nodata = src.nodata

    # Compute stats only on valid data
    # print("Original min:", data.min())
    # print("Original max:", data.max())
    # print("Nodata:", nodata)

    if data.max() <= 1.0:
        print("Already divided, skipping.")
        return

    # Perform division only on valid cells
    divided = np.round(data / divisor, 2)

    # Ensure output dtype is float32
    profile.update(dtype="float32", nodata=nodata)

    with rasterio.open(temp_divided_path, "w", **profile) as dst:
        dst.write(divided.filled(nodata).astype(np.float32), 1)

    os.remove(src_path)
    os.rename(temp_divided_path, src_path)
    print(f"Time to divide: {time.time() - start_time}")

if __name__ == "__main__":
    divide_raster(r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\new_stuff\NO2B25_AAV\France\NO2B25_AAV_XX_XX_00_v2.tif",
                  r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\new_stuff\NO2B25_AAV\France\NO2B25_AAV_XX_XX_00_v2_divided.tif", divisor=1)