from ibridges.interactive import interactive_auth
from ibridges.path import IrodsPath
from ibridges import download
from pathlib import Path
import os
from itertools import product
from settings import COUNTRIES, CATEGORIES, FOOD_PREFIXES, PHYSICAL_CHEMICAL_PREFIXES, BUILT_PREFIXES, LOCAL_PATH, INDEXER, TIMEREGEX
import shutil

class YodaCrawler(): 

    def __init__(self):
        pass

    def connect(self):
        self.session = interactive_auth()
        self.home_path = IrodsPath(self.session, self.session.home)
        self.expanse_path = self.home_path.joinpath('research-exposures/National')

    def disconnect(self):
        self.session.close()
        self.home_path = ""
        self.expanse_path = ""

    def download_everything_in_collection(self, folder_path, prefix_list, country):
        print(f"Starting download. This is my folder path: {folder_path}")
        if "temp" in str(folder_path):
            return

        # if "AirPollution" in str(folder_path):
        #     return

        for object in folder_path.collection.data_objects:
            tiff_name = Path(object.path).stem
            # print(f"This is the tiff name: {tiff_name}")

            found_prefix = ""
            # print(f"here is te prefix list: {prefix_list}")
            for prefix in prefix_list:
                if tiff_name.startswith(prefix):
                    found_prefix = prefix
            
            if found_prefix == "":
                # print(f"Not this one!: found_prefix{found_prefix}, prefix: {prefix}")
                continue

            if not "XX" in tiff_name: # This is so we skip the daily temperature files
                print(f"Oh no a daily temperature file: {tiff_name}")
                continue

            # if not "_21_" in tiff_name and not "_22_" in tiff_name and not "_23_" in tiff_name: # Temporary, just to download 2015
            #     continue
            if "_00_" in tiff_name: # Temporary, just to download Jan and Feb of 2020
                continue


            tiff_path = folder_path.joinpath(object.name)
            save_path = Path(LOCAL_PATH).joinpath(found_prefix, country)

            print(f"Downloading {tiff_path} to {save_path}")
            # # if savepath does not exist, create it
            if not save_path.exists():
                os.makedirs(save_path)


            ops = download(tiff_path, save_path, overwrite=True)

    def crawl(self, countries):        
        for country, category in product(countries, CATEGORIES):
            if category == "Food":
                prefix_list = FOOD_PREFIXES
            elif category == "Built":
                prefix_list = BUILT_PREFIXES
            elif category == "Physico-chemical":
                prefix_list = PHYSICAL_CHEMICAL_PREFIXES

            print(country, category)
            folder_path = self.expanse_path/country/category
            if not folder_path.exists():
                continue
            if category == "Physico-chemical":
                for subfolder in folder_path.collection.subcollections:
                    subfolder_name = folder_path/subfolder.name
                    print(subfolder_name)
                    self.download_everything_in_collection(subfolder_name, prefix_list, country)
            else:
                # pass # Temporary, only downloading physico-chemical for now
                self.download_everything_in_collection(folder_path, prefix_list, country)


def build_folder_structure():
    local_path = Path(LOCAL_PATH)
    if not local_path.exists():
        print("Check the local download path and make sure that it exists on your machine before continuing")
        return
    
    # Make folders for each theme prefix
    for prefix in BUILT_PREFIXES + PHYSICAL_CHEMICAL_PREFIXES:
        theme_path = local_path / prefix
        theme_path.mkdir(parents=False, exist_ok=True) # exist_ok=True doesnt overwrite existing dir, it prevents raising FileExistsError
        shutil.copy2(INDEXER, theme_path / "indexer.properties")
        shutil.copy2(TIMEREGEX, theme_path / "timeregex.properties")


if __name__ == "__main__":
    # build_folder_structure()

    yoda_crawler = YodaCrawler()
    yoda_crawler.connect()
    yoda_crawler.crawl(countries=COUNTRIES["EUROPE"][7:])
    # yoda_crawler.crawl(countries=COUNTRIES["EUROPE"][-7:])
    yoda_crawler.disconnect()