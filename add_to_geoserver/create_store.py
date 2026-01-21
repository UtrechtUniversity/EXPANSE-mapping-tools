import os
import shutil
from geoserver_settings import GEOSERVER_DATA_DIR, GEOSERVER_BASE, WORKSPACE, USERNAME, PASSWORD
import requests

def create_store(store_name, tiff_folder, template_store_path="A"):
    new_store = requests.post(
        f"{GEOSERVER_BASE}/workspaces/EXPANSE_map/coveragestores",
        auth=(f"{USERNAME}", f"{PASSWORD}"),
        headers={"Content-Type": "application/json"},
        json = {
            "coverageStore": {
                "name": f"{store_name}",
                "type": "ImageMosaic",
                "enabled": True,
                "workspace": {
                    "name": f"{WORKSPACE}"
                    },
                "url": f"file:{GEOSERVER_DATA_DIR}/data/{tiff_folder}"
                }
            }
    )
    if new_store.status_code != 201:
        print(new_store.status_code)
        print(new_store.text)

if __name__ == "__main__":
    create_store(store_name="Test_Store", tiff_folder="NO2B100_AAV")
    