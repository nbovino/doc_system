from flask import (Flask, flash, render_template, redirect, url_for, request, session, jsonify, json)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import exc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
from pathlib import Path
import data_functions
import time
import os
from werkzeug.utils import secure_filename

import datetime
import forms
import db_connect
import models
import re
import shutil

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nfj298RFERf4iwg4f4wfsrgSWFFELNFE:!#RefwkFpyio'
TEST_UPLOAD_FOLDER = "\\documentation_system\static\data\images"
# TEST_UPLOAD_FOLDER = "\\Users\Nate"
app.config['UPLOAD_FOLDER'] = TEST_UPLOAD_FOLDER
dirname = os.path.dirname(__file__)

# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)


@app.route('/test_form', methods=['GET', 'POST'])
def test_form():
    return render_template('test_form.html')


@app.route('/test_submit_form', methods=['GET', 'POST'])
def test_submit_form():
    if request.method == 'POST':
        complete_solution = {}
        d, i, t = 'data', 'images', 'test_image_upload'
        # file = request.files['test_image']
        # filename = secure_filename(file.filename)
        # try:
        #     os.mkdir(os.path.relpath(TEST_UPLOAD_FOLDER + "img_test"))
        # except OSError:
        #     print("Creation failed")
        # else:
        #     print("Successfully created!!!!!!!!")
        # print(file)
        data = request.form
        # print(type(data))
        images = request.files
        for d in data:
            print(d)
            print(d[4:])
        try:
            os.mkdir('\\documentation_system\\static\data\\solution_images')
        except FileExistsError:
            print("directory already exists")
        step_count = 1
        for step in request.form:
            image_file_names = []
            try:
                os.mkdir('\\documentation_system\\static\data\\solution_images\\step' + str(step_count))
            except FileExistsError:
                print("directory already exists")
            for i in images:
                if i[5:] == step[4:]:
                    # images = request.files[i]
                    step_images = request.files.getlist(i)
                    for se in step_images:
                        if se.filename:
                            se.save(se.filename)
                            shutil.move('\\documentation_system\\' + se.filename,
                                        '\\documentation_system\\static\data\\solution_images\\step' + str(step_count))
                            image_file_names.append(se.filename)
            step_info = {
                "Instruction": request.form[step],
                "Images": image_file_names
            }
            complete_solution[str(step_count)] = step_info
            step_count += 1
        print(complete_solution)
        # file.save(file.filename)
        # shutil.move('\\documentation_system\\' + file.filename, '\\documentation_system\\static\data\images\\' + file.filename)
        # os.rename(TEST_UPLOAD_FOLDER + filename, 'test.jpg')
    return render_template('test_submit_form.html')


@app.route('/', methods=['GET', 'POST'])
def main():
    all_asset_types = db_connect.query_all(models.AssetTypes)
    data_functions.write_all_solution_data()
    add_department_form = forms.AddDepartmentForm()
    if request.args.get('solution_category'):
        solution_category = request.args.get('solution_category')
    else:
        solution_category = '0'
    if request.args.get('company'):
        company = request.args.get('company')
    else:
        company = '0'
    if add_department_form.department_submit.data and add_department_form.validate():
        db_connect.insert_db(models.Departments(department=add_department_form.department.data))
        return redirect(url_for('main'))
    # This is as a test for creating dynamic steps and sending image data through ajax
    # return render_template('test_form.html')
    return render_template('base.html',
                           all_departments=db_connect.query_all(models.Departments),
                           add_department_form=add_department_form,
                           solution_category=solution_category,
                           company=company,
                           asset_types=all_asset_types)


