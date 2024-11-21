"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """connects the database to the FLask app."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """USer Model for the blogly applicatuon."""

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
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}  img_url={self.img_url} full_name={self.full_name}>"