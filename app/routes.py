import os
from flask import render_template, url_for, redirect, session, Markup
from werkzeug.utils import secure_filename
from app.models import Script, LocationInformation
from app import app, db
from app.forms import ScriptForm
from Script_reader import table_creator


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = ScriptForm()
    if form.validate_on_submit():
        f = form.script.data
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.instance_path, 'scripts', filename)
        f.save(os.path.join(app.instance_path, 'scripts', filename))
        script_name = file_path.split('/')[-1]
        s = Script(name=script_name)
        db.session.add(s)
        db.session.commit()
        session['file_path'] = file_path
        session['script_id'] = Script.query.order_by(Script.uploaded_at.desc()).first().id
        return redirect(url_for('locations'))
    return render_template('index.html', title='Home', form=form)


@app.route('/locations', methods=['POST', 'GET'])
def locations():
    script_id = session['script_id']
    s_id = Script.query.filter(Script.id == script_id).first()
    s_id = s_id.id
    file_path = session['file_path']
    table_as_html = Markup(table_creator(file_path, db, s_id).get_html_string())
    os.remove(file_path)
    return render_template('locations.html', data=table_as_html, title='Locations')

#Perhaps use http://flask.pocoo.org/docs/0.12/api/#flask.send_from_directory to allow a CSV to be downloaded.
