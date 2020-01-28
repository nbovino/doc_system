from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, DecimalField, BooleanField
from wtforms.validators import (DataRequired, Email,
                                Length, InputRequired)
from wtforms.fields.html5 import DateField


class addAssetTypeForm(Form):
    asset_type = StringField("Asset Type", validators=[DataRequired()], render_kw={"placeholder": "Asset Type"})


class addAssetForm(Form):
    asset_type = SelectField("Asset Type", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Asset Name"})
    description = TextAreaField("Description such as: Location, model number")
    ip_address = StringField("IP", render_kw={"placeholder": "0.0.0.0"})
