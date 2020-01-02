import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from ecosystem import app, db, bcrypt
from ecosystem.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, EventForm, CreatePollForm, VoteForm, SearchForm, FoundItemForm
from ecosystem.models import User, Post, Event, Poll, Item
from flask_login import login_user, current_user, logout_user, login_required

db.create_all()

@app.route("/announcements")
def home():
    posts = Post.query.all()
    return render_template('announcements.html', posts=posts)


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, name=form.name.data, apt_no = form.apt_no.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} resident of {form.apt_no.data}')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful please check username and password')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    '''form = UpdateAccountForm()
    if(request.method == 'POST'):
        if(form.validate_on_submit()):
            current_user.username = form.username.data
            current_user.apt_no = form.apt_no.data
            db.session.commit()
            flash('You account has been updated')
            return redirect(url_for('account'))
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.apt_no.data = current_user.apt_no'''
    return render_template('account.html', title='Account')

@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if(form.validate_on_submit()):
        post = Post(title=form.title.data, content=form.content.data, author=current_user, anonymity = form.go_anonymous.data)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form, legend='Create Post')

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.author!=current_user ):
        abort(403)
    form = PostForm()
    if(form.validate_on_submit()):
        post.title = form.title.data
        post.content = form.content.data
        post.anonymity = form.go_anonymous.data
        db.session.commit()
        flash('Your post has been updated')
        return redirect(url_for('post', post_id = post.id))
    elif(request.method == 'GET'):
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if(post.author!=current_user and current_user.username != 'admin'):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted')
    return redirect(url_for('home'))

@app.route("/new")
@login_required
def new():
    return render_template('new.html', title='Create New')

@app.route("/events")
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@app.route("/events/new", methods = ['GET', 'POST'])
def new_event():
    form = EventForm()
    if(form.validate_on_submit()):
        event = Event(category=form.category.data,date_of_event= form.date_of_event.data,  content=form.content.data, author=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Your Event has been posted!')
        return redirect(url_for('events'))
    return render_template('create_event.html', form=form, legend='Update Post')

@app.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', title=event.date_of_event, event=event)

@app.route("/event/<int:event_id>/update", methods = ['GET', 'POST'])
@login_required
def updateevent(event_id):
    event = Event.query.get_or_404(event_id)
    if(event.author!=current_user):
        abort(403)
    form = EventForm()
    if(form.validate_on_submit()):
        event.category = form.category.data
        event.date_of_event = form.date_of_event.data
        event.content = event.content.data
        db.session.commit()
        flash('Your event has been updated')
        return redirect(url_for('event', event_id = event.id))
    elif(request.method == 'GET'):
        form.category.data = event.category
        form.date_of_event = event.date_of_event
        form.content.data = event.content
    return render_template('create_event.html', title='Update Event', form=form, legend='Event Post', event=event)

@app.route("/event/<int:event_id>/delete", methods = ['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if(event.author != current_user):
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been Cancelled')
    return redirect(url_for('home'))

@app.route("/createpolls", methods=['GET', 'POST'])
@login_required
def create_poll():
    form = CreatePollForm()
    if(form.validate_on_submit()):
        poll = Poll(content = form.content.data, option1 = form.option1.data, option2 = form.option2.data, votes_1=0, votes_2=0, author = current_user)
        db.session.add(poll)
        db.session.commit()
        flash('Your Poll has been created')
        return redirect(url_for('view_polls'))
    return render_template('create_poll.html', legend= 'Create Poll', form=form)

@app.route("/view_polls", methods=['GET', 'POST'])
def view_polls():
    polls = Poll.query.all()
    return render_template('viewpolls.html', polls=polls)

@app.route("/view_polls/<int:poll_id>", methods=['GET', 'POST'])
@login_required
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    polls = Poll.query.all()
    #poll_id = poll.id
    form = VoteForm()
    if(form.validate_on_submit()):
        if(form.vote_1.data == 1 and form.vote_2.data == 1):
            flash('You cannot vote for both the options')
            return redirect(url_for('vote', poll_id=poll.id)) 
        elif(form.vote_1.data == 1 and form.vote_2.data == 0):
            poll.votes_1+=1
            db.session.commit()
        elif(form.vote_2.data == 1 and form.vote_1.data == 0):
            poll.votes_2+=1
            db.session.commit()
        else:
            flash('Invalid Vote please vote again', 'danger')
            return redirect(url_for('vote', poll_id=poll.id))
        flash('You have voted')
        return redirect(url_for('view_polls'))
    return render_template('vote.html', poll = poll, form=form, legend='Vote Form')


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    
    if(form.validate_on_submit()):
        apt_no = form.search.data
        user = User.query.filter_by(apt_no=apt_no).first()
        posts = Post.query.filter_by(author=user).all()
        events = Event.query.filter_by(author=user).all()
        polls = Poll.query.filter_by(author=user).all()
        return render_template('searchreturn.html', posts=posts, events=events, polls=polls)
    return render_template('search.html', form=form) 

'''def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.spilltext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/item_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn'''

@app.route("/listfound")
def listfound():
    items = Item.query.all()
    return render_template('founditems.html', items=items)


@app.route("/reportfound", methods=['GET', 'POST'])
def reportfound():
    form = FoundItemForm()
    if(form.validate_on_submit()):
        item = Item(description = form.description.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('listfound'))
    items = Item.query.all()
    return render_template('reportfound.html', form=form, items=items)


        






    