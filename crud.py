""" To create function for CRUD operations """
from datetime import datetime, date, timedelta
from types import MemberDescriptorType
from model import db, Client, Program, Service, User, connect_to_db
from sqlalchemy.sql import func
import sms, csv
from math import ceil

def create_client(fname,lname,address,city,state,zip,county,lang,r_date, mname='',dob='',phone=''):
    """ function to add new client to the clients table
        inputs: First name
                Last name
                Middle name
                Date of birth
                Phone number
                Address: house number, street and unit
                City
                State
                Zip code
                County
                Language spoken
                Date this client is added to database """

    client = Client(fname  = fname,     lname  = lname,  address = address,
                    city   = city,      state  = state,  zip     = zip,
                    county = county,    lang   = lang,   r_date  = r_date,
                    mname   = mname,    dob    = dob,    phone   = phone )
    db.session.add(client)
    db.session.commit()
    return client

def create_program(code, overview):
    """ function to create a new program
        inputs: code, overview            """

    program = Program(code=code, overview=overview ) 

    db.session.add(program)
    db.session.commit()

    return program

def create_user(email, password):
    """ function to create a new user for login registration purpose
        inputs: email, password            """

    user = User(email=email, password=password) 

    db.session.add(user)
    db.session.commit()

    return user

def record_service(client, program, sv_note, sv_date, sv_bt, sv_et, service_dur): 
    
    """ function to create and return a new service """

    service  = Service(client_id  = client,
                       program_id = program,
                       sv_note = sv_note,
                       sv_date = sv_date,
                       sv_bt   = sv_bt,
                       sv_et   = sv_et,
                       service_dur = service_dur ) 
    
    db.session.add(service)
    db.session.commit()
    return 

def get_program_by_id(program_id):  
    return Program.query.get(program_id)

def get_client_count_by_name(fname,lname):
    return Client.query.filter(Client.fname==fname, Client.lname==lname).count()

def get_client_by_name(fname,lname):
    return Client.query.filter(Client.fname==fname, Client.lname==lname).all()  

def get_client_by_city(city):
    return Client.query.filter(Client.city==city).all()  

def get_client_by_county(county):
    return Client.query.filter(Client.county==county).all()     

def get_client_by_zipcode(zipcode):
    return Client.query.filter(Client.zip==zipcode).all()

def get_client_by_lang(lang):
    return Client.query.filter(Client.lang==lang).all()

def get_client_by_id(client_id):
    return Client.query.filter(Client.client_id == client_id).first()

def get_client_name_by_program(program_id):
    return db.session.query(Client.fname).join(Service).filter(Service.program_id==program_id).all()

def get_client_name_phone_by_program(program_id):
    result = db.session.query(Client.fname, Client.lname, Client.phone, Client.dob, Service.program_id).join(Service).filter(Service.program_id==program_id).all()
    return result

def get_client_name_phone_by_age(age):
    """ Turn the age into a Date object that is --age year ago-- , then use that Date object to query the DB """

    today = date.today()
    today_year = today.year
    today.replace(year=today_year - age)
    birth_date =  today.replace(year=today_year - age) # age years ago 
    print(f"Birth year is {birth_date}")
    clients = db.session.query(Client.fname, Client.lname, Client.phone, Client.dob, Client.client_id, Service.program_id).join(Service).filter(Client.dob <= birth_date).all()
    return clients

def get_client_by_age(age):
    """ List all clients who are at least ** age ** year old today """

    today = date.today()
    today_year = today.year
    birth_date = today.replace(year=today_year - age)  # DATE age years ago 
    print(f"Birth year is {birth_date}")
    return Client.query.filter(Client.dob <= birth_date).all()

def create_user(email, password):
    """ function to add new user to users table
        inputs: user's email and password        """

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def list_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()
    
def validate_login(email,password):
    return User.query.filter(User.email == email, User.password == password).first()

def text_client(phone_list, body):
    #return sms.init_sms(phone_list, body) 
    return sms.mock_init_sms(phone_list, body)

