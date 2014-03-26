from flask import render_template
from app import app, comm, forms

@app.route('/')
@app.route('/index')
def index():
    c = comm.MaremComm()
    state = c.get_state()
    c.close()
    f = forms.MaremForm(data=state)
    return render_template("index.html",
            state=state,
            form=f,
            title="Home")

