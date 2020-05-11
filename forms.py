from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, DecimalField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import (DataRequired, Email,
                                Length, InputRequired)
from wtforms.fields.html5 import DateField


class AddAssetTypeForm(Form):
    asset_type = StringField("Asset Type", validators=[DataRequired()], render_kw={"placeholder": "Asset Type"})
    asset_type_submit = SubmitField("Add Asset Type")


class AddAssetForm(Form):
    asset_type = SelectField(label="Asset Type", validators=[DataRequired()])
    manufacturer = SelectField(validators=[DataRequired()])
    model = StringField("Model Number",  render_kw={"placeholder": "Model Number"})
    serial_no = StringField("Serial Number", render_kw={"placeholder": "Serial Number"})
    dia_asset_tag = StringField("Diamond Asset Tag", render_kw={"placeholder": "Diamond Tag Number"})
    name = StringField("Name", render_kw={"placeholder": "Asset Name"})
    department = SelectField("Department", render_kw={"placeholder": "Department"})
    description = TextAreaField("Description such as: Model number", render_kw={"placeholder": "Description"})
    ip_address = StringField("IP", render_kw={"placeholder": "0.0.0.0"})
    asset_submit = SubmitField('Add Asset')


class EditAssetForm(Form):
    asset_type = SelectField(validators=[DataRequired()])
    manufacturer = SelectField(validators=[DataRequired()])
    model = StringField("Model Number")
    serial_no = StringField("Serial Number")
    dia_asset_tag = StringField("Diamond Asset Tag")
    name = StringField("Name")
    department = SelectField("Department")
    description = TextAreaField("Description such as: Model number")
    ip_address = StringField("IP")
    asset_submit = SubmitField('Add Asset')


class AddManufacturerForm(Form):
    manufacturer = StringField("Add Manufacturer", validators=[DataRequired()], render_kw={"placeholder": "Enter Manufacturer"})
    manufacturer_submit = SubmitField('Add Manufacturer')


class AddDepartmentForm(Form):
    department = StringField(validators=[DataRequired()], render_kw={"placeholder": "Department"})
    department_submit = SubmitField('Add Department')


class AddAssetTypeToSolutionForm(Form):
    asset_types = SelectMultipleField(validators=[DataRequired()])
    solution_id = StringField(validators=[DataRequired()])
    add_submit = SubmitField('Add to Solution')


class AddAssocSolutionForm(Form):
    assoc_solution_id = StringField(validators=[DataRequired()])
    main_solution_id = StringField(validators=[DataRequired()])
    assoc_solution_submit = SubmitField('Add')


class ChangePrimaryAssetTypeForm(Form):
    all_asset_types = SelectField(validators=[DataRequired()])
    change_primary_asset_type_submit = SubmitField('Change')