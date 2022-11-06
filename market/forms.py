from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    # def validate_username(self, username_to_check):
    #     user = User.query.filter_by(username=username_to_check).first()
    #     if user:
    #         raise ValidationError('Username already exist Please try a different username')
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    def validate_phone_num(self, phone_num_to_check):
        number = User.query.filter_by(phone_number=phone_num_to_check.data).first()
        if number:
            raise ValidationError('Phone number already used Please try using a different phone number ')        

    username = StringField(label='First Name:', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='Last Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    phone_num = StringField(label='Phone Number:', validators=[Length(min=2, max=30), DataRequired()])
    # house_address = StringField(label='House Address:', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Log In')


class WriteBlogs(FlaskForm):
    blog_title =  StringField(label='Blog Tiltle:', validators=[DataRequired()])
    blog_content =  StringField(label='Blog Content:', validators=[DataRequired()])
    submit = SubmitField(label='Upload')
