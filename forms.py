from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])

class AddFolderForm(FlaskForm):
    folder_name = StringField('Name', validators=[InputRequired(), Length(min = 1, max = 100)])
    folder_parent_folder = SelectField('Parent folder')

class UpdateFolderForm(FlaskForm):
    folder_name_update = StringField('Name', validators=[InputRequired(), Length(min = 1, max = 100)])
    folder_parent_folder_update = SelectField('Parent folder')
    folder_id_update = HiddenField()

class DeleteFolderForm(FlaskForm):
    folder_id = HiddenField()

class AddBookmarkForm(FlaskForm):
    bookmark_name = StringField('Name', validators=[InputRequired(), Length(min = 1, max = 100)])
    bookmark_parent_folder = SelectField('Parent folder')
    link = StringField('Link', validators=[InputRequired()])
    description = StringField('Description')

class UpdateBookmarkForm(FlaskForm):
    bookmark_name_update = StringField('Name', validators=[InputRequired(), Length(min = 1, max = 100)])
    bookmark_parent_folder_update = SelectField('Parent folder')
    link_update = StringField('Link', validators=[InputRequired()])
    description_update = StringField('Description')
    bookmark_id_update = HiddenField()

class DeleteBookmarkForm(FlaskForm):
    bookmark_id = HiddenField()

class SearchForm(FlaskForm):
    search_term = StringField('',validators=[InputRequired()],render_kw={"placeholder": "Search"})