def get_client_hours_served_last_month():

    results = []
    lday_preMonth = date.today().replace(day=1) - timedelta(days=1)
    fday_preMonth = date.today().replace(day=1) - timedelta(days=lday_preMonth.day)
    dates = f"From {fday_preMonth} to {lday_preMonth}"
    print("First day of prev month:", fday_preMonth)
    print("Last day of prev month:", lday_preMonth)

    q = db.session.query(func.sum(Service.service_dur))
    names = ["All programs", "Second Harvest Program", "Elder Program", "MNSure Program"]
    services = q.filter(Service.sv_date >= fday_preMonth, Service.sv_date <= lday_preMonth).all()
    if services[0][0] == None:
            service_minutes = 0 
            service_unit    = 0   
    else:
        service_minutes = services[0][0]
        service_units = ceil(services[0][0] / 15 )
    results.append([names[0], service_minutes, service_units])

    for id in [1,2,3]:
        services = q.filter(Service.sv_date >= fday_preMonth, Service.sv_date <= lday_preMonth,
                                Service.program_id == id).all()     
        if services[0][0] == None:
            service_minutes = 0 
            service_units    = 0   
        else:
            service_minutes = services[0][0]
            service_units = ceil(services[0][0] / 15 )
        results.append([names[id], service_minutes, service_units])
    return (dates, results)

def get_last_quarter_dates(my_date):
    """ Return a tuple (begining and ending dates) of last quarter """

    q_month_end  = ((my_date.month-1)//3) * 3
    q_month_beg = q_month_end - 2
    if my_date.month < 4:
        year = my_date.year - 1
        lq_beg = my_date.replace(day=1, month=10, year=year)
        lq_end = my_date.replace(day=31, month=12, year=year)
    else:
        lq_beg = my_date.replace(day=1, month=q_month_beg)
        # lq_end = my_date.replace(day=1, month=q_month_end)
        lq_end = date(my_date.year, q_month_end + 1, 1) + timedelta(days=-1)
    return (lq_beg, lq_end)

def write_client_info_to_cvs_file(client_dict, sch_key):

    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    file_name = f'clients_by_{sch_key}_{date}.csv'
    print(file_name)
    with open(file_name, mode='w') as csv_file:
        fieldnames = ['fname', 'lname', 'phone', 'address', 'city', 'state', 'zip', 'county', 'dob', 'lang']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for c in client_dict:
            writer.writerow({'fname': c.fname, 'lname': c.lname, 'phone': c.phone, 'address': c.address, 'city': c.city,
                             'state': c.state, 'zip': c.zip, 'county': c.county, 'dob': c.dob, 'lang': c.lang})
        
def write_client_info_to_cvs_file_with_pro_id(client_dict):

    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    file_name = f'clients_by_pro_{date}.csv'
    print(file_name)
    with open(file_name, mode='w') as csv_file:
        fieldnames = ['fname', 'lname', 'phone', 'dob', 'program_id']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for c in client_dict:
            writer.writerow({'fname': c.fname, 'lname': c.lname, 'phone': c.phone, 
                             'dob': c.dob, 'program_id': c.program_id})
        
def get_client_hours_served_last_quarter():

    results = []
    beg, end = get_last_quarter_dates(date.today())
    dates = f"From {beg} to {end}"
    # print("First day of last quarter:", beg)
    # print("Last day of last quarter:", end)
    q = db.session.query(func.sum(Service.service_dur))
    names = ["All programs", "Second Harvest Program", "Elder Program", "MNSure Program"]
    #q = db.session.query(Service.service_dur)
    services = q.filter(Service.sv_date >= beg, Service.sv_date <= end).all()
    if services[0][0] == None:
            service_minutes = 0 
            service_unit    = 0   
    else:
        service_minutes = services[0][0]
        service_units = ceil(services[0][0] / 15 )
    results.append([names[0], service_minutes, service_units])
    for id in [1,2,3]:
        services = q.filter(Service.sv_date >= beg, Service.sv_date <= end, Service.program_id==id).all()
        if services[0][0] == None:
            service_minutes = 0 
            service_units    = 0   
        else:
            service_minutes = services[0][0]
            service_units = ceil(services[0][0] / 15 )
        results.append([names[id], service_minutes, service_units])
    return (dates, results)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # x = get_last_quarter_dates(date(2021,2,16))
    # print(x)
    # x = get_last_quarter_dates(date.today())
    # print(x)
    
