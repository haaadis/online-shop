from flask import *
from flask_wtf import *
from wtforms import *
from werkzeug.utils import *
import os
from wtforms.validators import InputRequired
import sqlite3

app = Flask(__name__ ,template_folder='template')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD-FOLDER']='static/files'

class UploadFileForm(FlaskForm):
    file = FileField('file', validators=[InputRequired()])
    submit = SubmitField('Upload File')

def connect():
    sql = sqlite3.connect('products.db')
    sql.row_factory = sqlite3.Row
    return sql

def database():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect()
    return g.sqlite_db

@app.route('/', methods=['GET','POST'])
@app.route('/add', methods=['GET','POST'])
def add():
    db = database()
    form = UploadFileForm()
    if  request.method=='POST':
       
        product_id=request.form['productId']
        product_name = request.form['name']
        product_size= request.form['size']
        product_color=request.form['color']
        product_price=request.form['price']
        quantity=request.form['quantity']
        category=request.form['category']
        db.execute('insert into ware (product_id, product_name, product_size,product_color,product_price,quantity,category) values (?,?,?,?,?,?,?)',[category,product_id, product_name,product_size,quantity,product_color,product_price])
        db.commit()
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD-FOLDER'],secure_filename(file.filename)))
        
    return render_template('add.html', form=form)
    
    


if __name__ == '__main__':
    app.run(debug=True)

