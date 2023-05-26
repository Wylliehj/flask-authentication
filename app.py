from flask import Flask, render_template, request, flash, redirect, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

db.create_all()

@app.route('/')
def root():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def handle_register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        try:
            new_user = User.register(username, password, email, first_name, last_name)

            db.session.add(new_user)
            db.session.commit()

            session['user'] = new_user.username 

            return redirect(f'/user/{username}')

        except:
            db.session.rollback()
            flash('Email or username already in use.')

            return render_template('register.html', form=form)         


    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    form = LoginForm()

    if 'user' in session:
        return redirect(f'/user/{session["user"]}')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        auth_user = User.authenticate(username, password)

        if auth_user:
            session['user'] = username
            return redirect(f'/user/{username}')

        else:
            form.username.errors = ['Username or password incorrect']
        
    return render_template('login.html', form=form)


@app.route('/user/<username>')
def show_secret(username):
    
    try:
        if session['user'] == username:
            user = User.query.get_or_404(username)

            return render_template('secret.html', user=user)

    except:
        return redirect('/login')


@app.route('/logout')
def handle_logout():
    session.clear()
    return redirect('/')


@app.route('/user/<username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):

    form = FeedbackForm()

    if 'user' in session:
        if session['user'] == username:
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data

                add_feedback = Feedback(title=title, content=content, username=username)

                db.session.add(add_feedback)
                db.session.commit()
                return redirect(f'/user/{username}')
            return render_template('feedback.html', form=form)
        return redirect(f'/user/{username}')

    return redirect('/login')

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def handle_update(feedback_id):

    form = FeedbackForm()

    feedback = Feedback.query.get_or_404(feedback_id)

    if 'user' in session:
        if session['user'] == username:
            if form.validate_on_submit():

                feedback.title = form.title.data
                feedback.content = form.content.data

                db.session.add(feedback)
                db.session.commit()

                return redirect(f'/user/{feedback.username}')
            return render_template('update.html', form=form, feedback=feedback)
        return redirect(f'/user/{session["user"]}')
    return redirect('/')


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username

    if 'user' in session:
        if session['user'] == username:
            Feedback.query.filter_by(id=feedback_id).delete()
            db.session.commit()

            return redirect(f'/user/{username}')
        return redirect('/register')
    return redirect(f'/user/{username}')
