from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from models import ROLE_ADMIN, Article, Author, Comment
from werkzeug.security import generate_password_hash, check_password_hash


class ArticleForm(Form):
    title = TextField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


    def validate(self):
        if not Form.validate(self):
            return False

        return True
    
    
class CommentForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    email = TextField('Email',validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)




    def validate(self):
        if not Form.validate(self):
            return False

        return True
    
class LoginForm(Form):
    email = TextField('Email',validators=[DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        author = Author.query.filter_by(email = self.email.data).first()
        if author is None:
            self.email.errors.append("Wrong email")
            return False
        if not check_password_hash(author.password, self.password.data):
            self.password.errors.append("Wrong password")
            return False
        if author.role != ROLE_ADMIN:
            return False
        self.author = author
        return True
    
class AuthorForm(Form):
    username = TextField('username', validators=[DataRequired()])
    email = TextField('email',validators=[DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)




    def validate(self):
        if not Form.validate(self):
            return False

        return True