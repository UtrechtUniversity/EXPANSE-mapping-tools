import subprocess
from pathlib import Path
import time
import shutil
import os
import pandas as pd



def size(path):
    return f"{round(os.path.getsize(path)/1048576, 2)} MB"

def compress(tiff_path, level):
    tiff_name = tiff_path.stem
    start = time.time()
    result_path = f"{RESULT_LOCATION/tiff_name}_compressed_{level}.tif"
    print(f"Intended result path: {result_path}")
    subprocess.run([
        "gdal_translate",
        "-ot", "Float32",
        "-co", "COMPRESS=ZSTD",
        "-co", f"ZSTD_LEVEL={level}",
        "-co", "PREDICTOR=3",
        "-co", "TILED=YES",
        "-co", "BLOCKXSIZE=256",
        "-co", "BLOCKYSIZE=256",
        tiff_path,
        result_path
        # "gdal_translate",
        # "-ot", "Int16",
        # "-scale", "2.5 34 0 65535",
        # "-a_scale", "0.00048",
        # "-a_offset", "2.5",
        # "-co", "COMPRESS=ZSTD",
        # "-co", "PREDICTOR=2",
        # "gdal_translate",
        # "-ot", "Float32",
        # "-co", "COMPRESS=LERC",
        # "-co", "MAX_Z_ERROR=0.5",
        # "-co", "TILED=YES",
        # "-co", "BLOCKXSIZE=256",
        # "-co", "BLOCKYSIZE=256",
        # tiff_path,
        # result_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    subprocess_time = round(end-start, 5)
    print(f"\n{tiff_name} --- ZSTD_LEVEL={level} --- {subprocess_time}\n{size(tiff_path)} -> {size(result_path)}\n\n")
    return f"{subprocess_time}"

if __name__ == "__main__":
    RESULT_LOCATION = Path(r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD3/")

    compressions = pd.DataFrame([["Tiff"] + list(range(1, 15))])
    testing_tiffs = [Path(r"C:\Users\5298954\Documents\Projects\Exposure_Map\project_geoserver\data_dir\data\NDV_MD3\NDV_MD3_XX_XX_10_v2.tif")]

    for i, tiff in enumerate(testing_tiffs):
        shutil.copy2(tiff, f"{RESULT_LOCATION/tiff.stem}_original.tif")
        compressions.loc[i, 0] = tiff.stem
        for level in range(3, 4):
            compressions.loc[i, level] = compress(tiff, level)

    print(compressions)