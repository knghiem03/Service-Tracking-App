""" Use this script to facilitate a database setup instead of manually 
    typing commands each time we have new data to seed the database """

import os, json
from random import choice, randint
from datetime import datetime, date
import model, server
from crud import *
from faker import Faker
faker = Faker()

# os.system('dropdb clients_app')
# os.system('createdb clients_app')

model.connect_to_db(server.app)
model.db.create_all()

# Calculate age from DateTime date
def age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
        age -= 1
    return age

def seed_client_table():
    # Load client data from faker file
    with open('data/Faker/client_data_file_23') as f:
        client_data = json.loads(f.read())

    # Create movies, store them in list so we can use them
    # to create fake ratings  
    clients_in_db = []
    for data in client_data:
        fname = data["fname"]
        lname = data["lname"]
        dob   = data["dob"]
        phone = data["phone"]
        address = data["address"]
        city  = data["city"]
        state = data["state"]
        zip   = data["zip"]
        county = data["county"]
        lang   = data["lang"]
        r_date = data['r_date']

        #print(f"{dob}===={age(datetime.strptime(dob,'%Y-%m-%d'))}")
        #client_age = age(datetime.strptime(dob,'%Y-%m-%d'))
        # This db_client is one row of the clients table 
        
        db_client = create_client(fname = fname, lname = lname, dob = dob, phone = phone,
                                    address = address, city = city, state = state, zip = zip,
                                    county = county, lang = lang , r_date = r_date, mname='')
        # Is the line below needed ????
        clients_in_db.append(db_client)

# FOR each fake client, check if age is 60, link it to "second harvest" and "elders"
# if it is under 60, randomly link it with mnsure, gotv, or other 2 out of 3


def seed_service_table():
    # This is a helper function to aid in seeding the services table *************************
    all_clients = db.session.query(Client.client_id,Client.dob).all()
    for client in all_clients:
    
        # client_age = age(datetime.strptime(client.dob,'%Y-%m-%d'))
        client_age = age(client.dob)
        service_dur = randint(5,75)
        # sv_date     = date.today()
        sv_date     = faker.date_between(start_date = "-180d", end_date = "-1d")
        temp        = datetime.now()
        sv_bt       = temp - timedelta(minutes=15)
        sv_et       = datetime.now()
        sv_note = [ "Sign up for Second Harvest program",
                    "Sign up for home meal delivery",
                    "register to vote and other voting information",
                    "Health care",
                    "Other"
        ]
        if (client_age >= 60):
            print(f"add {client.client_id} to older program")
            idx = randint(0,1)
            # sv_note1 = "Sign up for Second Harvest program"
            # sv_note2 = "Sign up for home meal delivery"
            # Nov 9, I refactor and move this def from crud.py and this module breaks. With help from Maura, it works.
            # It turns out that get_client_by_id returns a client object = one row, not just the id. Why it works before the move ????
            record_service(client.client_id, 1, sv_note[idx], sv_date, sv_bt, sv_et, service_dur)
            # record_service(client.client_id, 2, sv_note[idx], sv_date, sv_bt, sv_et, service_dur)
         
        else:
            # sv_note1 = "register to vote and other voting information"
            # sv_note2 = "Health care"
            # sv_note3 = "Other"
            idx = randint(2,4)
            record_service(client.client_id, 3, sv_note[idx], sv_date, sv_bt, sv_et, service_dur)
            # record_service(client.client_id, 4, sv_note[idx], sv_date, sv_bt, sv_et, service_dur)
            # record_service(client.client_id, 5, sv_note[idx], sv_date, sv_bt, sv_et, service_dur)

    return 

def seed_program_table():
   
    create_program("Second Harvest", "Monthly food box for seniors over 60")
    create_program("Elders",         "Assistance provided to senior over 60 who is a NAPIS member")
    create_program("GOTV",           "Civic engagement program")
    create_program("MNSURE",         "State sponsored Health Insurance")
    create_program("Other services", "Other services")

def create_extra_real_person():

    faker = Faker()
    dob = datetime.strptime("03-15-1955","%m-%d-%Y")
    r_date = faker.date()
    create_client('Kim','Nghiem','5990 Highview Pl','Shoreview','MN',
                '55126','Ramsey','Vietnamese',mname='Thi',dob=dob,phone='651-222-3333', r_date=r_date)
    
    dob = datetime.strptime("06-15-1973","%m-%d-%Y")
    r_date = faker.date()
    create_client('Mya','Nay','990 Scenic Pl','St. Paul','MN',
                '55103','Hennepin','Karen',mname='poe',dob=dob,phone='651-222-3335',r_date=r_date)

    dob = datetime.strptime("09-19-1956","%m-%d-%Y")
    r_date = faker.date()
    create_client('Toan','Nguyen','5990 Highview Pl','Maplewood','MN',
                '55104','Ramsey','Vietnamese',mname='Van',dob=dob,phone='651-222-3334',r_date=r_date)
    
    dob = datetime.strptime("06-15-1959","%m-%d-%Y")
    r_date = faker.date()
    create_client('Pew','Toe','954 Thomas Rd','St. Paul','MN',
                '55103','Hennepin','Karen',mname='poe',dob=dob,phone='651-222-3335',r_date=r_date)   


if __name__ == "__main__":
    os.system('dropdb clients_app')
    os.system('createdb clients_app')
    seed_client_table()
    seed_program_table()
    seed_service_table()
