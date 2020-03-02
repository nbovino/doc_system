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
    return type_dict


def one_solution_asset_types(solution_id):
    # This needs fixed. This should really call a function that just returns a dictionary of all asset types without writing json again
    all_asset_types = write_asset_types_to_json()
    solution_asset_types = {}
    associated_solutions = {}
    solution = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=solution_id)
    for t in solution.associated_asset_types:
        a_type = db_connect.query_one_db(model=models.AssetTypes, column=models.AssetTypes.id, v=t)
        solution_asset_types[t] = a_type.asset_type
    if solution.associated_solutions:
        for a in solution.associated_solutions:
            asid = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=a)
            associated_solutions[a] = asid.solution_title

    all_solution_data = {
        'all_asset_types': all_asset_types,
        'solution_asset_types': solution_asset_types,
        'associated_solutions': associated_solutions,
    }
    data_folder = Path("static/data/one_solution_data.json")
    with open(data_folder, 'w') as fp:
        json.dump(all_solution_data, fp, indent=4)
    return solution_asset_types


def one_solution_data(solution_id):
    solution_data = {}
    solution = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=solution_id)
    solution_data["Solution_id"] = solution.id
    solution_data["Title"] = solution.solution_title
    solution_data["Steps"] = solution.steps
    solution_data["Associated_Asset_Types"] = solution.associated_asset_types
    data_folder = Path("static/data/one_solution.json")
    with open(data_folder, 'w') as fp:
        json.dump(solution_data, fp, indent=4)
    return None


def solution_title_table():
    all_solutions = db_connect.query_all(models.Solutions)
    solution_data = []
    for s in all_solutions:
        solution_data.append(
            {
             'id': s.id,
             'title': s.solution_title
             }
        )
    data_folder = Path("static/data/all_solution_data.json")
    with open(data_folder, 'w') as fp:
        json.dump(solution_data, fp, indent=4)
    return None
