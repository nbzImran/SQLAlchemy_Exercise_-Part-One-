from flask import Blueprint, render_template, request, redirect
from models import db, User, Post

posts_bp = Blueprint('posts', __name__, template_folder='templates')

@posts_bp.route('/user/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """show form to add a post for a user and handle from submission."""


    user = User.query.get_or_404(user_id)


    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/user/{user_id}")
    
    return render_template('post_new.html', user=user)


@posts_bp.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)



@posts_bp.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit a pist and handle editing."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post_id)


    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(f"/posts/{post.id}")
    
    return render_template('post_edit.html', post=post, user=user)





@posts_bp.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """delete a post."""
    post = Post.query.get_or_404(post_id)

    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/user/{user_id}")