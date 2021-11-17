from flask import render_template, redirect, url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Crime,Comment,Upvote,Downvote
from .forms import CrimeForm
from .. import db,photos

@main.route('/')
def index():
    # crimes = Crime.query.all()
    crimes = Crime.query.order_by(Crime.time.desc())
    return render_template('index.html', crimes = crimes)

@main.route('/crime/<id>')
# @login_required
def crime(id):
    crime= Crime.query.get(id)
    return render_template('crime_page.html',crime=crime )

@main.route('/new_crime', methods = ['POST','GET'])
# @login_required
def new_crime():
    crime_form = CrimeForm()
    if crime_form.validate_on_submit():
        title = crime_form.title.data
        description = crime_form.security_issue_description.data
        location = crime_form.location.data
        # user_id =  current_user._get_current_object().id
        crime = Crime(title=title,location=location,security_issue_description= description)
        crime.save()
        return redirect(url_for('main.index'))
        
    return render_template('crime.html', crime_form = crime_form)
    

@main.route('/crime/<crime_id>/update', methods = ['GET','POST'])
# @login_required
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
# @login_required
def delete_post(crime_id):
    crime = Crime.query.get(crime_id)
    if crime.user != current_user:
        abort(403)
    crime.delete()
    return redirect(url_for('main.index'))