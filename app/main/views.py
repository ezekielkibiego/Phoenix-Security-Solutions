from flask import render_template, redirect, url_for,abort,request,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Crime,Comment,Upvote,Downvote
from .forms import CrimeForm,CommentForm
from .. import db,photos
from flask_login.utils import confirm_login

@main.route('/')
def index():
    crimes = Crime.query.all()
    crimes = Crime.query.order_by(Crime.time.desc())
    return render_template('index.html', crimes = crimes)

@main.route('/crime/<id>')
@login_required
def crime(id):
    crime= Crime.query.get(id)
    return render_template('crime_page.html',crime=crime )

@main.route('/new_crime', methods = ['POST','GET'])
@login_required
def new_crime():
    crime_form = CrimeForm()
    if crime_form.validate_on_submit():
        title = crime_form.title.data
        description = crime_form.security_issue_description.data
        location = crime_form.location.data
        user_id =  current_user._get_current_object().id
        crime = Crime(title=title,location=location,security_issue_description= description,user_id=user_id)
        crime.save()
        return redirect(url_for('main.index'))
        
    return render_template('crime.html', crime_form = crime_form)

@main.route('/crime/<crime_id>/update', methods = ['GET','POST'])
@login_required
def updatecrime(crime_id):
    crime = Crime.query.get(crime_id)
    if crime.user != current_user:
        abort(403)
    form = CrimeForm()
    if form.validate_on_submit():
        crime.title = form.title.data
        crime.security_issue_description = form.security_issue_description.data
        crime.location =form.location.data
        db.session.commit()
        return redirect(url_for('main.crime',id = crime.id))
    if request.method == 'GET':
        form.title.data = crime.title
        form.security_issue_description.data = crime.security_issue_description
    return render_template('edit_crime.html', form = form)
@main.route('/crime/<crime_id>/delete', methods = ['POST'])
@login_required
def delete_crime(crime_id):
    crime = Crime.query.get(crime_id)
    if crime.user != current_user:
        abort(403)
    crime.delete()
    return redirect(url_for('main.index'))


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

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
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
@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
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
    

