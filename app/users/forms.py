from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Length, Required, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email:',validators=[Required(), Email(),Length(1, 64)], render_kw={"placeholder": "Enter your email address"})
    username = StringField('Enter your username',validators = [Required()], render_kw={"placeholder": "Prefered Username"})
    password = PasswordField('Password:',validators = [Required(), EqualTo('confirm_password',message = 'Passwords must match')], render_kw={"placeholder": "Prefered password"})
    confirm_password = PasswordField('Confirm Password:',validators = [Required()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
                if User.query.filter_by(email =data_field.data).first():
                    raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[Required(),Email(),Length(1, 64) ], render_kw={"placeholder": "e.g janedoe@Blogtoday.com"})
    password = PasswordField('Password:',validators =[Required()], render_kw={"placeholder": "Your password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('LogIn')


class UpdateAccountForm(FlaskForm):
    username = StringField('Enter your username',validators = [Required()], render_kw={"placeholder": "Prefered Username"})
    email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    picture = SelectField()
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email(), Length(1, 64)])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm new Password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm new Password', validators=[Required()])
    submit = SubmitField('Update password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already in use!")  


class ContactForm(FlaskForm):
    name = StringField('Name: ', validators=[Required()])
    email = StringField('Email: ', validators=[Required(), Email()])
    subject = StringField('Subject: ', validators=[Required()])
    message = TextAreaField('Message:', validators=[Required()])
    submit = SubmitField('Send')


class SubscribeForm(FlaskForm):
    usename = StringField('Enter your username', validators=[Required()])
    useremail = StringField('Enter your Email Address', validators=[Required(), Email()])
    submit = SubmitField('Subscribe')


    def validate_useremail(self, data_field):
        if Subscribe.query.filter_by(email=data_field.data).first():
            raise ValidationError('There is an account with that email')
