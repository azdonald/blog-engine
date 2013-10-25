from app import app, lm, db
from flask import Flask, render_template, request, redirect, g, session, flash, url_for  
from forms import ArticleForm, LoginForm, AuthorForm
from models import Article, Author, Comment, ROLE_ADMIN
import bleach
import HTMLParser
from datetime import datetime
from flask.ext.login import login_user, logout_user, current_user, login_required


@app.before_request
def before_request():
    g.author = current_user
    

@app.route('/')
@app.route('/index')
def hello_world():
    author = g.author
    art = Article.query.all()
    if art is None:
        return 'error'
    return render_template('index.html',art = art, author = g.author)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.filter_by(id = id).first()
    if article is None:
        return 'error'
    return render_template('article.html', article = article)

@login_required
@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/new', methods=['POST', 'GET'])
@login_required
def new():
    author = g.author
    article = Article()
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        art = bleach.clean(article.content, strip=True)
        article = Article(title=article.title, content=art, datePosted = datetime.now(), author = g.author)
        db.session.add(article)
        db.session.commit()
        return redirect('/admin')

    return render_template('new.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if g.author is not None and g.author.is_authenticated():
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        author = Author.query.filter_by(email = form.email.data).first()
        if author is None:
            return redirect(url_for('login'))
        login_user(author)
        return redirect(request.args.get('next') or url_for('admin'))
    return render_template('login.html', form = form)

@login_required
@app.route('/user', methods=['GET', 'POST'])
def user():
    author = Author()
    form = AuthorForm()
    if request.method == 'POST':
        author.username = form.username.data
        author.email = form.email.data
        author.password = author.hash_password(form.password.data)
        author = Author(email = author.email, username = author.username, password = author.password,
                         role = ROLE_ADMIN, is_Active = True)
        db.session.add(author)
        db.session.commit()
        return redirect('/admin')
    return render_template('user.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin'))

    
@lm.user_loader
def load_user(id):
    return Author.query.get(int(id))    
#create a new filter to show only a limited amount of content
@app.template_filter('lc')
def limitcontent(s):
    return s[ : 150]