"""Models for Client Trackimng app."""

#from typing import NamedTuple
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user to keep track of login process """

    __tablename__ = "users"

    user_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email    = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Client(db.Model):
    """A client """

    __tablename__ = "clients"

    client_id = db.Column(db.Integer,    autoincrement=True, primary_key=True)
    fname     = db.Column(db.String(25), nullable = False)
    lname     = db.Column(db.String(25), nullable = False)
    mname     = db.Column(db.String(25), nullable = True)
    dob       = db.Column(db.Date,       nullable = True)
    phone     = db.Column(db.String(12), nullable = True)
    address   = db.Column(db.String(50), nullable = False)
    city      = db.Column(db.String(15), nullable = False)
    state     = db.Column(db.String(2),  nullable = False)
    zip       = db.Column(db.Integer,    nullable = False)
    county    = db.Column(db.String(20), nullable = False)
    lang      = db.Column(db.String(10), nullable = False)
    r_date    = db.Column(db.Date,       nullable = True)

    service       = db.relationship("Service",  back_populates="client")
    
    def __repr__(self):
        return f'<User client_id={self.client_id} name={self.fname} {self.lname}>'

class Program(db.Model):
    """A program or service provided by the agency, each row in the table is one program """

    __tablename__ = "programs"

    program_id = db.Column(db.Integer,     autoincrement=True, primary_key=True)
    code       = db.Column(db.String(20),   nullable = False)
    overview   = db.Column(db.String(100), nullable = False)

    service      = db.relationship("Service", back_populates="program")

    def __repr__(self):
        return f"<Program program_id={self.program_id} code={self.code}>"

class Service(db.Model):
    """ This class/table links the client with the services a client received """

    __tablename__ = "services"

    service_id   = db.Column(db.Integer, autoincrement=True, primary_key=True)

    client_id    = db.Column(db.Integer, db.ForeignKey("clients.client_id"))
    program_id   = db.Column(db.Integer, db.ForeignKey("programs.program_id"))

    sv_note = db.Column(db.Text,   nullable = True)
    sv_date = db.Column(db.Date)
    sv_bt   = db.Column(db.DateTime,  nullable = True)
    sv_et   = db.Column(db.DateTime,  nullable = False)
    service_dur  = db.Column(db.Integer,  nullable = True)

    # client       = db.relationship("Client",  backref="services")
    # program      = db.relationship("Program", backref="services")
    client       = db.relationship("Client",  back_populates="service")
    program      = db.relationship("Program", back_populates="service")


    def __repr__(self):
        return f"<Service client_id={self.client_id} program_id={self.program_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///clients_app", echo=True):

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db! in def")

def connect_to_test_db(flask_app, db_uri="postgresql:///testdb", echo=True):  
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db! in def")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_test_db(app)
    print("Connected to the db! in main")
    # This step below creates the tables in this model.py file
    db.create_all() 
    
    