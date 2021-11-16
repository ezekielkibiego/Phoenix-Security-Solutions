from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import Post, Upvote, Downvote
from flask_login import login_required, current_user
from .. import db

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    like = Upvote.query.filter_by(user_id=current_user.id, post_id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unupvoted the pitch!')
        return redirect(url_for('main.index'))
    new_like = Upvote(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully upvoted the pitch!')
    return redirect(url_for('main.index'))
@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    posts = Post.query.get(id)
    if posts is None:
        abort(404)
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, post_id=id).first()
    if dislike is not None:
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully undownvoted the pitch!')
        return redirect(url_for('.index'))
    new_dislike = Downvote(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully downvoted the pitch!')
    return redirect(url_for('.index'))