import subprocess
import os
import time
from osgeo import gdal



# def compress_raster(src_path, temp_compressed_path, level):
#     print(f"Compressing {src_path}")

#     subprocess.run([
#         "gdal_translate",
#         "-ot", "Float32",
#         "-co", "COMPRESS=ZSTD",
#         "-co", f"ZSTD_LEVEL={level}",
#         "-co", "PREDICTOR=3",
#         "-co", "TILED=YES",
#         "-co", "BLOCKXSIZE=256",
#         "-co", "BLOCKYSIZE=256",
#         src_path,
#         temp_compressed_path
#     ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#     os.remove(src_path)
#     os.rename(temp_compressed_path, src_path)
#     time.sleep(1)

from osgeo import gdal

def compress_raster(src_path, temp_compressed_path, level):
    start_time = time.time()
    print(f"Compressing {src_path}")
    src = gdal.Open(src_path)

    options = gdal.TranslateOptions(
        outputType=gdal.GDT_Float32,
        creationOptions=[
            "COMPRESS=ZSTD",
            f"ZSTD_LEVEL={level}",
            "PREDICTOR=3",
            "TILED=YES",
            "BLOCKXSIZE=256",
            "BLOCKYSIZE=256",
        ]
    )

    gdal.Translate(temp_compressed_path, src, options=options)
    src = None

    os.remove(src_path)
    os.rename(temp_compressed_path, src_path)
    print(f"Time to compress: {time.time() - start_time}")



if __name__ == "__main__":
    src_path = r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\OZOB25_AAV\Finland\OZOB25_AAV_20000101.tif"
    temp_compressed_path = r"D:\Projects\Exposure_Map\project_geoserver\data_dir\data\OZOB25_AAV\Finland\OZOB25_AAV_20000101_temp_compressed.tif"
    level = 9

    compress_raster(src_path, temp_compressed_path, level)
    
