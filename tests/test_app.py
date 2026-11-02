import os
import tempfile
import pytest
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    fd, path = tempfile.mkstemp(suffix='.db'); os.close(fd)
    os.environ['DATABASE_URL'] = 'sqlite:///' + path
    os.environ['SECRET_KEY'] = 'test-secret'
    from app import create_app, db
    app = create_app(); app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.app_context():
        db.drop_all(); db.create_all()
        db.session.execute(db.text("INSERT INTO users (id,email,password_hash,display_name,theme) VALUES (1,'test@example.com',:h,'Test','dark')"), {'h': generate_password_hash('password')}); db.session.commit()
    yield app
    try: os.remove(path)
    except OSError: pass
    os.environ.pop('DATABASE_URL', None)

def login(client): return client.post('/auth/login', data={'email':'test@example.com','password':'password'}, follow_redirects=True)

def test_health_and_login(app):
    c=app.test_client(); assert c.get('/health').json['status']=='ok'; response=login(c); assert response.status_code==200; assert b'Workspace overview' in response.data

def test_sermon_create_and_reopen(app):
    from app import db
    from app.models import Sermon
    c=app.test_client(); login(c)
    r=c.post('/sermons/new', data={'title':'Grace and Hope','sermon_date':'2026-11-02T10:00','speaker':'Pastor Test','location':'Main Hall','topic':'Grace','content':'John 3:16 is a reference to verify.'}, follow_redirects=True)
    assert r.status_code==200 and b'Grace and Hope' in r.data
    with app.app_context(): assert Sermon.query.count()==1

def test_private_sermon_route(app):
    from app import db
    from app.models import Sermon
    c=app.test_client(); login(c)
    with app.app_context():
        db.session.add(Sermon(user_id=2,title='Private',content='No')); db.session.commit(); sid=Sermon.query.filter_by(user_id=2).first().id
    assert c.get(f'/sermons/{sid}').status_code==404
