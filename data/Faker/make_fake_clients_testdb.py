from faker import Faker
from datetime import datetime
faker = Faker()
import random, json
COUNTY = [  ['Maplewood','55109','Ramsey'],
            ['New Brighton', '55112', 'Ramsey'],
            ['Roseville', '55113', 'Ramsey'],
            ['Shoreview', '55126', 'Ramsey'],
            ['Vadnais Heights', '55127','Ramsey'],
            ['White Bear Lake', '55110','Ramsey'],
            ['St. Paul', '55114','Ramsey'],
            ['St. Paul', '55114','Ramsey'],
            ['St. Paul', '55116','Ramsey'],
            ['St. Paul', '55117','Ramsey'],
            ['St. Paul', '55119','Ramsey'],
            ['St. Paul', '55101','Ramsey'],
            ['St. Paul', '55103','Ramsey'],
            ['St. Paul', '55104','Ramsey'],
            ['St. Paul', '55105','Ramsey'],
            ['St. Paul', '55106','Ramsey'],
            ['St. Paul', '55107','Ramsey'],
            ['St. Paul', '55108','Ramsey'],
            ['St. Paul', '55130','Ramsey'],
            ['Bloomington', '55420','Hennepin'],
            ['Minneapolis', '55401','Hennepin'],
            ['Minneapolis', '55402','Hennepin'],
            ['Minneapolis', '55403','Hennepin'],
            ['Minneapolis', '55404','Hennepin'],
            ['Minneapolis', '55405','Hennepin'],
            ['Brooklyn Center', '55429','Hennepin'],
            ['Brooklyn Park',   '55445','Hennepin'],
            ['Eden Prairie',    '55435','Hennepin'],
            ['Edina',           '55443','Hennepin'],
            ['Brooklyn Park', '55443','Hennepin'],
            ['Brooklyn Park', '55443','Hennepin'],
            ['Brooklyn Park', '55443','Hennepin'],
            ['West ST. Paul', '55118','Dakota'],
            ['Eagan',         '55121','Dakota'],
            ['Burnsville',    '55337','Dakota'],
            ['South St. Paul','55075','Dakota'],
            ['Apple Valley'  ,'55124','Dakota'], 
            ['Oakdale',       '55128','Washington'],
            ['Woodbury',      '55129','Washington'],
            ['Woodbury',      '55125','Washington']
            ]

LANG = ['Karen','Vietnamese','Vietnamese','Vietnamese']
def phn():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return n[:3] + '-' + n[3:6] + '-' + n[6:]

my_list = []
for i in range(20):
    # Need to make a list of dictionary similar to movies.json file to seed the database
    my_dict = {}
    my_dict["fname"] = f"{faker.first_name()}"
    my_dict["lname"] = faker.last_name()
    if i >= 12 :
        my_dict["dob"] = f"{faker.date_of_birth(minimum_age=18,maximum_age=80)}"
    else:
        my_dict["dob"] = f"{faker.date_of_birth(minimum_age=60,maximum_age=80)}"
    my_dict["phone"] = phn()
    my_dict["address"] = faker.street_address()
    ran_num = random.randint(0,len(COUNTY)-1)
    my_dict["city"] = COUNTY[ran_num][0]
    my_dict["state"] = "MN"
    my_dict['zip'] = COUNTY[ran_num][1]
    my_dict['county'] = COUNTY[ran_num][2]
    my_dict['lang'] = random.choice(LANG)
    # my_dict['r_date'] = faker.date()
    # print(f'faker.date type is {type(faker.date())}')
    r_date = faker.date_between(start_date = "-100d", end_date = "-1d")
    r_dateStr = r_date.strftime("%Y-%m-%d")
    my_dict['r_date'] = r_dateStr
    my_list.append(my_dict)

#print(my_list)
x = json.dumps(my_list)
print(x)
    # print(f"{faker.name()}")
    # # print(f"{faker.building_number()} {faker.street_name()}")
    # print(f"{faker.street_address()}")
    # #print(f"St. Paul, MN 55126")
    # ran_num = random.randint(0,len(COUNTY)-1)
    # city = COUNTY[ran_num][0]
    # print(f"{city}, MN {COUNTY[ran_num][1]}")
    # print(f"County: {COUNTY[ran_num][2]}")
    # print(f"DOB: {faker.date_of_birth(minimum_age=40,maximum_age=80)}")
    # print(f"Phone: {phn()}")
    # print("\n")

    # print(f"Female name: {faker.name_female()}")
    # print(faker.postcode())
    # faker.simple_profile('M')