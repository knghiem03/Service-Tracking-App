"""Server for Clients tracking app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify, url_for)
from flask.wrappers import Response
from model import Client, connect_to_db
from datetime import datetime, date, tzinfo
import crud
from jinja2 import StrictUndefined
from authlib.integrations.flask_client import OAuth
# decorator for routes that should be accessible only by logged in users
# from auth_decorator import login_required
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

# Replace this with routes and view functions!
@app.route('/')
def create_homepage():
    profile = 'profile'
    if profile in session:
        email = dict(session)['profile']['email']
        flash(f'Welcome {email}. You are now logged in','infor')
    else:
        flash("Please login in to use the app",'infor')
    return render_template('index.html')

@app.route('/show_search_box')  
def show_search_box():
    print(session.keys())
    if 'email' not in session.keys():
        return redirect('/')
    return render_template("show_client_search.html")
    
@app.route('/searchDb')  
def show_search_person_result():
    response = []
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    client_search_result = crud.get_client_by_name(fname,lname)
    # print(f'******{client_search_result}*****************')
    for person in client_search_result:
        response.append({"fname" : person.fname, 
                         "lname" : person.lname,
                         "client_id" : person.client_id})
    return jsonify(response)
    
@app.route('/loadClient/<int:id>')
def load_a_client(id):
    print(id)
    session['sv_st'] = datetime.now()
    session['sv_bt'] = datetime.now()
    session['client_id'] = id
    client_tb_as_dict = {}
    # Can't return a database record or row here. Need to make a dictinary with client table field as Key ???
    record = crud.get_client_by_id(id)
    client_tb_as_dict['fname']   = record.fname
    client_tb_as_dict['lname']   = record.lname
    client_tb_as_dict['mname']   = record.mname
    client_tb_as_dict['address'] = record.address
    client_tb_as_dict['city']    = record.city
    client_tb_as_dict['state']   = record.state
    client_tb_as_dict['zip']     = record.zip
    client_tb_as_dict['county']  = record.county
    client_tb_as_dict['lang']    = record.lang
    client_tb_as_dict['dob']     = record.dob
    client_tb_as_dict['phone']   = record.phone
    print(client_tb_as_dict)
    return render_template("ajax_client_intake.html", client=record)

@app.route('/client_page')
def show_client_intake_page():
    if 'email' not in session.keys():
        return redirect('/')
    session['sv_bt'] = datetime.now().replace(tzinfo=None)
    return render_template("ajax_client_intake.html", client=None) 


@app.route('/addClientToDb')  
def add_a_client():
    # Remember to pass this to the service table too !!!!
    response = []
    # session['sv_bt'] = datetime.now()

    fname   = request.args.get('fname')
    lname   = request.args.get('lname')
    mname   = request.args.get('mname')
    dob     = request.args.get('dob')
    phone   = request.args.get('phone')
    address = request.args.get('address')
    city    = request.args.get('city')
    state   = request.args.get('state')
    zip     = request.args.get('zip')
    county  = request.args.get('county')
    lang    = request.args.get('lang')
    # Use auto generate today to keep track of date this client is added to DB
    #r_date  = request.args.get('r_date')
    r_date = date.today()

    client = crud.create_client(fname=fname,lname=lname,address=address,city=city,
                       state=state,zip=zip,county=county,lang=lang,mname=mname,dob=dob,phone=phone,r_date=r_date)

    # Use session pass client_id and service start time to service record row 
    session['client_id'] = client.client_id
    return jsonify(fname=fname,lname=lname,address=address,city=city,
                   state=state,zip=zip,county=county,lang=lang,mname=mname,dob=dob,phone=phone,r_date=r_date)

@app.route("/recordService")
def record_service():
    # This route save one service record to the services table
    client_id  = session['client_id']
    program_id = int(request.args.get("service_radio"))
    sv_note    = request.args.get('message')
    sv_date    = date.today()
    sv_bt      = session['sv_bt'].replace(tzinfo=None)
    sv_et      = datetime.now().replace(tzinfo=None)
    # get the duration in seconds, convert to minutes and round up to the next 15 minutes
    service_dur = (sv_et - sv_bt).total_seconds() // 60
    service_dur = service_dur - (service_dur % 15) + 15 
    service = crud.record_service(client_id, program_id, sv_note, sv_date, sv_bt, sv_et, service_dur)
    return jsonify(client_id=client_id, program_id=program_id,sv_note=sv_note,
                    sv_date=sv_date,sv_bt=sv_bt,service_dur=service_dur)

@app.route('/query')
def show_query_page():
    if 'email' not in session.keys():
        return redirect('/')
    return render_template('query_page.html', response=None)

@app.route('/run_query/<int:query_id>')
def run_query(query_id):
    if 'email' not in session.keys():
        return redirect('/')
    response = []
    title ="Client list"
    # query_id = int(request.args.get("query_option"))
    session['query_option'] = query_id

    if query_id == 1:
        title = f"Second Harvest Clients"
    elif query_id == 2:
        title = f"Elders Program Clients"
    elif query_id == 3:
        title = f"Health Care Clients"
    else:
        pass 
    records = crud.get_client_name_phone_by_program(query_id)  
    
    # for rec in records:
    #     response.append({"fname"     : rec.fname, 
    #                     "lname"      : rec.lname,
    #                     "phone"      : rec.phone,
    #                     "dob"        : rec.dob.strftime("%m/%d/%Y"),
    #                     "program_id" : rec.program_id})
    # Write DB results to user's local drive in CSV format    
    crud.write_client_info_to_cvs_file_with_pro_id(records) 

    # This query render a Jinja template to display BootStrap table, Can't use Ajax here
    return render_template('query_result.html', response=records,title=title)

@app.route('/spl_query')
def show_spl_query_page():
    return render_template('query_page.html', response=None)

@app.route('/last_month_hours')
def last_month_hours():
    if 'email' not in session.keys():
        return redirect('/')
    result = crud.get_client_hours_served_last_month()
    return render_template('last_month_hours.html', response=result)

@app.route('/last_quarter_hours')
def last_quarter_hours():
    if 'email' not in session.keys():
        return redirect('/')
    result = crud.get_client_hours_served_last_quarter()
    return render_template('last_month_hours.html', response=result)

@app.route('/other_options')
def other_options():
    if 'email' not in session.keys():
        return redirect('/')
    # records = crud.get_client_hours_served_last_quarter()
    return render_template('special_query.html', response=None)

@app.route('/run_spl_query')
def run_spl_query():
    response = []
    query_id = int(request.args.get("query_option"))
    session['query_option'] = query_id
    if query_id == 4:
        records = crud.get_client_name_phone_by_age(60)
    elif query_id == 5:
        records = crud.get_client_hours_served_last_month()
        response.append({"total": records[0][0]})
    elif query_id == 6:
        records = crud.get_client_hours_served_last_quarter()
        response.append({"total": records[0][0]})
    else:
        records = crud.get_client_name_phone_by_program(query_id)  
    if query_id in [1,2,3,4]:
        for rec in records:
            response.append({"fname"     : rec.fname, 
                            "lname"      : rec.lname,
                            "phone"      : rec.phone,
                            "dob"        : rec.dob.strftime("%m/%d/%Y"),
                            "program_id" : rec.program_id })
    # This query render a Jinja template to display BootStrap table, Can't use Ajax here
    return render_template('query_page.html', response=records)

@app.route('/run_spl_query_1')
def run_spl_query_1():
    response = []
    query_id = request.args.get("query_option")
    user_input = request.args.get("user_input")
    session['query_option'] = query_id
    title = "Welcome"
    if query_id == "age":
        title = f'Clients who are {user_input} or older'
        records = crud.get_client_by_age(int(user_input))
    elif query_id == "city":
        title = f'Clients who reside in {user_input}'
        records = crud.get_client_by_city(user_input)
    elif query_id == "zip":
        title = f'Clients with {user_input} zipcode'
        records = crud.get_client_by_zipcode(int(user_input)) 
    elif query_id == "county":
        title = f'Clients who reside in {user_input} county'
        records = crud.get_client_by_county(user_input) 
    elif query_id == "lang":
        title = f'Clients who speak {user_input}'
        records = crud.get_client_by_lang(user_input)
    else:
        records = crud.get_client_name_phone_by_program(query_id)

    # Write DB results to user's local drive in CSV format    
    crud.write_client_info_to_cvs_file(records, query_id)
    # This query render a Jinja template to display BootStrap table, Can't use Ajax here
    return render_template('special_query.html', response=records,title=title)

@app.route('/one_sms_page')
def one_sms_page():
    if 'email' not in session.keys():
        return redirect('/')
    return render_template('one_sms.html')

@app.route('/one_sms')
def send_one_sms():
    phones = [request.args.get("phone")]
    msg = request.args.get("message")
    # need to make a dictionary and pass it to JS ???
    return crud.text_client(phones, msg)

@app.route('/many_sms_page')
def many_sms_page():
    if 'email' not in session.keys():
        return redirect('/')
    return render_template('many_sms.html',response=None)
    
@app.route('/run_sms_query')
def run_sms_query():
    response = []
    query_id = int(request.args.get("query_option"))
    session['query_option'] = query_id
    if query_id == 4:
        title = f"All clients who are 60 or over"
        # records = crud.get_client_name_phone_by_age(60)
        records = crud.get_client_by_age(60)
    else:
        records = crud.get_client_name_phone_by_program(query_id) 

    if query_id == 1:
        title = f"All clients enrolled in Second Harvest Program"
    elif query_id == 2:
        title = f"All clients who are in Elders Program"
    elif query_id == 3:
        title = f"All clients who received assistance in health care program"
    else:
        pass 
    return render_template('many_sms.html', response=records,title=title)
    
@app.route('/send_query_sms')
def run_query_sms():
    response = []
    phones = []
    
    # Can't use next line, it is not available at the moment
    # The form that uses this route doesn't know about query_option
    # query_id = int(request.args.get("query_option"))

    query_id = session['query_option']
    print(f'*****{query_id}******')
    msg = request.args.get("message")

    if query_id == 4:
        print("List all clients who are 60+")
        records = crud.get_client_name_phone_by_age(60)
    else:
        records = crud.get_client_name_phone_by_program(query_id)
    for rec in records:
        response.append({"fname"      : rec.fname, 
                         "lname"      : rec.lname,
                         "phone"      : rec.phone,
                         "dob"        : rec.dob.strftime("%m/%d/%Y"),
                         "program_id" : rec.program_id })
        # Assemble phone list to pass to Twilio
        phones.append(rec.phone)
    crud.text_client(phones,msg)
    return jsonify(response)

@app.route('/users')
def show_users():
    users = crud.list_all_users()
    return render_template('all_users.html', users=users)

@app.route('/showLogin')
def show_login_page():
    return render_template('login.html')

@app.route('/users', methods= ["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    db_email = crud.get_user_by_email(email)
    if db_email:
        flash(f"{email} is already registered. Please try a different email",'infor')
        return redirect('/showLogin')
    else:
        user = crud.create_user(email, password)         
        flash("Your login ID was successfully created and you can now log in", 'infor')
        return redirect('/')

@app.route('/login', methods= ["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    print(f'***{email} {password}')
    db_login = crud.validate_login(email, password)
    if db_login:
        session['email'] = email
        flash(f"Welcome, {email}",'infor')
        return redirect('/show_search_box')
    else:       
        flash("The email and password don't match",'infor')
        return redirect('/showLogin')

# @app.route('/logout')
# def logout():
#     """ logout the user """
    
#     session.pop("email")
#     return redirect('/')

@app.route('/login_gg')
def login_gg():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  
    # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session['email'] = session['profile']['email']
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # user = dict(session).get('profile', None)
        user = session.get('email', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return redirect('/')
    return decorated_function

@app.route('/logout')
@login_required
def logout():
    # For regular login session
    if session.get('email'):
        session.pop("email")
    # For Google login session, profile is a key
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    