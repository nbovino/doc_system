import db_connect
import models
from pathlib import Path
import json

def write_asset_types_to_json():
    asset_types = db_connect.query_all(models.AssetTypes)
    type_dict = {}
    for i in asset_types:
        type_dict[i.id] = i.asset_type
    data_folder = Path("static/data/all_assoc_types.json")
    with open(data_folder, 'w') as fp:
        json.dump(type_dict, fp, indent=4)