from app import db

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return '<BlogPost %r>' % self.title

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    usrnm = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    posts = db.relationship('BlogPost', backref = 'author')

    def __init__(self, usrnm, password):
        self.usrnm = usrnm
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.usrnm
