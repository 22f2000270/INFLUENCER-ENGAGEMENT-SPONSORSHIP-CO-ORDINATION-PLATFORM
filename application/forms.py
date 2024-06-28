# application/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField,DateField,IntegerField,DateTimeField,SelectField,FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from application.models import Admin, Influencer, Sponsor,Campaign,AdRequest,Message,AdRequest1
from datetime import datetime
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('Username is already taken. Please choose a different one.')
class RegistrationForm1(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    industry=StringField('industry', validators=[DataRequired()])
    budget=StringField('budget', validators=[DataRequired()])
    company=StringField('company', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    def validate_username1(self, username):
        sponsor = Sponsor.query.filter_by(username1=username.data).first()
        if sponsor:
            raise ValidationError('Username is already taken. Please choose a different one.')
class RegistrationForm2(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    category=StringField('category', validators=[DataRequired()])
    niche=StringField('niche', validators=[DataRequired()])
    reach=StringField('reach', validators=[DataRequired()])
    def validate_username2(self, username):
        i = Influencer.query.filter_by(username2=username.data).first()
        if i:
            raise ValidationError('Username is already taken. Please choose a different one.')     
class campaignForm(FlaskForm):
    name = StringField('Campaign Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = IntegerField('Budget', validators=[DataRequired()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    submit = SubmitField('Create Campaign')
class AdRequestForm(FlaskForm):
    campaign_id = SelectField('Campaign ID', coerce=int, validators=[DataRequired()])
    influencer_id = StringField('Influencer ID', validators=[DataRequired()])
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        super(AdRequestForm, self).__init__(*args, **kwargs)
        self.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.all()]
class MessageForm(FlaskForm):
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
class AdRequest1Form(FlaskForm):
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
class SearchForm(FlaskForm):
    query = StringField('Search Query', validators=[DataRequired()])
    submit = SubmitField('Search')
class AdminDashboardForm(FlaskForm):
    campaign_id = SelectField('Campaign ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Search')