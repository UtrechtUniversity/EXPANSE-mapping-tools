import subprocess
from pathlib import Path
import time
import shutil
import os
import pandas as pd


RESULT_LOCATION = Path("C:/Users/5298954/Documents/Projects/Exposure_Map/test_data/compression_test")

def size(path):
    return f"{round(os.path.getsize(path)/1048576, 2)} MB"

def compress(tiff_path, level):
    tiff_name = tiff_path.stem
    start = time.time()
    result_path = f"{RESULT_LOCATION/tiff_name}_compressed_{level}.tif"
    subprocess.run([
        "gdal_translate",
        "-co", "COMPRESS=ZSTD",
        "-co", f"ZSTD_LEVEL={level}",
        tiff_path,
        result_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    subprocess_time = round(end-start, 5)
    print(f"\n{tiff_name} --- ZSTD_LEVEL={level} --- {subprocess_time}\n{size(tiff_path)} -> {size(result_path)}\n\n")
    return f"{subprocess_time}"

if __name__ == "__main__":
    compressions = pd.DataFrame([["Tiff"] + list(range(1, 20))])

    testing_tiffs = [Path("C:/Users/5298954/Documents/Projects/Exposure_Map/test_data/demo/BSS_DIS/Netherlands/BSS_DIS_20130101.tif"),
                     Path(r"C:\Users\5298954\Documents\Projects\Exposure_Map\test_data\demo\BSI_DIS\Netherlands\BSI_DIS_20130101.tif"),
                     Path(r"C:\Users\5298954\Documents\Projects\Exposure_Map\test_data\demo\FastF_800m\Netherlands\FastF_800m_20200101.tif"),
                     Path(r"C:\Users\5298954\Documents\Projects\Exposure_Map\test_data\demo\NO2B100_MAV\belgium\NO2B100_MAV_20000101.tif")]

    for i, tiff in enumerate(testing_tiffs):
        # print(i, tiff)
        shutil.copy2(tiff, f"{RESULT_LOCATION/tiff.stem}_original.tif")
        compressions.loc[i, 0] = tiff.stem
        for level in range(1, 20):
            compressions.loc[i, level] = compress(tiff, level)

    print(compressions)