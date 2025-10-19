import functools
import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from subprocess import Popen, PIPE
from requests_oauthlib import OAuth2Session
import json
import app.mod.models as models

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
import os
import base64
import hashlib

def generate_pkce_pair():
    """
    Generates a PKCE code_verifier and code_challenge (S256 method).

    Returns:
        tuple: A tuple containing (code_verifier, code_challenge).
    """
    # Generate a high-entropy cryptographic random string for code_verifier
    # The length should be between 43 and 128 characters.
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8')
    # Ensure the code_verifier meets the length requirements
    code_verifier = code_verifier.replace('=', '') # Remove padding characters

    # Compute the code_challenge using SHA256 hash and URL-safe base64 encoding (without padding)
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '') # Remove padding characters

    return code_verifier, code_challenge

client_id = '54209660'
client_secret = 'gU6tT8w0jhZtUwTDDm5P'
'''
client_id = '51566900'
client_secret = 'HBYzYx2THXdewV9Rdj9y'
'''

# redirect_uri = 'https://dev.syllabica.com/auth/callback'
redirect_uri = 'https://5.101.69.112/auth/callback'

vk = OAuth2Session(client_id, redirect_uri=redirect_uri)
# vk.params['v'] = '5.81'

authorization_base_url = 'https://id.vk.com/authorize'
token_url = 'https://id.vk.ru/oauth2/auth'



bp = Blueprint('auth', __name__, url_prefix='/auth')

class User:
    def __init__(self, config):
        self.config = config

    @property
    def is_admin(self):
        return self.config['accesslvl'] > 99

    @property
    def is_expert(self):
        return self.config['accesslvl'] > 49

    @property
    def is_activated(self):
        return self.config['accesslvl'] > -1

@bp.url_value_preprocessor
def bp_url_value_preprocessor(endpoint, values):
    g.url_prefix = 'auth'


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.user.is_activated:
            return redirect(url_for('auth.checkemail'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = models.User.query.filter_by(vk_id=user_id).first()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    session['code_verifier'], session['code_challenge'] = generate_pkce_pair()
    authorization_url = vk.authorization_url(authorization_base_url, code_challenge=session['code_challenge'], code_challenge_method='S256')
    return redirect(authorization_url[0])

@bp.route('/callback')
def callback():
    print(request.args)
    t = vk.fetch_token(
        token_url,
        # grant_type = 'authorization_code',
        code = request.args['code'],
        code_verifier = session['code_verifier'],
        device_id = request.args['device_id'],
        client_secret=client_secret,
        authorization_response=request.url,
        include_client_id=True
    )

    resp = vk.get('https://api.vk.com/method/users.get?v=5.81&fields=first_name,last_name,photo_50')
    print(f'''
----
f{resp.json()}
----
    ''')
    data = resp.json()['response'][0]

    first_name = data['first_name']
    last_name = data['last_name']
    full_name = f"{first_name} {last_name}"

    db = get_db()
    user = models.User.query.filter_by(vk_id=data['id']).first()

    if not user:
        user = models.User(
            vk_id=data['id'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            url = data['photo_50'],
            access_level=1
        )
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.vk_id

    return redirect(url_for('show_index'))


'''

@bp.route('/callback')
def callback():
    t = vk.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url,  include_client_id=True)
    resp = vk.get('https://api.vk.com/method/users.get?v=5.81&fields=photo_50')

    # r = resp.json()
    # get_db().query(models.User).filter(models.User.email == r['response']['id'])
    # r['response']['id']
    # r['response']['first_name']
    # r['response']['last_name']

    return 'You are logged in as: ' + f'{resp.json()}'

'''

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_index'))

@bp.route('/accesslvl', methods = ('POST', 'GET'))
def get_accesslvl():

    res = 0 if g.user is None else g.user.config['accesslvl']

    return Response(str(res), mimetype='text/txt')

@bp.route('/edit', methods = ('POST', 'GET'))
@bp.route('/edit/<int:user_id>', methods = ('POST', 'GET'))
def edit(user_id = None):
    if not g.user :
       return render_template('auth/edit.html', user = None)

    if not g.user.is_admin or user_id is None:
        user_id = g.user.config["id"]

    db = get_db()
    if request.method == 'POST':
        sql = 'UPDATE user SET '
        if request.form['name']:
            sql += 'username = "' + request.form['name'] + '",'
        if request.form['npassword']:
            sql += 'password = "' + generate_password_hash(request.form['npassword']) + '",'
        key = random.randint(100000000,1000000000)
        if request.form['email']:
            sql += 'email = "' + request.form['email'] + '", accesslvl = "-' + str(key) + '",'

        if g.user.is_admin:
            if request.form['status']:
                sql += 'status = "' + request.form['status'] + '",'
            if request.form['accesslvl']:
                sql += 'accesslvl = "' + request.form['accesslvl'] + '",'

        if not (request.form['cpassword'] and check_password_hash(g.user.config['password'], request.form['cpassword'])):
            flash("Wrong current password")

        if g.user.is_admin or check_password_hash(g.user.config['password'], request.form['cpassword']):
            db.execute(
               sql[:-1] + ' WHERE id = ?', (user_id,)
            )
            db.commit()

    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    return render_template('auth/edit.html', user = user)


@bp.route('/list', methods = ('POST', 'GET'))
def list(user_id = None):
    # if not g.user :
    #    return render_template('auth/edit.html', user=None)

    # if not g.user.is_admin or user_id is None:
    #     user_id = g.user.config["id"]

    db = get_db()
    users = []
    for user in models.User.query.all():
        print(user, dir(user), user.id, user.name, user.password)

    return 'STOP'

    users = db.execute(
            'SELECT id, username, email, status, accesslvl FROM user'
    ).fetchall()
    return render_template('auth/list.html', users = users)


@bp.route('/check', methods=('GET', 'POST'))
def checkemail():
    if request.method == 'POST':
        code = request.form['code']
        db = get_db()
        error = None

        if g.user is None:
            error = 'You are not login.'
        elif code != str(-g.user.config['accesslvl']):
            error = 'Incorrect data.'

        if error is None:
            db.execute(
                'UPDATE user SET accesslvl = ? WHERE id = ?;',
                (1, g.user.config['id'])
            )
            db.commit()

            return redirect(url_for('show_index'))


        flash(error)
    return render_template('auth/login.html')

