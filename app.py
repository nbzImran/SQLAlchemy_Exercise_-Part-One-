"""Blogly application."""

from flask import Flask, render_template,request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from posts import posts_bp, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "noscamallowed25"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

#register the blueprint
app.register_blueprint(posts_bp)

with app.app_context():
    db.create_all()

    # new_user = User(first_name="Imran", last_name="Nabizada")
    # db.session.add(new_user)
    # db.session.commit()

    user = User.query.all()
    


@app.route('/')
def home():
    rencent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html',posts=rencent_posts)


@app.route('/user')
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users=users)

@app.route('/user/new', methods=["GET", "POST"])
def new_user():
    """Add new Users."""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img_url = request.form.get('img_url') or None

        if not first_name or not last_name:
            return "First and Last names are required.", 400

        new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/user')
    
    return render_template('user_new.html')


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """Show user details."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.img_url = request.form["img_url"] or user.img_url

        db.session.commit()
        return redirect(f"/user/{user.id}")
    
    return render_template('user_edit.html', user=user)



@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user."""

    user = User.query.get_or_404(user_id)

    if user.posts:
        # Prevent deletion if the user has associated posts
        flash("cannot delete users with posts. Please delete posts first.", "error")
        return redirect(f"/user/{user_id}")

    db.session.delete(user)
    db.session.commit()
    return redirect('/user')
