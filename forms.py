from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, URL, Length, Optional, email_validator


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for editing your user profile."""

    username = StringField('Username', validators=[Optional()])
    email = StringField('E-mail', validators=[Optional(), Email()])
    image_url = StringField('Image URL', validators=[Optional()])
    header_image_url = StringField('Header Image URL', validators=[Optional()])
    bio = StringField('Bio', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class ChangePasswordForm(FlaskForm):
    """Form for changing password."""

    current_password = PasswordField('Current Password', validators=[Length(min=6)])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    new_password_confirmed = PasswordField('Confirm New Password', validators=[Length(min=6)])