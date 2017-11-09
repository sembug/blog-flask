from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import logging.config
import settings
from core import blog_blueprint
from database import db
from database.models import Post, Category, Tag
from jinja2 import environment
from flaskext.markdown import Markdown

def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)

def categories_list():
    categories = Category.query.all()
    return render_template('_categories_list.html', categories=categories)

def tags_list():
    tags = Tag.query.all()
    return render_template('_tags_list.html', tags=tags)

def create_app():
    app = Flask(__name__)
    app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)
    configure_admin(app)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # db.drop_all(app=app)
    # db.create_all(app=app)
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.globals.update(categories_list=categories_list)
    app.jinja_env.globals.update(tags_list=tags_list)
    Markdown(app)
    return app

def configure_admin(app):
    admin = Admin(app, name='Blog', template_mode='bootstrap3')
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Tag, db.session))

def main():
    app = create_app()
    app.register_blueprint(blog_blueprint)
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == '__main__':
    main()