@app.route('/view_solutions', methods=['GET', 'POST'])
def view_solutions():
    if request.args.get('asset_type'):
        asset_type = request.args.get('asset_type')
    this_asset_type = db_connect.query_one_db(models.AssetTypes, models.AssetTypes.id, asset_type)
    return render_template('view_solutions.html',
                           all_departments=db_connect.query_all(models.Departments),
                           asset_type=this_asset_type.asset_type,
                           asset_type_id=this_asset_type.id,
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

    # Get image filenames for each step in the solution
    solution_path = '\\documentation_system\\static\data\\solution_images\\sid' + solution_id
    # solution_path = '\\documentation_system\\static\data\\solution_images\\sid' + solution_id
    # solution_path = 'documentation_system/static/data/solution_images/sid' + solution_id
    step_folders = [f.path for f in os.scandir(solution_path) if f.is_dir()]
    step_count = 1
    step_images = {}
    f = open('\\documentation_system\\static\data\one_solution.json')
    solution_json = json.load(f)
    # for s in step_folders:
    #     # This doesn't work because listdir(s) is a list of all the filenames in the directory
    #     this_step = []
    #     # for i in os.listdir(s):
    #     # Getting the info from the JSON data instead of the folder because that is what will update when editing
    #     # a solution so that is what it should pull from when selecting what images to get from the directory.
    for s in solution_json['Steps']:
        this_step = []
        for i in solution_json['Steps'][str(step_count)]['Images']:
            this_step.append(["data/solution_images/sid" + str(solution_id) + "/" + i, i])
        step_images[str(step_count)] = this_step
        step_count += 1
    print(step_images)
    # Info on view_one_solution page that may be useful on the edit checkbox for images
    # style='background-image: url("{{ url_for('static', filename=i[0]) }}")'

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
                           title=solution.solution_title,
                           step_images=step_images,
                           public=solution.public,
                           )


@app.route('/public_solution', methods=['GET', 'POST'])
def public_solution():
    if request.args.get('solution_id'):
        sid = request.args.get('solution_id')
    else:
        redirect(url_for('main'))
    solution = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=sid)
    if not solution.public:
        return redirect(url_for('main'))
    primary_asset_type = db_connect.query_one_db(model=models.AssetTypes,
                                                 column=models.AssetTypes.id,
                                                 v=solution.primary_asset_type)
    return render_template('public_solution.html',
                           solution_info=solution,
                           steps=solution.steps,
                           primary_asset_type=primary_asset_type.asset_type,
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
        if edit_asset_form.decommissioned.data:
            db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.decommissioned, v=datetime.datetime.now())
        else:
            db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.decommissioned, v=None)
        if edit_asset_form.deployed.data:
            db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.deployed, v=True)
        else:
            db_connect.update_column(model=models.Assets, id=asset_id, column=models.Assets.deployed, v=False)
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
    if asset.decommissioned:
        edit_asset_form.decommissioned.default = True
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
    data_folder = Path("static/data/one_solution.json")
    with open(data_folder, 'w') as fp:
        json.dump('', fp, indent=4)
    if request.args.get('message'):
        message = request.args.get('message')
    else:
        message = 0
    if request.args.get('asset_type'):
        asset_type = request.args.get('asset_type')
        this_asset_type = db_connect.query_one_db(model=models.AssetTypes, column=models.AssetTypes.id, v=asset_type)
    else:
        asset_type = 0
    return render_template('add_solution.html',
                           message=message,
                           asset_type_name=this_asset_type.asset_type,
                           asset_type_id=asset_type,
                           asset_types=db_connect.query_all(models.AssetTypes))


# This was used on the ajax version of edit solution
# @app.route('/edit_solution_post', methods=['GET', 'POST'])
# def edit_solution_post():
#     # TODO: Be able to edit the associated solutions and associated assets
#     data = request.form
#     new_steps = {}
#     count = 1
#     for d in data:
#         print(d, data[d])
#     solution = data['solution'].split('&')
#     for s in solution:
#         print(s)
#         if s[:4] == 'step':
#             step = s.replace("%20", " ")
#             new_steps[str(count)] = step.split('=')[1]
#             print(s.split('=')[0] + ' - ' + s.split('=')[1])
#             count += 1
#         if 'solution_title' in s:
#             title = s.split('=')[1]
#             title = title.replace("%20", " ")
#         if 'public_solution' in s:
#             public = True
#         else:
#             public = False
#     print(title, new_steps, id)
#     db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.solution_title,
#                              v=title)
#     db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.steps, v=new_steps)
#     db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.date_revised,
#                              v=datetime.datetime.now())
#     db_connect.update_column(model=models.Solutions, id=data['solution_id'], column=models.Solutions.public, v=public)
#     data_functions.write_all_solution_data()
#     return new_steps


