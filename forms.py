from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired

#  not used for now
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Sign In')


# end LoginForm

# A form that tells the user something, allows them to read it, and continue on
class ResponseForm(FlaskForm):
    submit = SubmitField('Continue')


# end ResponseForm

# A form to upload a jpg image
class UploadForm(FlaskForm):

    # note that width has to be large, for long file paths to be displayed gracefully
    photo = FileField(validators=[FileRequired()], render_kw={'style': 'width: 90%'})

    submit = SubmitField('Upload File')


# end UploadForm

