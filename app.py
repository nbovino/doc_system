from flask import (Flask, flash, render_template, redirect, url_for, request, session, jsonify, json)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import exc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    return render_template('view_solution.html',
                           solution_category=solution_category,
                           company=company,
                           asset_types=all_asset_types)


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
    return render_template('add_solution.html',
                           message=message,
                           asset_types=db_connect.query_all(models.AssetTypes))


@app.route('/add_solution_post', methods=['GET', 'POST'])
def add_solution_post():
    # return render_template('add_solution.html', combined=combined_steps)
    data = request.form
    # print(request.form)
    combined_steps = {}
    temp_dict = {}
    count = 1
    for v in data.keys():
        temp_dict[str(count)] = data[v]
        count += 1
        # print(v + " - " + data[v])

    combined_steps['Steps'] = temp_dict
    print(combined_steps)
    # if request.method == 'GET':
    #     return jsonify(combined_steps)
    return combined_steps


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
