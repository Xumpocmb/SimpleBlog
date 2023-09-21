from flask import Flask, render_template, request, flash, session, url_for, redirect, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from data.DB import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dcbe456b65ee12a127af010e84054b7f24dc0910'
app.config['DATABASE'] = 'site.db'
app.config['DEBUG'] = True
app.config.from_object(__name__)
# app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"




class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = DB(app.config['DATABASE']).get_user_info_by_id(user_id)
        print(self.__user['id'])
        return self

    def create(self, user):
        self.__user = user
        print(self.__user['id'])
        return self

    def get_id(self):
        return str(self.__user['id'])


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)


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
    if current_user.is_authenticated:
        return redirect(url_for('view_profile'))

    if request.method == "POST":
        user = DB(app.config['DATABASE']).get_user_info(request.form['username'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remember') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("view_profile"))

        flash("Неверная пара логин/пароль", "error")

    # if request.method == 'GET':
    #     # log = request.cookies.get('logged') if request.cookies.get('logged') else None
    #     if 'userLogged' in session:
    #         return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST':
    #     if request.form.get('remember', None):
    #         print('session permanent')
    #         session.permanent = True
    #     else:
    #         session.permanent = False
    #     user = DB(app.config['DATABASE']).get_user_password(request.form['username'])
    #     if user and check_password_hash(user['password'], request.form['username']):
    #         session['userLogged'] = request.form['username']
    #         # request.cookies.__setitem__('logged', 'yes')
    #         return redirect(url_for('profile', username=session['userLogged']))
    #     else:
    #         flash('Wrong data!', 'error')
    context = {
        'title': 'Login Page'
    }
    return render_template('login.html', context=context)


# @app.route('/profile/<username>')
# def profile(username):
#     context = {
#         'title': 'Profile Page',
#         'username': username,
#     }
#     if 'userLogged' not in session or session['userLogged'] != username:
#         # abort(401)
#         return redirect(url_for('profile', username=username))  # session['userLogged']
#     # print(session)
#     return render_template('profile.html', context=context)


@app.route('/profile')
@login_required
def view_profile():
    context = {
        'title': 'Profile Page',
        'username': current_user.get_id(),
    }

    return render_template('profile.html', context=context)


@app.errorhandler(404)
def page_not_found(error):
    context = {
        'title': 'Unknown Page'
    }
    return render_template('page404.html', context=context), 404


@app.route('/logout')
def logout():
    # request.cookies.__setitem__('logged', '')
    logout_user()
    # session.clear()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    context = {
        'title': 'Add Post Page',
    }
    post_info = {}
    if request.method == 'POST':
        if 'userLogged' in session:
            post_info['title'] = request.form['title']
            post_info['text'] = request.form['text']
            post_info['author'] = session['userLogged']
            dbase = DB(app.config['DATABASE']).add_post(post_info)
            if dbase:
                flash('The post was successfully added!', category='success')
            else:
                flash('Error was detected!', category='error')
            return render_template('add_post.html', context=context)
        else:
            return redirect(url_for('login'))
    return render_template('add_post.html', context=context)


@app.route('/posts')
def posts():
    context = {
        'title': 'Posts Page',
    }
    db_posts = DB(app.config['DATABASE']).get_posts()
    context['posts'] = db_posts
    return render_template('posts.html', context=context)


@app.route('/post/<int:id_post>')
def show_post(id_post):
    post = DB(app.config['DATABASE']).get_post(id_post)
    context = {
        'title': 'Posts Page',
        'post': post,
    }
    return render_template('view_post.html', context=context)


@app.route('/register', methods=['POST', 'GET'])
def register():
    context = {
        'title': 'Register Page'
    }
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            data = {'username': request.form['username'], 'password': generate_password_hash(request.form['password'])}
            result = DB(app.config['DATABASE']).add_user(data)
            if result:
                flash('You have register successfully!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error was detected!', 'error')
        else:
            flash('Please, fill all fields!', 'error')
    return render_template('register.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
