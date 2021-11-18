from flask import render_template, request, redirect, url_for, abort, flash
from flask_login.utils import confirm_login
from . import main
from ..models import Crime, Upvote, Downvote,Comment
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
def like(id):
    crime = Crime.query.get(id)
    if confirm_login is None:
        abort(404)
    like = Upvote.query.filter_by(user_id=current_user.id, crime_id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        flash('Your vote has been recorded successfully!')
        return redirect(url_for('main.index'))
    new_like = Upvote(
        user_id=current_user.id,
        crime_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully upvoted!')
    return redirect(url_for('main.index'))
@main.route('/dislike/:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    posts = Crime.query.get(id)
    if posts is None:
        abort(404)
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, crime_id=id).first()
    if dislike is not None:
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully downvoted!')
        return redirect(url_for('.index'))
    new_dislike = Downvote(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully downvoted!')
    return redirect(url_for('.index'))
    
