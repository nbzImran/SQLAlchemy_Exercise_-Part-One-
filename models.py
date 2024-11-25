"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """connects the database to the FLask app."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model for the blogly application."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)  #Required, max length 50
    last_name = db.Column(db.String(50), nullable=False) # Required, max length 50
    img_url = db.Column(
        db.String,
        nullable=True,
        default="https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png" # Default profile picture
    )


    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"


    def __repr__(self):
        """Provide a readable representation of user."""
        return (
            f"<User id={self.id} first_name={self.first_name}"
            f"last_name={self.last_name}  img_url={self.img_url} full_name={self.full_name}>"
        )


class Post(db.Model):
    """Model for blog posts."""

    __tablename__ = 'posts'

    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)  # Title max length 100
    content = db.Column(db.Text, nullable=False)  # Post content
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        """Provide a readable representation of the post."""
        return (
            f"<Post id={self.id} title='{self.title}' created_at='{self.created_at}' "
            f"user_id={self.user_id}>"
        )