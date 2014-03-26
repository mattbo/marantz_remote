from flask import Flask, jsonify, render_template, request
from app import app, comm, forms

@app.route('/')
@app.route('/index')
def index():
    c = comm.MaremComm()
    state = c.get_state()
    c.close()
    f = forms.MaremForm(request.form, **state)
    print("Volume : %s" % f.volume.data)
    return render_template("index.html",
            state=state,
            form=f,
            title="Home")

@app.route('/get_state')
def get_state():
    #state = Marem().get_state()
    state = {
        'speakers': 'a+b',
        'volume': -22,
        'surround': 'Dolby DTS',
        'source': 'SAT'}
    return jsonify(state)

@app.route('/set', methods=['POST'])
def set_state():

    attr = request.form['attr']
    if attr not in ('speakers', 'volume', 'surround', 'source'):
        raise KeyError('%s is not a valid attr' % attr)

    value = request.form['value']
    #do some error checking here, in case we get a non-int, or an 
    #out of range value

    #Marem.set_volume(volume)

    #Gather a fresh snapshot of the state each time, in case someone 
    #is playing with the remote
    #state = Marem().get_state

    #Fake
    state = {
        'speakers': 'a+b',
        'volume': volume,
        'surround': 'Dolby DTS',
        'source': 'SAT'}
    state[attr] = value

    return jsonify(state)
