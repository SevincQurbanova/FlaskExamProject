from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])     
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    # Şifrə mürəkkəbliyini yoxlamaq üçün xüsusi bir metod
    def validate_password(self, field):
        password = field.data
        
        # Şifrənin ən azı 8 simvol olmasını yoxlayırıq
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        # Ən azı bir ədədi simvol olub-olmamasını yoxlayırıq
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')

        # Ən azı bir kiçik hərf olub-olmamasını yoxlayırıq
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')

        # Ən azı bir böyük hərf olub-olmamasını yoxlayırıq
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')

        # @#$ simvollarından ən azı birinin olub-olmamasını yoxlayırıq
        if not re.search(r'[@#$]', password):
            raise ValidationError('Password must contain at least one special character (@, #, or $).')