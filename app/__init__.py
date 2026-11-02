import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'

def normalize_db_url(url):
    url = url or 'sqlite:///scripture-studio.db'
    if url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql+psycopg://', 1)
    if url.startswith('postgresql://') and '+psycopg' not in url:
        return url.replace('postgresql://', 'postgresql+psycopg://', 1)
    return url

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='../templates', static_folder='../static')
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'change-me'),
        SQLALCHEMY_DATABASE_URI=normalize_db_url(os.getenv('DATABASE_URL')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=os.getenv('APP_BASE_URL', '').startswith('https://'),
        BIBLE_PROVIDER=os.getenv('BIBLE_PROVIDER', 'not-configured'),
        BIBLE_SOURCE_URL=os.getenv('BIBLE_SOURCE_URL', ''),
    )
    db.init_app(app); migrate.init_app(app, db); login_manager.init_app(app); csrf.init_app(app)
    from .models import User, own_tables
    @login_manager.user_loader
    def load_user(user_id): return db.session.get(User, int(user_id))
    from .auth import auth
    from .routes import main
    app.register_blueprint(auth); app.register_blueprint(main)
    with app.app_context():
        db.metadata.create_all(bind=db.engine, tables=own_tables())
    @app.context_processor
    def globals(): return {'app_name': 'Scripture Studio'}
    @app.get('/health')
    def health(): return {'status': 'ok', 'service': 'phantomvault-scripture-studio'}
    return app
