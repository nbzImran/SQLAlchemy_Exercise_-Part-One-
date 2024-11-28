from flask import Blueprint, render_template, request, redirect
from models import db, User, Post, Tag, PostTag

posts_bp = Blueprint('posts', __name__, template_folder='templates')

@posts_bp.route('/user/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """show form to add a post for a user and handle from submission."""


    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tags')


        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()

        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)

            db.session.commit()
        return redirect(f"/user/{user_id}")
    
    return render_template('post_new.html', user=user, tags=tags)


@posts_bp.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)



@posts_bp.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit a pist and handle editing."""

    post = Post.query.get_or_404(post_id)
    # user = User.query.get_or_404(post_id)
    tags = Tag.query.all()


    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        tag_ids = request.form.getlist('tags')

        post.tags = [Tag.query.get(tag_id) for tag_id in tag_ids]
        db.session.commit()
        return redirect(f"/posts/{post.id}")
    
    return render_template('post_edit.html', post=post, tags=tags)





@posts_bp.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """delete a post."""
    post = Post.query.get_or_404(post_id)

    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/user/{user_id}")