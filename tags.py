from flask import Blueprint, render_template, request, redirect, flash
from models import db, User, Post, Tag, PostTag


tags_bp = Blueprint('tags', __name__, template_folder='templates')


@tags_bp.route('/tags')
def list_tags():
    """list all tags."""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)



@tags_bp.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """show detail about a tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)


@tags_bp.route('/tags/new', methods=["GET", "POST"])
def add_tag():
    """add a new tag."""
    posts = Post.query.all()

    if request.method == "POST":
        name = request.form['name']
        post_ids = request.form.getlist('posts')


        if not name:
            flash("Tag name cannot be empty!", "error")
            return redirect('/tags/new')
        
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        


        for post_id in post_ids:
            post = Post.query.get(post_id)
            new_tag.posts.append(post)

        db.session.commit()
        return redirect('/tags')
    
    return render_template('tag_new.html', posts=posts)



@tags_bp.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    """Edit a tag."""


    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()


    if request.method == "POST":
        tag.name = request.form['name']
        post_ids = request.form.getlist('posts')

        tag.posts = [Post.query.get(post_id) for post_id in post_ids]
        db.session.commit()
        return redirect('/tags')
    
    return render_template('tags_edit.html', tag=tag, posts=posts)




@tags_bp.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delet_tag(tag_id):
    """delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')