import re
import os
from settings import LOCAL_PATH, BUILT_PREFIXES, FOOD_PREFIXES, PHYSIO_CHEMICAL_PREFIXES
from pathlib import Path

def build_folder_structure():
    local_path = Path(LOCAL_PATH)
    if not local_path.exists():
        print("Check the local download path and make sure that it exists on your machine before continuing")
        return
    
    # Make folders for each theme prefix
    for prefix in BUILT_PREFIXES+FOOD_PREFIXES+PHYSIO_CHEMICAL_PREFIXES:
        theme_path = local_path / prefix
        theme_path.mkdir(parents=False, exist_ok=True) # exist_ok=True doesnt overwrite existing dir, it prevents raising FileExistsError

def is_tiff(file_path):
    return Path(file_path).suffix in ['.tif', '.tiff']

def build_new_name(file_name):
    # Get the prefix
    for prefix in BUILT_PREFIXES + FOOD_PREFIXES + PHYSIO_CHEMICAL_PREFIXES:
        if prefix in file_name:
            found_prefix = prefix
            break

    date_part = re.split(found_prefix, file_name)[1]
    
    # Rearrange the date section
    if date_part:
        date_part = re.split("_v\d+", date_part)[0] # Get rid of anything that looks like v_ followed by a digit
    else:
        if found_prefix in FOOD_PREFIXES:
            rearranged_time_part = 20200101
            new_name = f"{found_prefix}_{rearranged_time_part}"
            return new_name           

    year = date_part[-2:]

    if int(year) < 0:
        year = f"19{year}"
    else:
        year = f"20{year}"

    month = date_part[-5:-3]
    day = date_part[-8:-6]

    # Recreate date part and replace any missing days or months represented by XX with January 01
    rearranged_time_part = year+month+day
    rearranged_time_part = rearranged_time_part.replace("XX", "01") 

    new_name = f"{found_prefix}_{rearranged_time_part}"
    return new_name

def compress_and_rename(file_path):
    original_tiff_name = Path(file_path).stem
    new_tiff_name = build_new_name(original_tiff_name)

    # HERE THE ACTUAL COMPRESSION HAPPENS

    if not "XX" in original_tiff_name: # So it's already been compressed:
        return
    parent = Path(file_path).parent
    os.rename(file_path, f"{parent/new_tiff_name}.tif")
    print(f"file_path -> {parent/new_tiff_name}")

if __name__ == "__main__":
    # build_folder_structure()

    # Here, the crawler downloads data. Next is how it's transformed after.

    for path, subdirs, files in os.walk(LOCAL_PATH):
        for name in files:
            file_path = os.path.join(path, name)
            if is_tiff(file_path):
                compress_and_rename(file_path)

    # test = "NO2B100_AAV_XX_XX_01_v2"
    # result = build_new_name(test)
    # print(result)