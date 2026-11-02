from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(10), default='dark')
    __table_args__ = {'extend_existing': True}
    def check_password(self, value): return check_password_hash(self.password_hash, value)

class Sermon(db.Model):
    __tablename__ = 'scripture_sermons'
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, nullable=False, index=True)
    title = db.Column(db.String(220), nullable=False); sermon_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    speaker = db.Column(db.String(160)); location = db.Column(db.String(160)); topic = db.Column(db.String(160)); content = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow); updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    references = db.relationship('SermonReference', backref='sermon', cascade='all, delete-orphan', lazy=True)
    highlights = db.relationship('NoteHighlight', backref='sermon', cascade='all, delete-orphan', lazy=True)

class SermonReference(db.Model):
    __tablename__ = 'scripture_references'
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, nullable=False, index=True); sermon_id = db.Column(db.Integer, db.ForeignKey('scripture_sermons.id'), nullable=False)
    reference = db.Column(db.String(160), nullable=False); translation = db.Column(db.String(80), default='Reference only'); source_identifier = db.Column(db.String(255)); created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NoteHighlight(db.Model):
    __tablename__ = 'scripture_highlights'
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, nullable=False, index=True); sermon_id = db.Column(db.Integer, db.ForeignKey('scripture_sermons.id'), nullable=False)
    selected_text = db.Column(db.Text, nullable=False); anchor_start = db.Column(db.Integer); anchor_end = db.Column(db.Integer); color = db.Column(db.String(20), default='gold'); created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('NoteComment', backref='highlight', cascade='all, delete-orphan', lazy=True)

class NoteComment(db.Model):
    __tablename__ = 'scripture_comments'
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, nullable=False, index=True); sermon_id = db.Column(db.Integer, db.ForeignKey('scripture_sermons.id'), nullable=False); highlight_id = db.Column(db.Integer, db.ForeignKey('scripture_highlights.id'), nullable=True)
    comment = db.Column(db.Text, nullable=False); created_at = db.Column(db.DateTime, default=datetime.utcnow); updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BibleSource(db.Model):
    __tablename__ = 'scripture_sources'
    id = db.Column(db.Integer, primary_key=True); name = db.Column(db.String(160), nullable=False); language = db.Column(db.String(40), nullable=False); provider = db.Column(db.String(160)); licence_terms = db.Column(db.Text); status = db.Column(db.String(30), default='not_configured'); created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScriptureMatch(db.Model):
    __tablename__ = 'scripture_matches'
    id = db.Column(db.Integer, primary_key=True); user_id = db.Column(db.Integer, nullable=False, index=True); sermon_id = db.Column(db.Integer, db.ForeignKey('scripture_sermons.id'), nullable=False)
    excerpt = db.Column(db.Text, nullable=False); reference = db.Column(db.String(160)); match_type = db.Column(db.String(30), nullable=False, default='unverified'); confidence = db.Column(db.Float, default=0); source = db.Column(db.String(160), default='manual'); verification_status = db.Column(db.String(30), default='unverified'); created_at = db.Column(db.DateTime, default=datetime.utcnow)

def own_tables():
    return [Sermon.__table__, SermonReference.__table__, NoteHighlight.__table__, NoteComment.__table__, BibleSource.__table__, ScriptureMatch.__table__]
