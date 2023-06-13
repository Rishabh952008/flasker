from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # to keep track of when  they are added

## Validators 
# DataRequired
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID(Unique User Identification Number)
# AnyOf
# NoneOf

# create a flask instance 
app = Flask(__name__)

#Add a database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.db'
#Secret Key
app.config['SECRET_KEY']="rishabh@952008"

# Now we need to initialize the database
db = SQLAlchemy(app)

# Let's Create the Model what do we want to save in the database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    date_added = db.Column(db.DateTime , default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return '<Name %r' % self.name

#lets create a form class 
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    # BooleanField
    # DateField
    # DateTimeField
    # FileField
    # HiddenField
    # MultipleField
    # FieldList
    # FloatField
    # FormField
    # IntegerField
    # PasswordField
    # RadioField
    # SelectField
    # SelectMultipleField
    # SubmitField
    # StringField
    # TextAreaField

# we can now use this form on webpage whenever i want



@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # add the new guy to the database
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        flash("User Added Successfully!")    
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form=form,
                           name=name,
                           our_users=our_users)


# Create a route decorator
@app.route('/')
def index():
    first_name="Rishabh"
    favorite_pizza =['burger','chocolate']
    return render_template("index.html",first_name=first_name,favorite_pizza=favorite_pizza)

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name): 
    return render_template("user.html",user_name=name)

## Create Custom Error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#Internal Server error thing
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500


# create name page
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = UserForm()
    #validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data =''
        flash("Form Submitted Successfully")
    return render_template('name.html',
                           name=name,
                           form=form)