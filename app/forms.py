from flask.ext.wtf import Form
from wtforms import DecimalField, SelectField
from wtforms.validators import Required
from app.comm import MaremComm

class MaremForm(Form):
    #Note that the field names must match the get_state() keys in comm.py
    volume = DecimalField('volume', validators=[Required()], places=1)
    speakers = SelectField('speakers', choices=MaremComm.speakers)
    surround_mode = SelectField('surround mode',
            choices=[(x, x.capitalize()) for x in MaremComm.surround_modes])
    source = SelectField('source', choices=MaremComm.sources)