@app.route('/edit_solution_post', methods=['GET', 'POST'])
def edit_solution_post():
    if request.method == 'POST':
        all_step_info = {}
        images = request.files
        for i in images:
            print(i)
        data = request.form
        sid = int(data['solution_id'])
        this_sol = db_connect.query_one_db(model=models.Solutions, column=models.Solutions.id, v=sid)
        # all_step_info = {}
        # images = request.files
        # data = request.form
        sol_dir = '\\documentation_system\\static\data\\solution_images\\sid' + str(sid)
        # Edit basics of solution
        # TODO: This is not an efficient way of doing this
        step_count = 1
        for step in request.form:
            if step == 'solution_id' or step == 'solution_title':
                pass
            else:
                if step[:4] == 'step' and 'img' not in step:
                    current_step_no = step[4:]
                    image_file_names = []
                    for step_second in request.form:
                        # For loop to append the list of new images added to the step
                        for i in images:
                            if i[5:] == current_step_no:
                                step_images = request.files.getlist(i)
                                for se in step_images:
                                    print(se)
                                    if se.filename:
                                        try:
                                            src_dir = '\\documentation_system\\'
                                            src_file = '\\documentation_system\\' + se.filename
                                            dst_dir = '\\documentation_system\\static\data\\solution_images\\sid' + str(sid) + '\\'
                                            dst_file = '\\documentation_system\\static\data\\solution_images\\sid' + str(sid) + '\\' + se.filename
                                            # Keep the line immediately below this.
                                            se.save(se.filename)
                                            if os.path.exists(dst_file):
                                                if os.path.samefile(src_file, dst_file):
                                                    continue
                                                os.remove(dst_file)
                                                shutil.move('\\documentation_system\\' + se.filename,
                                                # '\\documentation_system\\static\data\\solution_images\\sid' + str(new_row.id) + '\\step' + str(step_count))
                                                            '\\documentation_system\\static\data\\solution_images'
                                                            '\\sid' + str(sid))
                                            # shutil.move(os.path.join(src, se.filename), os.path.join(dst, se.filename))
                                            print("File has been overwritten!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$$$$$")
                                            # Old way that works
                                        except:
                                            print('There was an error, likely the file already exists')
                                        image_file_names.append(se.filename)
                        # If statement to get the images that are going to still be included in this step
                        if step_second[:4] == 'step' and 'img' in step_second and step_second[4:len(current_step_no) + 4] == current_step_no:
                            image_file_names.append(step_second.split('img')[1])
                    image_file_names = list(dict.fromkeys(image_file_names))
                    step_info = {
                        "Instruction": data[step],
                        "Images": image_file_names
                    }
                    all_step_info[str(step_count)] = step_info
                    step_count += 1
        if 'solution_title' in data:
            title = data['solution_title']
        else:
            title = ''
        if 'public_solution' in data:
            ps = True
        else:
            ps = False
        db_connect.update_column(model=models.Solutions, id=sid, column=models.Solutions.solution_title, v=title)
        db_connect.update_column(model=models.Solutions, id=sid, column=models.Solutions.steps, v=all_step_info)
        db_connect.update_column(model=models.Solutions, id=sid, column=models.Solutions.date_revised, v=datetime.datetime.now())
        db_connect.update_column(model=models.Solutions, id=sid, column=models.Solutions.user, v=1)
        db_connect.update_column(model=models.Solutions, id=sid, column=models.Solutions.public, v=ps)
        print(all_step_info)
        return redirect(url_for('view_one_solution', solution_id=sid))


