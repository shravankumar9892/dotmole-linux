from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class ConfigurationForm(FlaskForm):
    name = StringField('Name', render_kw={'placeholder': 'Name'})
    description = StringField('Description', render_kw={'placeholder': 'Description'})
    services = StringField('Services', render_kw={'placeholder': 'Services'})
    build_configuration = SubmitField('Build Configuration', render_kw={'class': 'btn btn-info'})

class LivestreamForm(FlaskForm):
    name = StringField('Name', render_kw={'placeholder': 'Name'})
    internal_ip = StringField('Internal IP', render_kw={'placeholder': 'Internal IP'})
    #configuration_type can be left blank I guess
    configuration_type = SelectField(u'Type', choices=[('default', 'Default'), ('custom', 'Custom')])
    configuration_name = SelectField(u'Name')
    submit = SubmitField('Add', render_kw={'class': 'btn btn-info'})
