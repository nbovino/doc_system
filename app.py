from flask import (Flask, flash, render_template, redirect, url_for, request, session, jsonify, json)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import exc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import data_functions
import time

import datetime
import forms
import db_connect
import models
import re

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'nfj298RFERf4iwg4f4wfsrgSWFFELNFE:!#RefwkFpyio'
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    all_asset_types = db_connect.query_all(models.AssetTypes)
    if request.args.get('solution_category'):
        solution_category = request.args.get('solution_category')
    else:
        solution_category = '0'
    if request.args.get('company'):
        company = request.args.get('company')
    else:
        company = '0'
    return render_template('base.html',
                           solution_category=solution_category,
                           company=company,
                           asset_types=all_asset_types)


@app.route('/view_solutions', methods=['GET', 'POST'])
def view_solutions():
    if request.args.get('asset_type'):
        asset_type = request.args.get('asset_type')
    type_id = db_connect.query_one_db(models.AssetTypes, models.AssetTypes.asset_type, asset_type)
    return render_template('view_solutions.html',
                           asset_type=asset_type,
                           asset_types=db_connect.query_all(models.AssetTypes),
                           latest_five=db_connect.query_latest_five_by_asset_type(type_id.id)
                           )


@app.route('/view_one_solution', methods=['GET', 'POST'])
def view_one_solution():
    if request.args.get('solution_id'):
        solution_id = request.args.get('solution_id')
    else:
        solution_id = 0
    solution = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=solution_id)
    associated_asset_types = solution.associated_asset_types
    assoc_names = []
    assoc_dict = {}
    for t in associated_asset_types:
        a_type = db_connect.query_one_db(model=models.AssetTypes, column=models.AssetTypes.id, v=t)
        assoc_names.append(a_type.asset_type)
        assoc_dict[str(a_type.id)] = a_type.asset_type
    data_folder = Path("static/data/assoc_types_for_solution.json")
    with open(data_folder, 'w') as fp:
        json.dump(assoc_dict, fp, indent=4)
    data_functions.write_asset_types_to_json()
    data_functions.one_solution_asset_types(solution_id)
    return render_template('view_one_solution.html',
                           asset_types=db_connect.query_all(models.AssetTypes),
                           associated_asset_types=assoc_names,
                           solution_id=solution_id,
                           steps=solution.steps,
                           title=solution.solution_title)


@app.route('/add_asset_type', methods=['GET', 'POST'])
def add_asset_type():
    data = request.form
    db_connect.insert_db(models.AssetTypes(asset_type=data['new-asset-type']))
    return str(data['new-asset-type'])


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    add_asset_form = forms.AddAssetForm()
    add_asset_type_form = forms.AddAssetTypeForm()
    add_manufacturer_form = forms.AddManufacturerForm()
    add_department_form = forms.AddDepartmentForm()
    add_asset_form.department.choices = [('', 'Select Department')]
    add_asset_form.manufacturer.choices = [('', 'Select Manufacturer')]
    add_asset_form.asset_type.choices = [('', 'Select Asset Type')]
    return render_template('add_asset.html',
                           add_asset_form=add_asset_form,
                           add_asset_type_form=add_asset_type_form,
                           add_manufacturer_form=add_manufacturer_form,
                           add_department_form=add_department_form
                           )


@app.route('/add_solution', methods=['GET', 'POST'])
def add_solution():
    if request.args.get('message'):
        message = request.args.get('message')
    else:
        message = 0
    if request.args.get('asset_type'):
        asset_type = request.args.get('asset_type')
    else:
        asset_type = 0
    return render_template('add_solution.html',
                           message=message,
                           asset_type=asset_type,
                           asset_types=db_connect.query_all(models.AssetTypes))


@app.route('/add_solution_post', methods=['GET', 'POST'])
def add_solution_post():
    # return render_template('add_solution.html', combined=combined_steps)
    data = request.form
    # print(request.form)
    combined_steps = {}
    temp_dict = {}
    count = 1
    # TODO: Put in the asset type into a variable to put in the associated asset types column
    # for v in data.keys():
    #     print(type(data[v]))
    #     print(v)
    #     print(data[v])
    #     temp_dict[str(count)] = data[v]
    #         print(data['solution'][v])
    #         count += 1
    asset_type = db_connect.query_one_db(model=models.AssetTypes,
                                         column=models.AssetTypes.asset_type,
                                         v=data['asset_type'])
    print(data['solution'])
    solution = data['solution'].split('&')
    for s in solution:
        print(s)
        if s[:4] == 'step':
            step = s.replace("%20", " ")
            temp_dict[str(count)] = step.split('=')[1]
            print(s.split('=')[0] + ' - ' + s.split('=')[1])
            count += 1
        if 'solution_title' in s:
            title = s.split('=')[1]
            title = title.replace("%20", " ")
    # print(data['asset_type'])
    for i in temp_dict:
        print(i, temp_dict[i])
    print(asset_type.id, asset_type.asset_type)
    # for i in temp_dict:
    #     print(i)
    # print(v + " - " + data[v])
    # print(data['solution_title'])
    # print(temp_dict)
    # combined_steps['Steps'] = temp_dict
    # print(combined_steps)
    print(type(asset_type.id))
    db_connect.insert_db(models.Solutions(solution_title=title,
                                          steps=temp_dict,
                                          date_added=datetime.datetime.now(),
                                          date_revised=datetime.datetime.now(),
                                          associated_asset_types=[asset_type.id],
                                          user=1))

    # if request.method == 'GET':
    #     return jsonify(combined_steps)
    return combined_steps


@app.route('/add_assoc_type', methods=['GET', 'POST'])
def add_assoc_type():
    data = request.form
    # solution_id = data['solution_id']
    print(data['added_types'])
    print('solution ID: ' + data['solution_id'])
    return data


@app.route('/edit_solution', methods=['GET', 'POST'])
def edit_solution():
    pass


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
