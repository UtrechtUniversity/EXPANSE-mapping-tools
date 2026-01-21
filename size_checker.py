import os

# get the total size of a directory
def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

if __name__ == "__main__":
    directory = "C:/Users/5298954/Documents/Projects/Exposure_Map/project_geoserver/data_dir/data/NO2B25_AAV"
    size_bytes = get_directory_size(directory)
    size_gb = size_bytes / (1024 ** 3)
    print(f"Total size of directory '{directory}': {size_gb:.2f} GB")