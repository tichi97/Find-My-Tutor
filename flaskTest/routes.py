import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskTest import app, db, bcrypt, mail,login_manager
from flask_mail import Message
from flaskTest.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ContactForm, SearchForm
from flaskTest.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    posts = Post.query.all()
    results = []
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            search_term = form.search.data.title()
            qry = db.session.query(Post).filter(Post.title == search_term)
            results = qry.all()
            return render_template('home.html', title='Results', form=form, posts=results)
    return render_template('home.html', posts=posts, form=form)





@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,location=form.location.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log in Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profilepics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data=current_user.location
    image_file = url_for(
        'static', filename='profilepics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(subject=form.subject.data, topics=form.topics.data, grades=form.grades.data, style=form.style.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.subject, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.subject = form.subject.data
        post.style = form.style.data
        post.grades=form.grades.data
        post.topics=form.topics.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.subject.data = post.subject
        form.style.data = post.style
        form.topics.data=post.topics
        form.grades.data=post.grades

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/contact", methods=['GET', 'POST'])
def contact(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.author
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg = Message("Tutoring Request",
                          sender='kenanitichi@gmail.com', recipients=[user.email])
            msg.body = """
              From: %s <%s>
              %s
              """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Your message has been sent!', 'success')
            return redirect(url_for('home'))
    return render_template('post.html', title='Contact', form=form, post=post)


@app.route("/home/results", methods=['GET', 'POST'])
def search_post():
    post = Post.query.get_or_404(post_id)
    user = post.author
    results = []
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
            search_term = form.search.data
            qry = db_session.query(Post).filter(Post.subject == search_term)
            results = qry.all()
            return render_template('home.html', title='Contact', form=form, posts=results)
