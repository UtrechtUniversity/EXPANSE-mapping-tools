import subprocess
import os
import time

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

def compress_raster(src_path, temp_compressed_path, level):
    """
    Compress integer raster (UInt8 or Int32) for visualization.
    Preserves data type and NoData.
    """

    print(f"Compressing {src_path}")

    subprocess.run([
        "gdal_translate",
        "-co", "COMPRESS=ZSTD",
        "-co", f"ZSTD_LEVEL={level}",
        "-co", "PREDICTOR=2",
        "-co", "TILED=YES",
        "-co", "BLOCKXSIZE=256",
        "-co", "BLOCKYSIZE=256",
        src_path,
        temp_compressed_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(src_path)
    os.rename(temp_compressed_path, src_path)
    time.sleep(1)



if __name__ == "__main__":
    path = r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\LAN_B10\merged\LAN_B10_20200101.tif"
    target_path = r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\LAN_B10\merged\LAN_B10_20200101_compressed.tif"
    compress_raster(path, target_path, level=9)