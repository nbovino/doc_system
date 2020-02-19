from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, DecimalField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Email,
                                Length, InputRequired)
from wtforms.fields.html5 import DateField


class AddAssetTypeForm(Form):
    asset_type = StringField("Asset Type", validators=[DataRequired()], render_kw={"placeholder": "Asset Type"})


class AddAssetForm(Form):
    asset_type = SelectField("Asset Type", validators=[DataRequired()])
    manufacturer = SelectField("Manufacturer", validators=[DataRequired()])
    model = StringField("Model Number")
    serial_no = StringField("Serial Number")
    dia_asset_tag = StringField("Diamond Asset Tag Number")
    name = StringField("Name", render_kw={"placeholder": "Asset Name"})
    department = SelectField("Department")
    description = TextAreaField("Description such as: Model number")
    ip_address = StringField("IP", render_kw={"placeholder": "0.0.0.0"})
    asset_submit = SubmitField('Add Asset')


class AddManufacturerForm(Form):
    manufacturer = StringField("Add Manufacturer", validators=[DataRequired()], render_kw={"placeholder": "Enter Manufacturer"})
    manufacturer_submit = SubmitField('Add Manufacturer')


class AddDepartmentForm(Form):
    department = StringField(validators=[DataRequired()], render_kw={"placeholder": "Department"})
    department_submit = SubmitField('Add Department')
