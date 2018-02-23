import os
from flask import render_template, url_for, redirect
from werkzeug.utils import secure_filename

from app import app
from app.forms import ScriptForm
from Script_reader import locations_emailer


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = ScriptForm()
    if form.validate_on_submit():
        print(form.script.data)
        f = form.script.data
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.instance_path, 'scripts', filename)
        print(file_path)
        f.save(os.path.join(app.instance_path, 'scripts', filename))
        locations_emailer(file_path, form.email_address.data)
        os.remove(file_path)
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)
