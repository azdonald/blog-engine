from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

ROLE_USER = 1
ROLE_ADMIN = 2


class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True, unique = True)
    content = db.Column(db.Text(5000), index = False)
    datePosted = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, ForeignKey('author.id'))
    article = db.relationship('Comment', backref = 'article', lazy = 'dynamic')

    
    def __repr__(self):
        return '<Article %r %r>' %(self.title, self.author)



class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(254), index = True, unique = True)
    username = db.Column(db.String(254), index = True, unique = True)
    password = db.Column(db.String(256))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    is_Active = db.Column(db.Boolean, default = False)
    article = db.relationship('Article', backref = 'author', lazy = 'dynamic')
    comment = relationship('Comment', backref = 'author', lazy = 'dynamic')
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
    def hash_password(self, password):
        self.hash_pw = generate_password_hash(password)
        return self.hash_pw
    
    def check_password(self, password):
        return check_password_hash(self.hash_password(password), password)
    
    
    def __repr__(self):
        return '<Author %r>' %(self.username)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(500))
    datePosted = db.Column(db.DateTime)
    article_id = db.Column(db.Integer, ForeignKey('article.id'))
    author_id = db.Column(db.Integer, ForeignKey('author.id'))
    
    
    def __repr__(self):
        pass