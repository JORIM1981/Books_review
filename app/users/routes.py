from . import users
from flask import render_template,redirect,url_for, flash,request
from app import db, bcrypt
from flask_login import login_user,logout_user,login_required, current_user
from ..models import User, Subscribe
from .forms import LoginForm,RegistrationForm,RequestResetPasswordForm, PasswordResetForm, ContactForm, ChangeEmailForm, ChangePasswordForm, UpdateAccountForm
from ..email import mail_message


@users.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        
        if user is None or not user.verify_password(login_form.password.data):
            flash('invalid username or password', 'form-error')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if next_page is None or not next_page.startswith('/'):
            next_page = url_for('main.home')
        flash("You are now logged in", 'form-success')
        return redirect(next_page)

    title = " Website login"
    return render_template('auth/login.html',form = login_form,title=title)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.home"))


@users.route('/register',methods = ["GET","POST"])
def register():
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome ","email/welcome", user.email,user=user)
        
        return redirect(url_for('users.login'))
    title = "New Account"
    return render_template('auth/register.html',form = form, title =title)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, title=f'{user.username} Posts')


@users.route('/user/<username>/update/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('users.account',username=username))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            mail_message("Reset your Password",'email/reset_password', user.email, user=user, token=token)
        flash('A password reset link has been sent to {}'.format(form.email.data), 'form-info')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_password.html', form=form, title='Password Reset')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = PasswordResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address!', 'form-error')
            return redirect(url_for('users.reset_password_request'))
    
        if user.reset_password(token, form.password.data):
            flash('Your password was successfully changed.')
            return redirect(url_for('users.login'))
        else:
            flash('The password link is invalid or has expired', 'form-error')
    return render_template('auth/reset_password.html', form=form)


@users.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("Email address has been updated!", 'form-success')
    else:
        flash("Invalid request", 'form-warning')
    return redirect(url_for('users.login'))


@users.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account', 'form-success')
    else:
        flash('The confirmation link is invalid or has expired ', 'form-error')
    return redirect(url_for('main.index'))


@users.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("your password has been updated!", 'form-success')
            return redirect(url_for('users.login'))
        else:
            flash('Invalid password', 'form-error')
    return render_template('auth/change_password.html', form=form)


@users.route('/user/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_change_email_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'email/change_email',
                       user=current_user, token=token)
            flash('A confirmation link has been sent to {}'.format(new_email),
                  'form-info')
            return redirect(url_for('users.login'))
        flash('Invalid email address', 'form-error')
    return render_template('auth/change_email.html', form=form)


@users.route('/contact')
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)


@users.route('/subscribe', methods=["GET", "POST"])
def subscribe():
    
    subscribingform = SubscribeForm()
    
    if subscribingform.validate_on_submit():
        subscribers = Subscribe(name=subscribingform.usename.data, email=subscribingform.useremail.data)

        db.session.add(subscribers)
        db.session.commit()

        mail_message("Welcome to Book Review...", "email/subscribing", subscribers.email, subscribers=subscribers)
        
        return redirect(url_for('main.index'))
        
    title = "Subscribe to get new updates"
    return render_template('auth/subscribe.html', title =title, subscribe_form=subscribingform)