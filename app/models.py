from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key = True)
    service = db.Column(db.String(255))
    ticketnum = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    status = db.Column(db.String(255))

    def __init__(self, service, ticketnum, date, status):
        self.service = service
        self.ticketnum = ticketnum
        self.date = date
        self.status = "READY"

    def __repr__(self):
        return '<Ticket n. %r for service: %r>' % self.ticketnum % self.service
