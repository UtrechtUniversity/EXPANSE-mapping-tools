import pandas as pd
import json
import sys

def table_to_json(table_path, json_path):
    df = pd.read_csv(table_path, dtype={'show_on_map': 'bool'}, on_bad_lines='skip', header=0, delimiter=';', keep_default_na=False, encoding='latin1')
    metadata_json = {"Built": {}, "Physico-Chemical": {}}

    for index, row in df.iterrows():
        if row['Category'] in metadata_json:
            if row['Theme'] in metadata_json[row['Category']]:
                metadata_json[row['Category']][row['Theme']].append(row.to_dict())
            else:
                metadata_json[row['Category']][row['Theme']] = [row.to_dict()]

    with open(json_path, 'w') as json_file:
        json.dump(metadata_json, json_file, indent=4)

def comman_line_router(args):
    if len(args) != 3:
        sys.exit(1)

    table_path = args[1]
    json_path = args[2]
    table_to_json(table_path, json_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        comman_line_router(sys.argv)
    
    else:
        table_path = r"C:/Users/5298954/Documents/Github_Repos/Exposome-Map-Documents/Exposome_maps_inventory/Exposome maps inventory.csv"
        json_path = r"C:/Users/5298954/Documents/Github_Repos/exposome-maps/metadata.json"
        
        table_to_json(table_path, json_path)