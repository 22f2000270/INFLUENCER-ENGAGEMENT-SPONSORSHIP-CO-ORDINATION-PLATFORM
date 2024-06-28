from application.database import db
from datetime import datetime
from flask_wtf import FlaskForm
class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

class Influencer(db.Model):
    __tablename__ = 'influencer'

    id = db.Column(db.Integer, primary_key=True)
    username2 = db.Column(db.String(100), nullable=False)
    password2 = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String, nullable=True)
    niche = db.Column(db.String, nullable=True)
    reach = db.Column(db.Integer, nullable=True)
    is_flagged = db.Column(db.String, nullable=True, default=None)
    
class Sponsor(db.Model):
    __tablename__ = 'sponsor'

    id = db.Column(db.Integer, primary_key=True)
    username1 = db.Column(db.String(100), nullable=False)
    password1 = db.Column(db.String(100), nullable=False)
    industry=db.Column(db.String, nullable=True)
    budget=db.Column(db.Integer, nullable=True)
    company=db.Column(db.String, nullable=True)
    is_flagged = db.Column(db.String, nullable=True, default=None)
class Campaign(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    visibility = db.Column(db.String(10), nullable=True)
    goals = db.Column(db.Text, nullable=True)
    sponsor_id=db.Column(db.Integer,db.ForeignKey('sponsor.id'), nullable=True)

class AdRequest(db.Model):
    __tablename__ = 'ad_request'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id', ondelete='CASCADE'), nullable=False)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='Pending')

    # Define relationships
    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', lazy=True,cascade='all, delete-orphan'))
    influencer = db.relationship('Influencer', backref=db.backref('ad_requests', lazy=True))
    
    m=db.relationship('Message',backref='a',cascade='all, delete-orphan')
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad_request.id', ondelete='CASCADE'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
class AdRequest1(db.Model):
    __tablename__ = 'ad_request1'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)

    campaign = db.relationship('Campaign', backref=db.backref('ad_requests1', lazy=True, cascade='all, delete-orphan'))
    influencer = db.relationship('Influencer', backref=db.backref('ad_requests1', lazy=True))
