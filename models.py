from flask_sqlalchemy import SQLAlchemy
import datetime
"""Models for Blogly."""
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_PIC_URL = 'https://www.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'


class User(db.Model):
    """User Class"""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False, unique=False)

    last_name = db.Column(db.Text, nullable=False, unique=True)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_PIC_URL)

    posts = db.relationship('Post', backref="user")

    @classmethod
    def get_by_user_id(cls, id):
        """Return full name of user."""
        return cls.query.filter_by(id=id).all()

    @classmethod
    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last_name={u.last_name} image url={u.image_url}>"

    def greet(self):
        return f"I'm {self.first_name} {self.last_name}"


class Post(db.Model):
    """Post Class"""
    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False, unique=True)

    content = db.Column(db.Text, nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    
    

    

    @classmethod
    def get_by_user_id(cls, id):
        """Return post info for a given ID."""
        return cls.query.filter_by(id=id).all()

    @classmethod
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id ={p.user_id} user={p.user}>"


class PostTag(db.Model):
    """Post Tag Class"""
    __tablename__ = 'PostTags'

    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),  primary_key=True)
    
    
    

    @classmethod
    def __repr__(self):
        pt = self
        return f"<Post id ={pt.post_id} Tag id = {pt.tag_id}>"

class Tag(db.Model):
    """Tag Class"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary="PostTags", backref="tags")

    @classmethod
    def __repr__(self):
        t = self
        return f"<Tag id = {t.id} Tag name = {t.name}>"