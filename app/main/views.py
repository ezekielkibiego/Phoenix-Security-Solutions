from flask import render_template, request, redirect, url_for, abort,flash
from . import main
from flask_login import login_required, current_user
from .. import db, photos
from ..models import User,Crime,Comment,Upvote,Downvote
from .forms import CrimeForm,CommentForm,UpdateProfile
from flask_login.utils import confirm_login

@main.route('/')
def index():
    crimes = Crime.query.all()
    crimes = Crime.query.order_by(Crime.time.desc())
    return render_template('index.html', crimes = crimes)

@main.route('/crime/')
@login_required
def crime():
    crime= Crime.query.all()
    return render_template('display_crimes.html',crimes=crime )

@main.route('/new_crime', methods = ['POST','GET'])
@login_required
def new_crime():
    crime_form = CrimeForm()
    if crime_form.validate_on_submit():
        title = crime_form.title.data
        description = crime_form.security_issue_description.data
        location = crime_form.location.data
        user_id =  current_user.id
        crime = Crime(title=title,location=location,security_issue_description= description,user_id=user_id)
        crime.save()
        return redirect(url_for('main.crime'))
        
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
            proposed_solution=form.proposed_solution.data,
            crime_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.proposed_solution.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comments.html', crime=crimes, comment=comments, comment_form=form)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.user_bio = form.bio.data
        user.email=form.email.data
        user.username=form.username.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username,  user=user))
    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname, user = user))

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    comment = Comment.query.get(id)
    if comment is None:
        abort(404)
    like = Upvote.query.filter_by(user_id=current_user.id, comment_id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unupvoted!')
        return redirect(url_for('main.crime_details'))
    new_like = Upvote(
        user_id=current_user.id,
        comment_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully upvoted the pitch!')
    return redirect(url_for('main.crime_details'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    comments = Comment.query.get(id)
    if comments is None:
        abort(404)
    
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, comment_id=id).first()
    if dislike is not None:
       
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully undownvoted!')
        return redirect(url_for('main.crime_details'))

    new_dislike = Downvote(
        user_id=current_user.id,
        comment_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully downvoted!')
    return redirect(url_for('main.crime_details'))
