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
    data_functions.write_all_solution_data()
    if request.args.get('solution_category'):
        solution_category = request.args.get('solution_category')
    else:
        solution_category = '0'
    if request.args.get('company'):
        company = request.args.get('company')
    else:
        company = '0'

    return render_template('base.html',
                           all_departments=db_connect.query_all(models.Departments),
                           solution_category=solution_category,
                           company=company,
                           asset_types=all_asset_types)


@app.route('/view_solutions', methods=['GET', 'POST'])
def view_solutions():
    if request.args.get('asset_type'):
        asset_type = request.args.get('asset_type')
    this_asset_type = db_connect.query_one_db(models.AssetTypes, models.AssetTypes.id, asset_type)
    return render_template('view_solutions.html',
                           asset_type=this_asset_type.asset_type,
                           manufacturers=data_functions.manufacturers_as_dict(),
                           asset_types=db_connect.query_all(models.AssetTypes),
                           latest_five=db_connect.query_latest_five_by_asset_type(this_asset_type.id),
                           latest_five_assets=db_connect.query_latest_five_better(model=models.Assets,
                                                                                  column=models.Assets.asset_type,
                                                                                  v=this_asset_type.id)
                           )


# @app.route('/add_type_to_solution', methods=['GET', 'POST'])
# def add_type_to_solution():
#     form =  = request.add_type_to_solution_form['asset_types']
#     for r in all_request:
#         print(r)
#     return redirect(url_for('main'))


