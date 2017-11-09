from flask import render_template
from . import blog_blueprint
from database.models import Post
from database.models import Category


@blog_blueprint.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', items=posts)

@blog_blueprint.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('single.html', item=post)
