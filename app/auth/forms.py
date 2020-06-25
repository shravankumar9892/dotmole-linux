from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), render_kw={'class':'form-control', 'placeholder': 'Email', 'type': 'email'}, validators=[DataRequired()])
    password = PasswordField(_l('Password'), render_kw={'class':'form-control', 'placeholder': 'Password', 'type': 'password'}, validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'), render_kw={'id': 'remember', 'type': 'checkbox'})
    submit = SubmitField('Sign In', render_kw={'class': 'btn btn-primary btn-block'})


class RegistrationForm(FlaskForm):
    full_name = StringField(_l('Full name'), render_kw={'class': 'form-control', 'placeholder': 'Full name', 'type': 'text'}, validators=[DataRequired()])
    email = StringField(_l('Email'), render_kw={'class':'form-control', 'placeholder': 'Email', 'type': 'email'}, validators=[DataRequired()])
    password = PasswordField(_l('Password'), render_kw={'class':'form-control', 'placeholder': 'Password', 'type': 'password'}, validators=[DataRequired()])
    retype_password = PasswordField(_l('Retype password'), render_kw={'class': 'form-control', 'placeholder': 'Retype password', 'type': 'password'}, validators=[DataRequired(), EqualTo('password')])
    agree_terms = BooleanField(_l('I agree to the terms'), render_kw={'id': 'remember', 'type': 'checkbox'}, validators=[DataRequired()])
    register = SubmitField('Register', render_kw={'class': 'btn btn-primary btn-block'})

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


'''
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))'''


## To reset password - Later functionality
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))