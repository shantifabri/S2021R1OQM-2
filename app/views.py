"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from sqlalchemy import func, Date, cast
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserForm, GetTicketForm
from app.models import User, Ticket
import datetime
# import sqlite3

###
# Routing for your application.
###

@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the website's about page."""
    
    return render_template('about.html', name="Mary Jane")

@app.route('/officer')
def officer():
    return render_template('officer.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/user')
def user():
    services = ['A','B','C']
    numbers = db.session.query(func.max(Ticket.ticketnum),Ticket.service).filter(func.date(Ticket.date) == datetime.date.today()).group_by(Ticket.service).all()
    serviceNums = {}
    for serv in services:
        serviceNums[serv] = 0
    
    for num in numbers:
        serviceNums[num[1]] = num[0]

    return render_template('user.html', serviceNumbers=serviceNums)

@app.route('/add-ticket/<service>', methods=['POST', 'GET'])
def add_ticket(service):
    date = datetime.datetime.now()
    number = db.session.query(func.max(Ticket.ticketnum),Ticket.service).group_by(Ticket.service).filter(Ticket.service == service).filter(func.date(Ticket.date) == datetime.date.today()).all()
    try:
        number = number[0][0]
    except:
        number = 0
    number = number + 1
    ticket = Ticket(service, number, date, "READY")
    db.session.add(ticket)
    db.session.commit()
    flash('Ticket successfully generated')

    services = ['A','B','C']
    #users = db.session.query(User).all() # or you could have used User.query.all()
    numbers = db.session.query(func.max(Ticket.ticketnum),Ticket.service).group_by(Ticket.service).filter(func.date(Ticket.date) == datetime.date.today()).all()
    serviceNums = {}
    for num in numbers:
        serviceNums[num[1]] = num[0]

    return redirect(url_for('user', serviceNumbers=serviceNums))

@app.route('/serve-customer/<service>', methods=['POST', 'GET'])
def serve_customer(service):
    # date = datetime.datetime.now()
    # number = db.session.query(func.max(Ticket.ticketnum),Ticket.service).group_by(Ticket.service).filter(Ticket.service == service).filter(func.date(Ticket.date) == datetime.date.today()).all()
    # try:
    #     number = number[0][0]
    # except:
    #     number = 0
    # number = number + 1
    # ticket = Ticket(service, number, date, "READY")
    # db.session.add(ticket)
    # db.session.commit()
    # flash('Ticket successfully generated')

    # services = ['A','B','C']
    # #users = db.session.query(User).all() # or you could have used User.query.all()
    # numbers = db.session.query(func.max(Ticket.ticketnum),Ticket.service).group_by(Ticket.service).filter(func.date(Ticket.date) == datetime.date.today()).all()
    # serviceNums = {}
    # for num in numbers:
    #     serviceNums[num[1]] = num[0]

    return redirect(url_for('officer', serviceNumbers=[]))

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            email = user_form.email.data # You could also have used request.form['email']

            # save user to database
            user = User(name, email)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
