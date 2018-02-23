from flask import render_template, url_for, redirect
from app import app
from app.forms import ScriptForm
from Script_reader import *


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = ScriptForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)
