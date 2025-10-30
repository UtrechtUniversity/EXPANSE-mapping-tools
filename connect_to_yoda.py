from ibridges.interactive import interactive_auth
from ibridges.path import IrodsPath
from ibridges import download
from pathlib import Path
import os
from settings import LOCAL_PATH

# Set up iBridges session
session = interactive_auth()
home_path = IrodsPath(session, session.home)
research_path = home_path.joinpath('Research')
expanse_path = home_path.joinpath('research-exposures/National/Albania/Built')

# print(expanse_path.collection.subcollections)
ops = download(expanse_path.joinpath('BSI_DIS_XX_XX_13_v2.tif'), LOCAL_PATH, overwrite=True, dry_run=True)
print(expanse_path.joinpath('BSI_DIS_XX_XX_13_v2.tif'))

# ops = download(r"\nluu9ot\home\research-exposures\National\Netherlands\Built\WAL_B10_XX_XX_20_v3.tif", r"C:\Users\5298954\Documents\Projects\Exposure_Map\test_data\demo\WAL_B10\Netherlands")
ops.print_summary()

session.close()