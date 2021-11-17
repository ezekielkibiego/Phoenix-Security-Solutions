from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import Crime,Comment
from flask_login import login_required, current_user
from .. import db
from .forms import CommentForm

@main.route('/crime/<id>', methods=['GET', 'POST'])
@login_required
def crime_details(id):
    comments = Comment.query.filter_by(crime_id=id).all()
    crimes = Crime.query.get(id)
    if crimes is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.comment.data,
            crime_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comments.html', crime=crimes, comment=comments, comment_form=form)