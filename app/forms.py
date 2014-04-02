from flask.ext.wtf import Form
from wtforms import DecimalField, SelectField
from wtforms.validators import Required
from wtforms.widgets import TextInput, HTMLString
from app.comm import MaremComm

class VolumeInput(TextInput):
    def __call__(self, field, **kwargs):
        if hasattr(kwargs, 'style'):
            kwargs['style'] = kwargs['style'] + ' width:50%; display:inline-block'
        else :
            kwargs['style'] = 'width:50%; display:inline-block'
        html = super(VolumeInput, self).__call__(field, **kwargs)
        vol_up = "<button class='form-control btn btn-success' id='%s_up' style='width:25%%' name='%s_up'>+</button>" % (
                field.id, field.id)
        vol_dn = "<button class='form-control btn btn-danger' id='%s_down' style='width:25%%' name='%s_down'>-</button>" % (
                field.id, field.id)
        print "displaying volume widget: " + html + vol_up + vol_dn
        return HTMLString(html + vol_up + vol_dn)


class MaremForm(Form):
    #Note that the field names must match the get_state() keys in comm.py
    volume = DecimalField('Volume (dB)', widget=VolumeInput(), validators=[Required()], places=1)
    speakers = SelectField('Speakers', choices=MaremComm.speakers)
    surround_mode = SelectField('Surround mode',
            choices=MaremComm.surround_modes)
    source = SelectField('Source', choices=MaremComm.sources)
