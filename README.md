# Service Tracking App

## Summary

**Client and Service Tracking App** allows users at the agency to search through current clients or add new clients to the database. The app also records the type of service, date of service and duration of the call. When clients within a specific program or age group need to be contacted, the user can either text or call a list of clients with a pre-determined text or voice message via Twilio API, as opposed to calling each individual client.  With this application, the agency will be able to quickly report the level of services and the composition of the community it serves to the funding agency.


## About the Developer

Service Tracking App was created by Kim Nghiem. 


## Technologies

Service Tracking App is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses JQuery and AJAX to interact with the backend. Server routes are tested using the Python unittest module.

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, CSS, AJAX, Javascript, jQuery, Bootstrap <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, Jinja2 <br/>
__APIs:__ Twilio <br/>

## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- PostgreSQL
- Python 3.7
- Twilio API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/knghiem03/Service-Tracking-App.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies🔗:
```
$ pip3 install -r requirements.txt
```
Get your own secret keys🔑 for [Twilio](https://www.twilio.com/doers). Save them to a file `secrets.py`. Your file should look something like this:
```
APP_KEY = 'xyz'
TWILIO_ACCOUNT_SID = 'abc'
TWILIO_AUTH_TOKEN = 'abc'
GOOGLE_CLIENT_ID = 'xyz'
GOOGLE_CLIENT_SECRET = 'xyz'
```
Create database 'clients_app'.
```
$ createdb clients_app
```
Create your database tables and seed🌱 example data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```
