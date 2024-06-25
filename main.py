# main.py

from flask import Flask, render_template, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from application.forms import LoginForm, RegistrationForm,RegistrationForm1,RegistrationForm2,campaignForm,AdRequestForm,MessageForm,AdRequest1Form
from application import create_app, db
from application.models import Admin, Influencer, Sponsor,Campaign,AdRequest,Message,AdRequest1
import secrets
from datetime import datetime

# Create the Flask application
app = create_app()

app.secret_key = secrets.token_hex(16)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            flash('Login successful')
            return redirect(url_for('admin_dashboard',username=username))  # Redirect to admin dashboard
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('create/login.html', form=form)
@app.route('/login1', methods=['GET', 'POST'])
def login1():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        sponsor = Sponsor.query.filter_by(username1=username).first()
        
        if sponsor and sponsor.password1 == password:
            flash('Login successful')
            session['user']=username
            session['spon_id']=sponsor.id
            return redirect(url_for('sponsor_dashboard',username=username))  # Redirect to admin dashboard
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('create/login1.html', form=form)
@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        i = Influencer.query.filter_by(username2=username).first()
        if i and i.password2 == password:
            flash('Login successful')
            session['username'] = username
            session['id']=i.id
            return redirect(url_for('influ_dashboard',username=username))  # Redirect to admin dashboard
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('create/login2.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = Admin(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page
    return render_template('create/register.html', form=form)

@app.route('/register1', methods=['GET', 'POST'])
def register1():
    form = RegistrationForm1()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        industry = form.industry.data
        budget = form.budget.data
        company = form.company.data
        sponsor = Sponsor(username1=username, password1=password,industry=industry, budget=budget, company=company)
        db.session.add(sponsor)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login1'))  # Redirect to login page
    return render_template('create/register1.html', form=form)

@app.route('/register2', methods=['GET', 'POST'])
def register2():
    form = RegistrationForm2()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        category=form.category.data
        niche=form.niche.data
        reach=form.reach.data
        i = Influencer(username2=username, password2=password,category=category,niche=niche,reach=reach)
        db.session.add(i)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login2'))  # Redirect to login page
    return render_template('create/register2.html', form=form)
@app.route('/sponsor_dashboard/<username>', methods=['GET', 'POST'])
def sponsor_dashboard(username):
    form = campaignForm()
    i = Influencer.query.all()
    spon_id=session.get('spon_id')
    if form.validate_on_submit():   
        new_campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data,
            sponsor_id=spon_id
        )
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('sponsor_dashboard',username=session.get('user')))
        
    return render_template('sponsor_dashboard.html', form=form,i=i,username=username)
@app.route('/Request/<int:id>', methods=['GET', 'POST'])
def request(id):
    form=AdRequestForm()
    spon_id=session.get('spon_id')
    campaigns=Campaign.query.filter_by(sponsor_id=spon_id).all()
    if form.validate_on_submit():
        new_ad_request = AdRequest(
            campaign_id=form.campaign_id.data,
            influencer_id=id,  # assuming 'id' is the influencer ID passed in the URL
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status=form.status.data
        )
        db.session.add(new_ad_request)
        db.session.commit()
        flash('Ad request submitted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('Request.html',id=id,form=form,campaigns=campaigns)
    
@app.route('/dashboard')
@app.route('/dashboard/<username>')
def admin_dashboard(username=None):
    if username:
        return render_template('admin_dashboard.html', username=username)
    else:
        # Handle case where username is not provided (e.g., user not logged in)
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
@app.route('/influ_dashboard/<username>')
def influ_dashboard(username):
    username = session.get('username')
    id=session.get('id')
    ad_requests=AdRequest.query.filter_by(influencer_id=id).all()
    return render_template('influ_dashboard.html', username=username,ad_requests=ad_requests,id=id)
@app.route('/public_cam', methods=['GET'])
def public_cam():
    id=session.get('id')
    m=AdRequest1.query.filter_by(influencer_id=id).all()
    public_campaigns = Campaign.query.filter_by(visibility='public').all()
    return render_template('public_cam.html', campaigns=public_campaigns,m=m)
@app.route('/accept_ad_request/<int:id>', methods=['POST'])
def accept_ad_request(id):
    ad_request = AdRequest.query.get_or_404(id)
    ad_request.status = 'Accepted'
    db.session.commit()
    
    flash('Ad request accepted successfully!', 'success')
    return redirect(url_for('influ_dashboard',username=session.get('username')))
@app.route('/reject_ad_request/<int:id>', methods=['POST'])
def reject_ad_request(id):
    ad_request = AdRequest.query.get_or_404(id)
    ad_request.status = 'Rejected'
    db.session.commit()
    
    flash('Ad request rejected successfully!', 'success')
    return redirect(url_for('influ_dashboard',username=session.get('username')))
@app.route('/info/<int:id>', methods=['GET','POST'])
def info(id):
    form=MessageForm()
    c=Campaign.query.filter_by(id=id).first()
    influencer_id = session.get('id')
    if form.validate_on_submit():
        influencer_id = session.get('id')
        msg=Message( 
            ad_id=id,
            influencer_id=influencer_id,
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('info',id=id))
        
    return render_template('info.html',c=c,form=form,id=id)
@app.route('/campaign_status', methods=['GET', 'POST'])
def campaign_status():
    username=session.get('user')
    spon_id=session.get('spon_id')
    campaigns = Campaign.query.filter_by(sponsor_id=spon_id).all() # Assuming Campaign is your model class
    return render_template('campaign_status.html', campaigns=campaigns,username=username)
@app.route('/campaign_status1/<int:id>', methods=['GET', 'POST'])
def campaign_status1(id):
    username=session.get('user')
    session['id1']=id
    a=AdRequest.query.filter_by(campaign_id=id).all()
    b=AdRequest1.query.filter_by(campaign_id=id).all()
    return render_template('campaign_status1.html', username=username,a=a,b=b)
@app.route('/request_status/<int:id>', methods=['GET', 'POST'])
def request_status(id):
    form=AdRequest1Form()
    if form.validate_on_submit():
        influencer_id = session.get('id')
        msg=AdRequest1( 
            campaign_id=id,
            influencer_id=influencer_id,
            message=form.message.data,
            status="pending"
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('request_status',id=id))
        
    return render_template('request_status.html',form=form,id=id)
@app.route('/accept_ad_request1/<int:id>', methods=['POST'])
def accept_ad_request1(id):
    ad_request1 = AdRequest1.query.get_or_404(id)
    ad_request1.status = 'Accepted'
    db.session.commit()
    flash('Ad request accepted successfully!', 'success')
    return redirect(url_for('campaign_status'))

@app.route('/reject_ad_request1/<int:id>', methods=['POST'])
def reject_ad_request1(id):
    ad_request1 = AdRequest1.query.get_or_404(id)
    ad_request1.status = 'Rejected'
    db.session.commit()
    id1=session.get('id1')
    flash('Ad request rejected successfully!', 'success')
    return redirect(url_for('campaign_status'))
@app.route('/delete_campaign/<int:id>', methods=['POST'])
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    ad_requests1 = AdRequest1.query.filter_by(campaign_id=id).all()
    ad_requests = AdRequest.query.filter_by(campaign_id=id).all()
    
    try:
        for ad_request1 in ad_requests1:
            db.session.delete(ad_request1)
        
        for ad_request in ad_requests:
            db.session.delete(ad_request)
        
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign and associated requests deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting campaign: {str(e)}', 'danger')
    
    return redirect(url_for('campaign_status'))
if __name__ == '__main__':
    app.run(debug=True)
