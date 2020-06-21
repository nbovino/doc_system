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


def get_associated_solutions(solution_id):
    s = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=solution_id)
    assoc_solutions = {}
    if s.associated_solutions:
        for r in s.associated_solutions:
            asid = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=r)
            assoc_solutions[asid.id] = asid.solution_title
    else:
        assoc_solutions = []
    return assoc_solutions


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
    step_number = []
    for s in solution.steps:
        step_number.append(s)
    if len(step_number) > 0:
        solution_data["Highest_Step"] = max(step_number)
    else:
        solution_data["Highest_Step"] = '0'
    solution_data["Associated_Asset_Types"] = solution.associated_asset_types
    solution_data["Primary_Asset_Type"] = solution.primary_asset_type
    data_folder = Path("static/data/one_solution.json")
    with open(data_folder, 'w') as fp:
        json.dump(solution_data, fp, indent=4)
    return None


def write_all_solution_data():
    all_solutions = db_connect.query_all(models.Solutions)
    solution_data = []
    for s in all_solutions:
        main_asset_type = db_connect.query_one_db(model=models.AssetTypes, column=models.AssetTypes.id, v=s.primary_asset_type)
        solution_data.append(
            {
             'id': s.id,
             'title': s.solution_title,
             'primary_asset_type': main_asset_type.asset_type
             }
        )
    data_folder = Path("static/data/all_solution_data.json")
    with open(data_folder, 'w') as fp:
        json.dump(solution_data, fp, indent=4)
    return None


def write_one_asset_data_to_json(asset_id):
    asset_data = {}
    asset = db_connect.query_one_db(model=models.Assets, column=models.Assets.id, v=asset_id)
    asset_data["Asset_Id"] = asset.id
    asset_data["Asset_Type"] = asset.asset_type
    asset_data["Manufacturer"] = asset.manufacturer
    asset_data["Model"] = asset.model
    asset_data["Serial_No"] = asset.serial_no
    asset_data["Dia_Asset_Tag"] = asset.dia_asset_tag
    asset_data["Description"] = asset.description
    asset_data["Department"] = asset.department
    asset_data["Location"] = asset.location
    # data_folder = Path("static/data/one_asset.json")
    # with open(data_folder, 'w') as fp:
    #     json.dump(asset_data, fp, indent=4)
    return asset_data


def write_asset_data_to_json(asset_id=0):
    if asset_id != 0:
        asset_data = {}
        all_types = []
        all_manufacturers = []
        all_departments = []
        for t in db_connect.query_all(models.AssetTypes):
            all_types.append(
                {
                    'id': t.id,
                    'asset_type': t.asset_type
                }
            )
        for m in db_connect.query_all(models.Manufacturers):
            all_manufacturers.append(
                {
                    'id': m.id,
                    'manufacturer': m.manufacturer
                }
            )
        for d in db_connect.query_all(models.Departments):
            all_departments.append(
                {
                    'id': d.id,
                    'department': d.department
                }
            )
        asset_data['all_types'] = all_types
        asset_data['all_manufacturers'] = all_manufacturers
        asset_data['all_departments'] = all_departments
        asset_data['this_asset'] = write_one_asset_data_to_json(asset_id)
        data_folder = Path("static/data/all_asset_data.json")
        with open(data_folder, 'w') as fp:
            json.dump(asset_data, fp, indent=4)
        return None
    else:
        return None

# This makes a dictionary of { Manufacturer: { Asset_Type: [ Model no. list ] }, Manufacturer: { Asset_Type: [ Model no. list ] }}
def asset_models_by_manufacturer():
    all_manufacturers = db_connect.query_all(models.Manufacturers)
    all_asset_types = db_connect.query_all(models.AssetTypes)
    model_by_manufacturer = {}
    for m in all_manufacturers:
        asset_type_list = {}
        for t in all_asset_types:
            model_numbers_for_type = []
            q = db_connect.query_distinct_for_models(m.id, t.id)
            for model_no in q:
                model_numbers_for_type.append(model_no.model)
            asset_type_list[t.id] = model_numbers_for_type
        model_by_manufacturer[m.id] = asset_type_list
    print(model_by_manufacturer)
    return model_by_manufacturer


def manufacturers_as_dict():
    all_manufacturers = db_connect.query_all(models.Manufacturers)
    manufacturer_dict = {}
    for m in all_manufacturers:
        manufacturer_dict[m.id] = m.manufacturer
    return manufacturer_dict


def departments_as_dict():
    all_departments = db_connect.query_all(models.Departments)
    dept_dict = {}
    for d in all_departments:
        dept_dict[d.id] = d.department
    return dept_dict


def software_companies_as_dict():
    all_software_companies = db_connect.query_all(models.SoftwareCompanies)
    software_co_dict = {}
    for s in all_software_companies:
        software_co_dict[s.id] = s.software_company
    return software_co_dict

def software_names_as_dict():
    all_software = db_connect.query_all(models.Software)
    software_name_dict = {}
    for s in all_software:
        software_name_dict[s.id] = s.software_name
    return software_name_dict