@app.route('/view_one_solution', methods=['GET', 'POST'])
def view_one_solution():
    add_type_to_solution_form = forms.AddAssetTypeToSolutionForm()
    add_assoc_solution_form = forms.AddAssocSolutionForm()
    change_primary_asset_type_form = forms.ChangePrimaryAssetTypeForm()
    if request.args.get('solution_id'):
        solution_id = request.args.get('solution_id')
    else:
        solution_id = 0
    if request.args.get('asset_types'):
        for r in request.args.get('asset_types'):
            print(r)
    data_functions.one_solution_data(solution_id)
    # print("this is solution ID" + str(solution_id))
    solution = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=solution_id)
    associated_asset_types = solution.associated_asset_types
    assoc_dict = {}
    all_types = db_connect.query_all(models.AssetTypes)
    # I believe the below comment is resolved. Leaving in just in case it is not.
    # this is causing an issue when reloading the page. It is returning too many things.
    for t in associated_asset_types:
        a_type = db_connect.query_one_db(model=models.AssetTypes, column=models.AssetTypes.id, v=t)
        assoc_dict[str(a_type.id)] = a_type.asset_type
    change_primary_choices = list(assoc_dict.items())
    change_primary_asset_type_form.all_asset_types.choices = change_primary_choices
    data_folder = Path("static/data/assoc_types_for_solution.json")
    with open(data_folder, 'w') as fp:
        json.dump(assoc_dict, fp, indent=4)
    data_functions.write_asset_types_to_json()

    data_functions.one_solution_asset_types(solution_id)

    add_type_to_solution_form.solution_id.data = solution_id
    non_assoc_types = []
    add_type_to_solution_form.asset_types.choices = non_assoc_types
    for t in all_types:
        if t.id not in associated_asset_types:
            non_assoc_types.append((str(t.id), t.asset_type))
    if change_primary_asset_type_form.change_primary_asset_type_submit.data and change_primary_asset_type_form.validate():
        db_connect.update_column(model=models.Solutions,
                                 column=models.Solutions.primary_asset_type,
                                 id=solution_id,
                                 v=change_primary_asset_type_form.all_asset_types.data)
        data_functions.one_solution_data(solution_id)
    # Adds asset type to solution
    if add_type_to_solution_form.add_submit.data and add_type_to_solution_form.validate():
        solution = db_connect.query_one_db(model=models.Solutions,
                                           column=models.Solutions.id,
                                           v=solution_id)
        updated_list = solution.associated_asset_types
        for t in add_type_to_solution_form.asset_types.data:
            if t not in solution.associated_asset_types:
                updated_list.append(int(t))
                print(t)
        db_connect.update_assoc_asset_types(sid=int(add_type_to_solution_form.solution_id.data),
                                            values=updated_list)
        db_connect.update_column(model=models.Solutions,
                                 id=solution_id,
                                 column=models.Solutions.date_revised,
                                 v=datetime.datetime.now())
        redirect(url_for('view_one_solution', solution_id=add_type_to_solution_form.solution_id.data))

    # Adds associated solution
    if add_assoc_solution_form.assoc_solution_submit.data and add_assoc_solution_form.validate():
        print(add_assoc_solution_form.assoc_solution_id.data + "will be added")
        update_column = db_connect.query_one_db(model=models.Solutions,
                                                column=models.Solutions.id,
                                                v=int(add_assoc_solution_form.main_solution_id.data))
        print(str(add_assoc_solution_form.assoc_solution_id.data) + " added to " + str(update_column.id))

        # This makes sure the associated solution is not the solution itself
        if int(add_assoc_solution_form.assoc_solution_id.data) == int(
                update_column.id):  # or update_column.associated_solutions is None or int(add_assoc_solution_form.assoc_solution_id.data) in update_column.associated_solutions:
            print("Caught to be the same solution!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('view_one_solution', solution_id=add_assoc_solution_form.main_solution_id.data))
        else:
            # If the solution IDs are not the same, check if there is an associated solution yet.
            if update_column.associated_solutions is None:
                # If there are no associated solutions, make an empty list
                print("No associated solutions!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                associated_solutions = []
                db_connect.update_column(model=models.Solutions,
                                         id=int(add_assoc_solution_form.main_solution_id.data),
                                         column=models.Solutions.associated_solutions,
                                         v=associated_solutions + [int(add_assoc_solution_form.assoc_solution_id.data)])
            # If the solution IDs are not the same, make sure it is not already an associated solution
            elif int(add_assoc_solution_form.assoc_solution_id.data) not in update_column.associated_solutions:
                print("Adding to solution!!!!!!!!!!!!!!!!!!!!!!!")
                # If it is already an associated solution it will just reload the page. Can make a message later
                # There might be a way to make the Array field have to be unique with sqlalchemy.
                # In which case I could just but this in a try/except statement.
                associated_solutions = []
                s = data_functions.get_associated_solutions(solution_id)
                for i in s:
                    associated_solutions.append(i)
                print(associated_solutions + [int(add_assoc_solution_form.assoc_solution_id.data)])
                db_connect.update_column(model=models.Solutions,
                                         id=int(add_assoc_solution_form.main_solution_id.data),
                                         column=models.Solutions.associated_solutions,
                                         v=associated_solutions + [int(add_assoc_solution_form.assoc_solution_id.data)])
                redirect(url_for('view_one_solution', solution_id=add_assoc_solution_form.main_solution_id.data))

    return render_template('view_one_solution.html',
                           asset_types=db_connect.query_all(models.AssetTypes),
                           associated_asset_types=data_functions.one_solution_asset_types(solution_id),
                           assoc_solutions=data_functions.get_associated_solutions(solution_id),
                           non_assoc_types=non_assoc_types,
                           all_asset_types=data_functions.write_asset_types_to_json(),
                           add_type_to_solution_form=add_type_to_solution_form,
                           add_assoc_solution_form=add_assoc_solution_form,
                           change_primary_asset_type_form=change_primary_asset_type_form,
                           solution_id=solution_id,
                           steps=solution.steps,
                           title=solution.solution_title)


@app.route('/view_one_asset', methods=['GET', 'POST'])
def view_one_asset():
    if request.args.get('asset_id'):
        asset_id = request.args.get('asset_id')
    else:
        asset_id = 0
    asset = db_connect.query_one_db(model=models.Assets,
                                    column=models.Assets.id,
                                    v=asset_id)
    data_functions.write_asset_data_to_json(asset_id)
    add_asset_type_form = forms.AddAssetTypeForm()
    add_manufacturer_form = forms.AddManufacturerForm()
    add_department_form = forms.AddDepartmentForm()
    all_asset_types = []
    all_departments = []
    all_manufacturers = []
    try:
        for t in db_connect.query_all(models.AssetTypes):
            all_asset_types.append((str(t.id), t.asset_type.title()))
    except:
        pass
    try:
        for d in db_connect.query_all(models.Departments):
            all_departments.append((str(d.id), d.department.title()))
    except:
        pass
    try:
        for m in db_connect.query_all(models.Manufacturers):
            all_manufacturers.append((str(m.id), m.manufacturer.title()))
    except:
        pass

    edit_asset_form = forms.EditAssetForm()
    edit_asset_form.asset_type.choices = all_asset_types
    edit_asset_form.department.choices = all_departments
    edit_asset_form.manufacturer.choices = all_manufacturers

    if add_asset_type_form.asset_type_submit.data and add_asset_type_form.validate():
        db_connect.insert_db(models.AssetTypes(asset_type=add_asset_type_form.asset_type.data))
        return redirect(url_for('view_one_asset', asset_id=asset_id))
    if add_department_form.department_submit.data and add_department_form.validate():
        db_connect.insert_db(models.Departments(department=add_department_form.department.data))
        return redirect(url_for('view_one_asset', asset_id=asset_id))
    if add_manufacturer_form.manufacturer_submit.data and add_manufacturer_form.validate():
        db_connect.insert_db(models.Manufacturers(manufacturer=add_manufacturer_form.manufacturer.data))
        return redirect(url_for('view_one_asset', asset_id=asset_id))

    if edit_asset_form.edit_asset_submit.data and edit_asset_form.validate():
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.asset_type, v=edit_asset_form.asset_type.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.manufacturer, v=edit_asset_form.manufacturer.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.model, v=edit_asset_form.model.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.serial_no, v=edit_asset_form.serial_no.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.dia_asset_tag, v=edit_asset_form.dia_asset_tag.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.name, v=edit_asset_form.name.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.description, v=edit_asset_form.description.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.ip_address, v=edit_asset_form.ip_address.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.department, v=edit_asset_form.department.data)
        db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.date_revised, v=datetime.datetime.now())
        return redirect(url_for('view_one_asset', asset_id=asset_id))

    edit_asset_form.asset_type.default = str(asset.asset_type)
    edit_asset_form.process()
    edit_asset_form.department.default = str(asset.department)
    edit_asset_form.process()
    edit_asset_form.manufacturer.default = str(asset.manufacturer)
    edit_asset_form.process()
    edit_asset_form.model.default = asset.model
    edit_asset_form.process()
    if asset.serial_no:
        edit_asset_form.serial_no.default = asset.serial_no
        edit_asset_form.process()
    if asset.dia_asset_tag:
        edit_asset_form.dia_asset_tag.default = asset.dia_asset_tag
        edit_asset_form.process()
    if asset.name:
        edit_asset_form.name.default = asset.name
        edit_asset_form.process()
    if asset.description:
        edit_asset_form.description = asset.description
        edit_asset_form.process()
    if asset.ip_address:
        edit_asset_form.ip_address = asset.ip_address
        edit_asset_form.process()

    return render_template('view_one_asset.html',
                           asset_types=db_connect.query_all(models.AssetTypes),
                           manufacturers=data_functions.manufacturers_as_dict(),
                           departments=data_functions.departments_as_dict(),
                           asset_id=asset_id,
                           add_asset_type_form=add_asset_type_form,
                           add_manufacturer_form=add_manufacturer_form,
                           add_department_form=add_department_form,
                           edit_asset_form=edit_asset_form,
                           asset=asset)


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    add_asset_form = forms.AddAssetForm()
    add_asset_type_form = forms.AddAssetTypeForm()
    add_manufacturer_form = forms.AddManufacturerForm()
    add_department_form = forms.AddDepartmentForm()
    all_asset_types = []
    all_departments = []
    all_manufacturers = []
    try:
        for t in db_connect.query_all(models.AssetTypes):
            all_asset_types.append((str(t.id), t.asset_type.title()))
    except:
        pass
    try:
        for d in db_connect.query_all(models.Departments):
            all_departments.append((str(d.id), d.department.title()))
    except:
        pass
    try:
        for m in db_connect.query_all(models.Manufacturers):
            all_manufacturers.append((str(m.id), m.manufacturer.title()))
    except:
        pass

    if add_asset_type_form.asset_type_submit.data and add_asset_type_form.validate():
        db_connect.insert_db(models.AssetTypes(asset_type=add_asset_type_form.asset_type.data))
        return redirect(url_for('add_asset'))
    if add_department_form.department_submit.data and add_department_form.validate():
        db_connect.insert_db(models.Departments(department=add_department_form.department.data))
        return redirect(url_for('add_asset'))
    if add_manufacturer_form.manufacturer_submit.data and add_manufacturer_form.validate():
        db_connect.insert_db(models.Manufacturers(manufacturer=add_manufacturer_form.manufacturer.data))
        return redirect(url_for('add_asset'))

    add_asset_form.asset_type.choices = [('', 'Select Asset Type')] + all_asset_types
    add_asset_form.department.choices = [('', 'Select Department')] + all_departments
    add_asset_form.manufacturer.choices = [('', 'Select Manufacturer')] + all_manufacturers
    if add_asset_form.asset_submit.data and add_asset_form.validate():
        db_connect.insert_db(models.Assets(asset_type=add_asset_form.asset_type.data,
                                           manufacturer=add_asset_form.manufacturer.data,
                                           model=add_asset_form.model.data,
                                           serial_no=add_asset_form.serial_no.data,
                                           dia_asset_tag=add_asset_form.dia_asset_tag.data,
                                           name=add_asset_form.name.data,
                                           description=add_asset_form.description.data,
                                           ip_address=add_asset_form.ip_address.data,
                                           department=add_asset_form.department.data,
                                           date_added=datetime.datetime.now(),
                                           date_revised=datetime.datetime.now()
                                           )
                             )
        return redirect(url_for('view_solutions', asset_type=add_asset_form.asset_type.data))

    return render_template('add_asset.html',
                           asset_types=db_connect.query_all(models.AssetTypes),
                           add_asset_form=add_asset_form,
                           add_asset_type_form=add_asset_type_form,
                           add_manufacturer_form=add_manufacturer_form,
                           add_department_form=add_department_form
                           )


