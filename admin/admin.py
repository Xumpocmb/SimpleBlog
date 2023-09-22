from flask import Blueprint, render_template, url_for, redirect, session, request, flash, g
from flask_login import logout_user

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.logout', 'title': 'Выйти'}]


def admin_is_logged():
    return True if session.get('admin_logged') else False


def set_logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    context = {
        'title': 'Admin Page'
    }
    if not admin_is_logged():
        return redirect(url_for('.login_admin'))

    return render_template('admin/admin.html', context=context, menu=menu, title='Админ-панель')


@admin.route('/login', methods=["POST", "GET"])
def login_admin():
    if admin_is_logged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "admin":
            session['admin_logged'] = 1
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout_admin():
    # logout_user()
    set_logout_admin()
    return redirect(url_for('.login_admin'))
