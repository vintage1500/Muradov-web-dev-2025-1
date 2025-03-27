from flask import Flask, render_template

app = Flask(__name__)

app.config["SERVER_NAME"] = 'vintage150.pythonanywhere.com' 
app.config['SCRIPT_NAME'] = '/root_app'

@app.route('/')
def index():
    return render_template('index.html')