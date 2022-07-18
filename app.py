"""Blogly application."""
from flask import Flask, redirect, render_template, request, flash

from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SECRET_KEY'] = "jondawson917"




connect_db(app)
db.create_all()

@app.route('/')
def main():
    """Shows list of all pets in db"""
    return redirect('/users')


#--------------USERS----------------------------------------
@app.route('/users')
def list_users():
    """Shows list of all pets in db"""
    users = User.query.all()
    
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_add_user_form():

    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single pet"""
    
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route('/users/<int:id>/edit')
def edit_user(id):
    
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:id>/edit', methods = ["POST"])
def edit_user_update(id):
    user = User.query.get_or_404(id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

###############POSTS########################################

@app.route("/users/<int:id>/posts/new")
def new_post_form(id):
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route("/users/<int:id>/posts/new", methods=["POST"])
def process_post(id):
    post_titles = db.session.query(Post.title).all()
    post_content = db.session.query(Post.content).all()
    title = request.form["title"]
    content = request.form["content"]
    if (title in post_titles) or (content in post_content):
        flash (f"{title} and/or {content} already exists")
    else:
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(user_id=id, title=title, content=content, tags=tags)
        db.session.add(new_post)
        db.session.commit()
    
    return redirect(f"/users/{id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post =  Post.query.get_or_404(post_id)
 
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title} has been edited")
    return redirect(f'/users/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

###############TAGS##################

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()

    return render_template('allTags.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    posts = Post.query.all()
    return render_template('tag_new.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def new_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag = Tag(name=request.form['name'], posts=posts)
    if tag not in Tag.query.all():
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag {tag.name} added")
        return redirect('/tags')
    else:
        flash(f"Tag {tag.name} is already in the list")
        return redirect('/tags')
@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show a page with dertail on a tag by tag id"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_id_nums = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/')

@app.route('/tags/<int:tag_id>/delete', methods = ["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"The Tag {tag.name} has been deleted.")
    return redirect(f'/tags')
