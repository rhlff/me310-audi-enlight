from flask import Flask, render_template, request, g

app = Flask(__name__)

def get_settings():
    settings = getattr(g, '_settings', None)
    if settings is None:
        settings = g._settings = [
        { 'name': 'Working Light', 'url': 'working_light', 'activated': True },
        { 'name': 'Beat Detection', 'url': None, 'activated': False },
    ]
    return settings

@app.route('/')
def dashboard():
    return render_template('dashboard.html', settings=get_settings())

@app.route('/toggle', methods=['POST'])
def toggle_settings():
    print "Set", request.form['name'], "to", request.form['activate']
    return ('', 204)

@app.route('/working-light')
def working_light():
    return render_template('working_light.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
