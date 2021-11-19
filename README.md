# Title
Phoenix Security Solutions(PSS)

# Description
The primary goal of this project is to present a credible platform whereby any one with a suggestion on how a particular crime can be subverted to bring up the idea. Other people with access to the application can up-vote or down-vote the proposed solution and based on the feasibility of the idea and the number of votes, the relevant authorities can act on the suggestions.

## Features
As a user of the web application you will be able to:

Create an account
Log in
Create an idea
Comment on an idea
See comments given on an idea.
Edit your profile i.e will be able to add a short bio about yourself and a profile picture.

## Getting started
python3.8
virtual environment
pip

Cloning
In your terminal:
$ git clone git@github.com:ezekielkibiego/Phoenix-Security-Solutions.git

## Running the Application
Install virtual environment using $ python3.8 -m venv --without-pip virtual

Activate virtual environment using $ source virtual/bin/activate

Download pip in our environment using $ curl https://bootstrap.pypa.io/get-pip.py | python

Install all the dependencies from the requirements.txt file by running python3.6 pip install -r requirements.txt

Create a start.sh file in the root of the folder and add the following code:

 export MAIL_USERNAME=<your-email-address>
 export MAIL_PASSWORD=<your-email-password>
 export SECRET_KEY=<your-secret-key>
 Edit the configuration instance in manage.py by commenting on production instance and un commenting development instanceEdit the configuration instance in manage.py by commenting on production instance and un commenting development instance

 To run the application, in your terminal:

  $ chmod a+x start.sh
  $ ./start.sh
Testing the Application
To run the tests for the class file:

  $ python3.8 manage.py server

  ## Technologies Used
  Python3.8
  Flask
  HTML
  Bootstrap
This application is developed using Python3.8, Flask, HTML and Bootstrap

## live link:




