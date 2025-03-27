import re
from flask import Flask, render_template, request, make_response
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
application = app

@app.before_request
def fix_script_name():
    if 'SCRIPT_NAME' in app.config:
        app.wsgi_app = DispatcherMiddleware(None, {app.config['SCRIPT_NAME']: app.wsgi_app})

app.config["SERVER_NAME"] = 'vintage150.pythonanywhere.com' 
app.config['SCRIPT_NAME'] = '/lab2'
app.config['APPLICATION_ROOT'] = '/lab2'

@app.route('/')
def index():
    msg = request.url
    return render_template('base.html', msg=msg)

@app.route('/params')
def params(): 
    return render_template('params.html')

@app.route('/headers')
def headers(): 
    return render_template('headers.html', headers=request.headers)

@app.route('/cookies')
def cookies(): 
    resp = make_response(render_template('cookies.html'))
    if 'name' not in request.cookies:
        resp.set_cookie('name', 'Same')
    else:
        resp.set_cookie('name', expires=0)
    return resp

@app.route('/form', methods=['GET', 'POST'])
def form(): 
    return render_template('form.html')

def format_phone_number(phone):
    digits = re.sub(r'\D', '', phone)  
    if len(digits) == 11 and (digits.startswith('7') or digits.startswith('8')):
        digits = '8' + digits[1:]
    elif len(digits) == 10:
        digits = '8' + digits
    return f"{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"


@app.route("/phone", methods=["GET", "POST"])
def phone_form():
    error = None
    formatted_number = None
    
    if request.method == "POST":
        phone = request.form.get("phone", "")
        digits = re.sub(r'\D', '', phone)  
        
        if not re.match(r'^[\d+().\s-]+$', phone):
            error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
        elif not (len(digits) == 11 and (digits.startswith("7") or digits.startswith("8")) or len(digits) == 10):
            error = "Недопустимый ввод. Неверное количество цифр."
        else:
            formatted_number = format_phone_number(phone)
    
    return render_template("phone_form.html", error=error, formatted_number=formatted_number)