@app.route('/add_asset_type', methods=['GET', 'POST'])
def add_asset_type():
    data = request.form
    db_connect.insert_db(models.AssetTypes(asset_type=data['new-asset-type']))
    return str(data['new-asset-type'])


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


@app.route('/edit_solution_post', methods=['GET', 'POST'])
def edit_solution_post():
    # TODO: Be able to edit the associated solutions and associated assets
    data = request.form
    new_steps = {}
    count = 1
    for d in data:
        print(d, data[d])
    solution = data['solution'].split('&')
    for s in solution:
        print(s)
        if s[:4] == 'step':
            step = s.replace("%20", " ")
            new_steps[str(count)] = step.split('=')[1]
            print(s.split('=')[0] + ' - ' + s.split('=')[1])
            count += 1
        if 'solution_title' in s:
            title = s.split('=')[1]
            title = title.replace("%20", " ")
    print(title, new_steps, id)
    db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.solution_title,
                             v=title)
    db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.steps, v=new_steps)
    db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.date_revised,
                             v=datetime.datetime.now())
    data_functions.write_all_solution_data()
    return new_steps


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
                                          primary_asset_type=asset_type.id,
                                          associated_asset_types=[asset_type.id],
                                          user=1))

    # if request.method == 'GET':
    #     return jsonify(combined_steps)
    data_functions.write_all_solution_data()
    return combined_steps


