from app import db
import datetime


class LocationInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scene_number = db.Column(db.String(length=10))
    int_or_ext = db.Column(db.String(length=8))
    location_type = db.Column(db.String())
    time_of_day = db.Column(db.String(length=20))
    script_id = db.Column(db.Integer, db.ForeignKey('scripts.id'))


class Script(db.Model):
    __tablename__ = 'scripts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    uploaded_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow())