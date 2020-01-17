from flask import (Flask, flash, render_template, redirect, url_for, request, session)
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import exc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime
# import forms
import db_connect
import models
import re

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'nfj2984ijNDUUFH89()&&iJINOkf)(_@KLNFE:!#RefwkFpyio'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main():
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
                           company=company)


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)