@app.route('/add_assoc_type', methods=['GET', 'POST'])
def add_assoc_type():
    data = request.form
    solution_id = data['solution_id']
    print(data['added_types'])
    print('solution ID: ' + data['solution_id'])
    data_functions.write_all_solution_data()
    return data


@app.route('/edit_solution', methods=['GET', 'POST'])
def edit_solution():
    data_functions.write_all_solution_data()
    pass


@app.route('/edit_solution_remove_assoc_solution', methods=['GET', 'POST'])
def edit_solution_remove_assoc_solution():
    data = request.form
    print("solution to remove: " + data['sol_to_remove'] + " | Solution ID: " + data['solution_id'])
    solution_to_update = db_connect.query_one_db(model=models.Solutions,
                                                 column=models.Solutions.id,
                                                 v=data['solution_id'])
    assoc_solutions = solution_to_update.associated_solutions
    assoc_solutions.remove(int(data['sol_to_remove']))
    db_connect.update_column(model=models.Solutions,
                             column=models.Solutions.associated_solutions,
                             id=int(data['solution_id']),
                             v=assoc_solutions)
    return data


@app.route('/edit_solution_remove_rel_asset_type', methods=['GET', 'POST'])
def edit_solution_remove_rel_asset_type():
    data = request.form
    print("Type to remove: " + data["type_to_remove"] + " | Solution ID: " + data['solution_id'])
    solution_to_update = db_connect.query_one_db(model=models.Solutions,
                                                 column=models.Solutions.id,
                                                 v=data['solution_id'])
    assoc_asset_types = solution_to_update.associated_asset_types
    # Double checks it's not the same as the primary asset type before removing
    if solution_to_update.primary_asset_type != int(data['type_to_remove']):
        assoc_asset_types.remove(int(data['type_to_remove']))
    db_connect.update_column(model=models.Solutions,
                             column=models.Solutions.associated_asset_types,
                             id=int(data['solution_id']),
                             v=assoc_asset_types)
    return data


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
