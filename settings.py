LOCAL_PATH = "C:/Users/5298954/Documents/Projects/Exposure_Map/project_geoserver/data_dir/data"

INDEXER = "C:/Users/5298954/Documents/Projects/Exposure_Map/indexer.properties"
TIMEREGEX = "C:/Users/5298954/Documents/Projects/Exposure_Map/timeregex.properties"


# CATEGORIES = ["Food", "Physico-chemical", "Built"]
CATEGORIES = ["Built"]
FOOD_PREFIXES = [
    "FastF_800m",
    "Rest_800m",
    "Superm_800m",
    "FastF_KD_800m",
    "Rest_KD_800m",
    "Superm_KD_800m"
]

PHYSICAL_CHEMICAL_PREFIXES = [
    # "NO2B25_AAV", 
    # "NO2B25_MAV", 
    # "P10B25_AAV", 
    # "P10B25_MAV", 
    # "P25B25_AAV", 
    # "P25B25_MAV", 
    # "OZOB25_AAV", 
    # "OZOB25_MAV", 
    # "UV_AVG", 
    # "UV_MAX", 
    # "UR_B15", 
    # "RTN_AVG"
    # "TMP_AVG",
    # "TEMP_AVG"
]

BUILT_PREFIXES = [
    "NDV_MD3", 
    "NDV_MD5", 
    "NDV_MD1", 
    "NDV_ST3", 
    "NDV_ST5", 
    "NDV_ST1", 
    "NDV_ME3", 
    "NDV_ME5", 
    "NDV_ME1", 
    # "MVI_MD3", 
    # "MVI_MD5", 
    # "MVI_MD1", 
    # "MVI_ST3", 
    # "MVI_ST5", 
    # "MVI_ST1", 
    # "MVI_ME3", 
    # "MVI_ME5", 
    # "MVI_ME1", 
    # "GSC_DIS", 
    # "GSU_DIS", 
    # "BSW_DIS", 
    # "BSS_DIS", 
    # "BSI_DIS",
    # "IMP_B03", 
    # "IMP_B05", 
    # "IMP_B10", 
    # "LAN_B03", 
    # "LAN_B05", 
    # "LAN_B10", 
    # "WAL_B03", 
    # "WAL_B05", 
    # "WAL_B10"
]

COUNTRIES = {
    "EUROPE": ("Albania", "Andorra", "Austria", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Faroes", "Finland", "France", "Germany", "Greece", "Guernsey", "Hungary", "Iceland", "Ireland", "Isle of Man", "Italy", "Jersey", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "United Kingdom", "Vatican City"),
    "NETHERLANDS": ("Netherlands",),
    "LOW_COUNTRIES": ("Belgium", "Luxembourg", "Netherlands")
    }