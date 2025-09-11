from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import datetime
import json

from werkzeug.exceptions import abort
import click
from FlaskApp.auth import login_required
from FlaskApp.db import get_db

bp = Blueprint('addWordlists', __name__, url_prefix='/addWordlists')

@bp.route('/<string:name>', methods=('GET', 'POST'))
@login_required
def render(name):
    click.echo(name)
    return render_template('addWordlists.html', name=name)


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     # if request.method == 'POST':
#     #     name = request.form['title']
#     #     body = request.form['body']
#     #     error = None
#     #
#     #     if not name:
#     #         error = 'Title is required.'
#     #
#     #     if error is not None:
#     #         flash(error)
#     #     else:
#     #         db = get_db()
#     #         db.execute(
#     #             'INSERT INTO post (title, body, author_id)'
#     #             ' VALUES (?, ?, ?)',
#     #             (g.user['id'], name, datetime.date.today().strftime('%Y-%m-%d'))
#     #         )
#     #         db.commit()
#     #         return redirect(url_for('wordlists.index'))
#
#     return render_template('addWordlists.html')


@login_required
def save_words(pairs, list_name):
    db = get_db()
    db.executemany("INSERT INTO translation(author_id, name, created, source, translation) VALUES(?,?,?,?,?)", [(g.user['id'], list_name, datetime.date.today().strftime('%Y-%m-%d'), p, pairs[p]) for p in pairs.keys()])
    db.executemany("INSERT INTO wordlists(author_id, name, created) VALUES(?,?,?)", [(g.user['id'],list_name, datetime.date.today().strftime('%Y-%m-%d'))])
    db.commit()

@login_required
@bp.route("/add/<string:name>", methods=["GET", "POST"])
def add(name):
    if request.method == "POST":
        try:
            pairs = dict(zip(request.form.getlist("source_word[]"),request.form.getlist("target_word[]") ))
            pairs = {k: v for k, v in pairs.items() if (v and k)} # get rid of empty records (db attributes cannot be null)
            list_name = name
        except Exception as e:
            click.echo(f"failed to parse new wordlist: {e}")
            pairs = []
            list_name = ""
        if not pairs:
            # fall back to parsing raw text server-side if needed
            raw = request.form.get("pairs", "")
            # TODO: parse raw here
            pairs = []
        if pairs:
            save_words(pairs = pairs, list_name=list_name)
            flash(f"Saved {len(pairs)} word pairs.")
            return redirect(url_for("wordlists.index"))
        flash("Nothing to import.")

    return render_template('addWordlists.html')