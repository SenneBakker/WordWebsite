from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import datetime

from werkzeug.exceptions import abort

from FlaskApp.auth import login_required
from FlaskApp.db import get_db

bp = Blueprint('wordlists', __name__, url_prefix='/wordlists')

@login_required
@bp.route('/')
def index():
    db = get_db()
    query = query = """
SELECT
    w.author_id AS wordlist_id,
    w.name AS name,
    w.created AS created,
    u.id AS user_id,
    u.username AS username
FROM wordlists w
INNER JOIN user u ON u.id = w.author_id;"""

    lists = db.execute(query).fetchall()
    return render_template('wordlists.html', lists = lists)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['title']
        body = request.form['body']
        error = None

        if not name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)' 
                ' VALUES (?, ?, ?)',
                (g.user['id'], name, datetime.date.today().strftime('%Y-%m-%d'))
            )
            db.commit()
            return redirect(url_for('addWordlists.index'))

    return render_template('wordlists.html')