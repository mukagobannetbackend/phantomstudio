from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from . import db
from .models import Sermon, SermonReference, NoteHighlight, NoteComment, ScriptureMatch, BibleSource

main = Blueprint('main', __name__)

def owned(sermon_id):
    sermon = Sermon.query.filter_by(id=sermon_id, user_id=current_user.id).first()
    if not sermon: abort(404)
    return sermon

def form_date(value):
    try: return datetime.fromisoformat(value) if value else datetime.utcnow()
    except ValueError: return datetime.utcnow()

@main.get('/')
def home(): return redirect(url_for('main.dashboard')) if current_user.is_authenticated else redirect(url_for('auth.login'))

@main.get('/dashboard')
@login_required
def dashboard():
    sermons = Sermon.query.filter_by(user_id=current_user.id).order_by(Sermon.sermon_date.desc()).all()
    return render_template('dashboard.html', sermons=sermons[:8], total=len(sermons), sources=BibleSource.query.all())

@main.route('/sermons')
@login_required
def sermons():
    q = Sermon.query.filter_by(user_id=current_user.id)
    term = request.args.get('q','').strip()
    for field in ('topic','speaker'):
        if request.args.get(field): q = q.filter(getattr(Sermon, field).ilike(f"%{request.args[field]}%"))
    if term: q = q.filter(or_(Sermon.title.ilike(f'%{term}%'), Sermon.content.ilike(f'%{term}%'), Sermon.location.ilike(f'%{term}%')))
    return render_template('sermons.html', sermons=q.order_by(Sermon.sermon_date.desc()).all())

@main.route('/sermons/new', methods=['GET','POST'])
@login_required
def new_sermon():
    if request.method == 'POST':
        sermon = Sermon(user_id=current_user.id, title=request.form.get('title','').strip(), sermon_date=form_date(request.form.get('sermon_date')), speaker=request.form.get('speaker','').strip(), location=request.form.get('location','').strip(), topic=request.form.get('topic','').strip(), content=request.form.get('content',''))
        if not sermon.title: flash('A sermon title is required.', 'error')
        else: db.session.add(sermon); db.session.commit(); flash('Sermon saved.', 'success'); return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))
    return render_template('sermon_form.html', sermon=None)

@main.route('/sermons/<int:sermon_id>', methods=['GET','POST'])
@login_required
def sermon_detail(sermon_id):
    sermon = owned(sermon_id)
    if request.method == 'POST':
        sermon.title=request.form.get('title','').strip(); sermon.sermon_date=form_date(request.form.get('sermon_date')); sermon.speaker=request.form.get('speaker','').strip(); sermon.location=request.form.get('location','').strip(); sermon.topic=request.form.get('topic','').strip(); sermon.content=request.form.get('content',''); db.session.commit(); flash('Sermon updated.', 'success'); return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))
    return render_template('sermon_detail.html', sermon=sermon, matches=ScriptureMatch.query.filter_by(sermon_id=sermon.id, user_id=current_user.id).all())

@main.post('/sermons/<int:sermon_id>/delete')
@login_required
def delete_sermon(sermon_id):
    sermon=owned(sermon_id); db.session.delete(sermon); db.session.commit(); flash('Sermon deleted.', 'success'); return redirect(url_for('main.sermons'))

@main.post('/sermons/<int:sermon_id>/references')
@login_required
def add_reference(sermon_id):
    sermon=owned(sermon_id); reference=request.form.get('reference','').strip()
    if reference: db.session.add(SermonReference(user_id=current_user.id, sermon_id=sermon.id, reference=reference, translation=request.form.get('translation','Reference only').strip(), source_identifier=request.form.get('source_identifier','').strip())); db.session.commit(); flash('Reference saved. Bible text is not bundled until an authorized source is configured.', 'success')
    return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))

@main.post('/sermons/<int:sermon_id>/highlights')
@login_required
def add_highlight(sermon_id):
    sermon=owned(sermon_id); selected=request.form.get('selected_text','').strip()
    if selected: db.session.add(NoteHighlight(user_id=current_user.id, sermon_id=sermon.id, selected_text=selected, anchor_start=request.form.get('anchor_start',type=int), anchor_end=request.form.get('anchor_end',type=int), color=request.form.get('color','gold'))); db.session.commit(); flash('Highlight saved.', 'success')
    return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))

@main.post('/sermons/<int:sermon_id>/comments')
@login_required
def add_comment(sermon_id):
    sermon=owned(sermon_id); comment=request.form.get('comment','').strip(); highlight_id=request.form.get('highlight_id',type=int)
    if highlight_id and not NoteHighlight.query.filter_by(id=highlight_id, sermon_id=sermon.id, user_id=current_user.id).first(): abort(404)
    if comment: db.session.add(NoteComment(user_id=current_user.id, sermon_id=sermon.id, highlight_id=highlight_id, comment=comment)); db.session.commit(); flash('Comment saved.', 'success')
    return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))

@main.post('/sermons/<int:sermon_id>/matches')
@login_required
def add_match(sermon_id):
    sermon=owned(sermon_id); excerpt=request.form.get('excerpt','').strip(); reference=request.form.get('reference','').strip()
    if excerpt: db.session.add(ScriptureMatch(user_id=current_user.id, sermon_id=sermon.id, excerpt=excerpt, reference=reference or None, match_type=request.form.get('match_type','unverified'), confidence=0, source='manual', verification_status='unverified')); db.session.commit(); flash('Match saved as unverified. Confirm it against an authorized Bible source.', 'success')
    return redirect(url_for('main.sermon_detail', sermon_id=sermon.id))
