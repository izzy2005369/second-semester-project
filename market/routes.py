from market import app
from market.models import User, Blogs
from flask import render_template,  redirect, url_for, flash, request, session
from market.forms import RegisterForm,LoginForm, WriteBlogs
from market import db
from flask_login import login_user, logout_user
import time

@app.route('/')
@app.route('/home')
def home_page():
    blogs = Blogs.query.all()
    return render_template('home.html', blogs = blogs)

@app.route('/Login', methods=['GET', 'POST'])
def Login_page():
    logform = LoginForm()  
    if logform.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=logform.username.data).first()
        me = logform.username.data
        session["username"] = me
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=logform.password1.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('blogs_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=logform)  


@app.route('/Register', methods=['GET', 'POST'])
def Register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              lastname=form.lastname.data,
                              email_address=form.email_address.data,
                              phone_number=form.phone_num.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit() 
        flash(f'Account successfully created! Now logged in to your acount', category='success')
        return redirect(url_for('Login_page'))

    if form.errors != {}: #If there are not errors from the validations
           for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)
 
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/signedblog', methods=['GET', 'POST'])
def blogs_page():
    blogs = Blogs.query.all()
    return render_template('signedblog.html', blog=blogs)

@app.route('/writeblog', methods=['GET', 'POST'] )
def wblogs():
    localtime = time.asctime( time.localtime(time.time()) )
    form = WriteBlogs()
    if "username" in session:
            oruko = session["username"]
            surname = User.query.filter_by(email_address=oruko).first()
            surn = surname.username
            last = surname.lastname
            realname = surn +' '+last
            
    if form.validate_on_submit():
        
        blog_to_create = Blogs(name=realname,
                               blog_title=form.blog_title.data,
                               blog_content=form.blog_content.data,
                               time = localtime)

        db.session.add(blog_to_create)
        db.session.commit()
        return redirect(url_for('blogs_page'))
    return render_template('writeblog.html', localtime=localtime, form = form)

@app.route('/editblog/<int:id>/', methods=['GET', 'POST'])    
def edit(id):
    blog_to_update = Blogs.query.get_or_404(id)       
    if request.method == "POST":
        
        
        blog_to_update.blog_title = request.form.get('blog_title')
        blog_to_update.blog_content = request.form.get('blog_content')

        db.session.commit()
        return redirect(url_for('blogs_page'))
    return render_template('editblog.html', blo =blog_to_update)   

@app.route('/deleteblog/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    blog_to_delete = Blogs.query.get_or_404(id)

    db.session.delete(blog_to_delete)
    db.session.commit()
    return redirect(url_for('blogs_page'))

@app.route('/about')
def about_page():
    # items = Item.query.all()
    return render_template('about.html')    