@app.route('/add_solution_post', methods=['GET', 'POST'])
def add_solution_post():
    if request.method == 'POST':
        db_connect.insert_db(models.Solutions())
        new_row = db_connect.query_latest(models.Solutions)
        all_step_info = {}
        images = request.files
        data = request.form
        for d in data:
            print(d)
        try:
            os.mkdir('\\documentation_system\\static\data\\solution_images\\sid' + str(new_row.id))
        except FileExistsError:
            print("directory already exists")
        step_count = 1
        for step in request.form:
            image_file_names = []
            if step[:4] == 'step':
                # try:
                #     os.mkdir('\\documentation_system\\static\data\\solution_images\\sid' + str(new_row.id) + '\\step' + str(step_count))
                # except FileExistsError:
                #     print("directory already exists")
                for i in images:
                    print(i)
                    if i[5:] == step[4:]:
                        # images = request.files[i]
                        step_images = request.files.getlist(i)
                        for se in step_images:
                            if se.filename:
                                try:
                                    se.save(se.filename)
                                    shutil.move('\\documentation_system\\' + se.filename,
                                                # '\\documentation_system\\static\data\\solution_images\\sid' + str(new_row.id) + '\\step' + str(step_count))
                                                '\\documentation_system\\static\data\\solution_images'
                                                '\\sid' + str(new_row.id))
                                except:
                                    print('There was an error')
                                image_file_names.append(se.filename)
                step_info = {
                    "Instruction": data[step],
                    "Images": image_file_names
                }
                all_step_info[str(step_count)] = step_info
                step_count += 1
        print(all_step_info)
        if 'solution_title' in data:
            title = data['solution_title']
        else:
            title = ''
        if 'asset_type' in data:
            asset_type = int(data['asset_type'])
        else:
            asset_type = None
        if 'public_solution' in data:
            ps = True
        else:
            ps = False
        s = models.Solutions
        db_connect.update_column(model=s, id=new_row.id, column=s.solution_title, v=title)
        db_connect.update_column(model=s, id=new_row.id, column=s.steps, v=all_step_info)
        db_connect.update_column(model=s, id=new_row.id, column=s.date_added, v=datetime.datetime.now())
        db_connect.update_column(model=s, id=new_row.id, column=s.date_revised, v=datetime.datetime.now())
        db_connect.update_column(model=s, id=new_row.id, column=s.primary_asset_type, v=asset_type)
        db_connect.update_column(model=s, id=new_row.id, column=s.associated_asset_types, v=[asset_type])
        db_connect.update_column(model=s, id=new_row.id, column=s.user, v=1)
        db_connect.update_column(model=s, id=new_row.id, column=s.public, v=ps)

        return redirect(url_for('view_one_solution', solution_id=new_row.id))


# TODO: This will need completely reworked to be able to save images
# TODO: and not have to be used with an AJAX request but just a straight form
@app.route('/add_solution_post_old', methods=['GET', 'POST'])
def add_solution_post_old():
    data = request.form
    combined_steps = {}
    temp_dict = {}
    count = 1

    asset_type = db_connect.query_one_db(model=models.AssetTypes,
                                         column=models.AssetTypes.id,
                                         v=data['asset_type'])

    solution = data['solution'].split('&')
    for s in solution:
        print(s)
        if s[:4] == 'step':
            step = s.replace("%20", " ")
            instructions = step.split('=')[1]
            images = []  # This should be a list of strings that will be file paths to the solution step's images
            # temp_dict[str(count)] = step.split('=')[1]
            print(s.split('=')[0] + ' - ' + s.split('=')[1])
            # Code to test adding images
            step_info = {
                "Instruction": instructions,
                "Images": images
            }
            temp_dict[str(count)] = step_info
            count += 1
        if 'solution_title' in s:
            title = s.split('=')[1]
            title = title.replace("%20", " ")
        if 'public_solution' in s:
            public = True
        else:
            public = False
    for i in temp_dict:
        print(i, temp_dict[i])
    print(asset_type)
    print(type(asset_type))
    db_connect.insert_db(models.Solutions(solution_title=title,
                                          steps=temp_dict,
                                          date_added=datetime.datetime.now(),
                                          date_revised=datetime.datetime.now(),
                                          primary_asset_type=asset_type.id,
                                          associated_asset_types=[asset_type.id],
                                          user=1,
                                          public=public))

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
