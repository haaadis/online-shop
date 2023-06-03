from flask import *
from flask_wtf import *
from wtforms import *
from werkzeug.utils import *
import os

app = Flask(__name__ ,template_folder='template')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD-FOLDER']='static/files'

class UploadFileForm(FlaskForm):
    file = FileField('file')
    submit = SubmitField('Upload File')

@app.route('/', methods=['GET','POST'])
@app.route('/add', methods=['GET','POST'])
def add():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD-FOLDER'],secure_filename(file.filename)))
        return 'file has been uploaded'
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
