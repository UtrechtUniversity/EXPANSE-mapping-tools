from ibridges.interactive import interactive_auth
from ibridges.path import IrodsPath
from ibridges import download, MetaData
from pathlib import Path
import os
from itertools import product
from settings import COUNTRIES, CATEGORIES, FOOD_PREFIXES, PHYSIO_CHEMICAL_PREFIXES, BUILT_PREFIXES, LOCAL_PATH

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
        for object in folder_path.collection.data_objects:

            tiff_name = Path(object.path).stem
            print(tiff_name)
            
            found_prefix = ""
            for prefix in prefix_list:
                if tiff_name.startswith(prefix):
                    found_prefix = prefix
                    break
            
            if not found_prefix:
                continue

            if not "XX" in tiff_name: # This is so we skip the daily temperature files
                print(f"Oh no a temperature file: {tiff_name}")
                continue

            tiff_path = folder_path.joinpath(object.name)
            save_path = Path(LOCAL_PATH).joinpath(found_prefix, country)

            # if savepath does not exist, create it
            if not save_path.exists():
                os.makedirs(save_path)

            print(f"Downloading {tiff_name}")
            ops = download(tiff_path, save_path, overwrite=True)

    def crawl(self, countries=("Netherlands", )):        
        for country, category in product(countries, CATEGORIES):
            if category == "Food":
                prefix_list = FOOD_PREFIXES
            elif category == "Built":
                prefix_list = BUILT_PREFIXES
            elif category == "Physico-chemical":
                prefix_list = PHYSIO_CHEMICAL_PREFIXES

            print(country, category)
            folder_path = self.expanse_path/country/category
            if not folder_path.exists():
                continue
            if category == "Physico-chemical":
                for subfolder in folder_path.collection.subcollections:
                    subfolder_name = folder_path/subfolder.name
                    # print(subfolder_name)
                    self.download_everything_in_collection(subfolder_name, prefix_list, country)
            else:
                self.download_everything_in_collection(folder_path, prefix_list, country)

if __name__ == "__main__":
    yoda_crawler = YodaCrawler()

    yoda_crawler.connect()
    yoda_crawler.crawl()
    yoda_crawler.disconnect()

# print(expanse_path.collection.subcollections)
# ops = download(expanse_path.joinpath('BSI_DIS_XX_XX_13_v2.tif'), LOCAL_PATH, overwrite=True)
# ops.print_summary()



        # print(type(self.research_path))
        # if download:
        #     pass
        # else:
        #     print(self.research_path.collection.subcollections)

        # Set up iBridges session
        # session = interactive_auth()
        # home_path = IrodsPath(session, session.home)

