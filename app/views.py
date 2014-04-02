from flask import Flask, jsonify, render_template, request
from app import app, comm, forms

@app.route('/')
@app.route('/index')
def index():
    c = comm.MaremComm()
    state = c.get_state()
    c.close()
    f = forms.MaremForm(**state)
    print("Volume : %s" % f.volume.data)
    return render_template("index.html",
            form=f,
            state=state,
            title="Home")

@app.route('/get_state')
def get_state():
    c = comm.MaremComm()
    state = c.get_state()
    return jsonify(state)

@app.route('/set_state', methods=['POST'])
def set_state():
    ''' Takes a single key:value.  If more are passed, deals with the first one. '''

    print(request.form)
    attr = request.form.keys()[0]
    if attr not in ('speakers', 'volume', 'surround', 'source'):
        raise KeyError('%s is not a valid attr' % attr)

    value = request.form[attr]
    print("Got a request to set %s to %s" % (attr, value))
    #do some error checking here, in case we get a non-int, or an 
    #out of range value

    #Ok, we're good, set up the comm
    c = comm.MaremComm()
    func_name = 'set_%s' % attr
    getattr(c, func_name)(value)
    state = c.get_state()
    return jsonify(state)
