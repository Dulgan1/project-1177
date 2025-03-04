from flask import (Flask, render_template, jsonify,
                   request, session, redirect, url_for,
                   flash, make_response, abort)
from pymongo import DESCENDING
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from models import Ticket
from os import getenv

app = Flask(__name__)

@app.route("/")
def index():
    tickets = None
    with MongoClient( getenv('URI')) as db_client:
        db = db_client[getenv('MAIN_DB')]
        tickets = db.tickets.find(sort=[('ticket_index', DESCENDING)])

    return render_template('index.html', tickets=tickets)

@app.route("/ticket/<ticket_index>")
def ticket(ticket_index):
    ticket = None
    with MongoClient(getenv('URI')) as db_client:
        db = db_client[getenv('MAIN_DB')]
        ticket = db.posts.find_one({'ticket_index': ticket_index})
    
    return render_template('ticket.html', ticket=ticket)

@app.route("/admin/login", methods=['GET', 'POST'], strict_slashes=False)
def admin_login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        with MongoClient( getenv('URI')) as db_client:
            db = db_client[getenv('MAIN_DB')]
            user = db.admin.find_one({'user_name': user_name})
            if password == user.get('password'):
                session['user_name'] = user_name
                return redirect(url_for('admin'))

    return render_template('login.html')

@app.route("/admin", methods=['GET', 'POST'], strict_slashes=False)
def admin():
    with MongoClient( getenv('URI')) as db_client:
        if request.method == 'GET':
            if not session.get('user_name'):
                return redirect(url_for('admin_login'))
        if request.method == 'POST':
            if not session.get('user_name'):
                return redirect(url_for('admin_login'))

            ticket_db = db_client[getenv('MAIN_DB')]
            new_ticket = Ticket(games=games, total_odds=total_odds, dated=dated,
                                starts=starts, ticket_index=ticket_index,
                                status=status, )
            ticket_db.tickets.insert_one(new_ticket.to_dict())
            
            