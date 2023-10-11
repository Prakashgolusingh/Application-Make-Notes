from flask import Blueprint, render_template, request, flash, redirect
from .models import Note
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
      if request.method == 'POST':
            notes = request.form.get('notes')
            if len(notes)<1:
                  flash("Note is too short", category = 'error')
            else:
                  new_note = Note(data = notes, user_id = current_user.id)
                  db.session.add(new_note)
                  db.session.commit()
                  flash("Note is added successfully", category='success')
      return render_template('home.html', user = current_user)

@views.route('/delete/<id>')
@login_required
def deleteNote(id):
      note_id = Note.query.get(id)
      print(note_id)
      db.session.delete(note_id)
      db.session.commit()
      flash('Note Deleted Successfully', category='success')
      return redirect('/')