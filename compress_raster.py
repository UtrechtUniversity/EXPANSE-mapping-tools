import subprocess
import os
import time

def compress_raster(src_path, temp_compressed_path, level):
    print(f"Compressing {src_path}")

    subprocess.run([
        "gdal_translate",
        "-ot", "Float32",
        "-co", "COMPRESS=ZSTD",
        "-co", f"ZSTD_LEVEL={level}",
        "-co", "PREDICTOR=3",
        "-co", "TILED=YES",
        "-co", "BLOCKXSIZE=256",
        "-co", "BLOCKYSIZE=256",
        src_path,
        temp_compressed_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(src_path)
    os.rename(temp_compressed_path, src_path)
    time.sleep(1)


    