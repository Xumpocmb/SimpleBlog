from flask import Flask, render_template, request, flash, session, url_for, redirect, abort
import sqlite3
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '123123'
app.config['DATABASE'] = '/data/site.db'
app.config['DEBUG'] = True
app.config.update(dict(DATABASE=os.path.join(app.root_path, '/data/site.db')))


def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/')
def index():
    context = {
        'title': 'Main Page'
    }
    return render_template('index.html', context=context)


@app.route('/about')
def about():
    context = {
        'title': 'About Page'
    }
    return render_template('about.html', context=context)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        message = request.form['message']
        flash('Message was sent!', category='success')
    context = {
        'title': 'Contact Page'
    }
    return render_template('contact.html', context=context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' and request.form['password'] == 'admin':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    context = {
        'title': 'Login Page'
    }
    return render_template('login.html', context=context)


@app.route('/profile/<username>')
def profile(username):
    context = {
        'title': 'Profile Page',
        'username': username,
    }
    if 'userLogged' not in session or session['userLogged'] != username:
        # abort(401)
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('profile.html', context=context)


@app.errorhandler(404)
def page_not_found(error):
    context = {
        'title': 'Unknown Page'
    }
    return render_template('page404.html', context=context), 404


if __name__ == '__main__':
    app.run(debug=True)


