from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import send_from_directory
from flask import session
from werkzeug.utils import secure_filename
from flask import Flask

# import object holding app-specific configuration
from config import Config

# import the specification of forms used, to be included in rendered templates

from forms import ResponseForm
from forms import UploadForm

# Recognizer wraps AI model (CNN)
from recognizer import Recognizer

# import fastai modules
import fastai
import fastai.vision
import fastai.metrics
import fastai.basic_train

import torch


import os
import base64


# from app import app

app = Flask(__name__)
app.config.from_object(Config)


# home page
@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


# end index


ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])


def allowed_extension(filename):
    '''
    checks a filename for having an extension in the allowed list.
    Allowed list is held in ALLOWED_EXTENSIONS
    '''
    return ('.' in filename) and (
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# end allowed_file


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            file = form.photo.data
            if not allowed_extension(file.filename):
                #  File must be a jpg, etc
                exts = ""
                flash(
                    'File name must end in one of: '
                    + ', '.join(ALLOWED_EXTENSIONS)
                    + '. You entered:  '
                    + file.filename
                )
                return redirect(request.url)
            else:
                filename = secure_filename(file.filename)

                # if needed, initialize upload count, else bump count
                if 'upload_count' in session:
                    session['upload_count'] = session['upload_count'] + 1
                else:
                    session['upload_count'] = 1
                # end if

                # report upload success to user, showing file name
                flash('Loading ... ' + filename)
                flash('Saving to ' + app.config['UPLOAD_FOLDER'] + '...')
                filename = file.filename
                file.save(
                    os.path.join(
                        app.instance_path, app.config['UPLOAD_FOLDER'], filename
                    )
                )
                flash('Saved to ' + app.config['UPLOAD_FOLDER'])

                #  run CNN on image
                my_cnn = Recognizer()

                model_path = os.path.join(app.instance_path, app.config['MODEL_FOLDER'])
                image_path = os.path.join(
                    app.instance_path, app.config['UPLOAD_FOLDER'], filename
                )
                guesses = my_cnn.recognize(model_path, image_path)

                flash('Processing complete ...')

                image_path = os.path.join(
                    app.instance_path, app.config['UPLOAD_FOLDER'], filename
                )

                # read the image into a base64 encoded string, for later display to user
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = encoded_string.decode('utf-8')
                # end with

                # remove the file, having performed guess process
                try:
                    os.remove(image_path)
                    flash('File cleanup OK.')
                except OSError:
                    flash('File cleanup: error seen !')
                # end try
                flash('File cleanup ended.')

                # Display result to user
                #  Show uploaded image, followed by identification guesses

                # get file extension, to include in HTML response
                image_type = filename.rsplit('.', 1)[1].lower()
                # b64 is the src value for the <img> tag in response page
                b64 = "data:image/" + image_type + ";base64," + encoded_string

                form = ResponseForm()
                return render_template(
                    'ack_upload.html',
                    form=form,
                    filename=filename,
                    uploadcount=str(session['upload_count']),
                    guesses=guesses,
                    image64=b64,
                )
            # end if
        # end if
    # end if
    return render_template('upload.html', title='Upload File', form=form)


# end upload_file


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.instance_path, app.config['UPLOAD_FOLDER']), filename
    )


# end uploaded_file

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
#end if


