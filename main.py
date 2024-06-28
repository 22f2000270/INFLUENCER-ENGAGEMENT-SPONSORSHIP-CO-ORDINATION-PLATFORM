# main.py

from flask import Flask, render_template, redirect, url_for, flash,session,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from application. forms import LoginForm, AdminDashboardForm,RegistrationForm,RegistrationForm1,RegistrationForm2,campaignForm,AdRequestForm,MessageForm,AdRequest1Form,SearchForm
from application import create_app, db
from application. models import Admin, Influencer, Sponsor,Campaign,AdRequest,Message,AdRequest1
import secrets
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms. validators import DataRequired
import plotly
import plotly. graph_objs as go
import plotly. io as pio
import json
import logging

app = create_app()

app.secret_key = secrets.token_hex(16)
@app.route('/')
def index():
    return render_template('index.html')

@app. route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form. username. data
        password = form. password. data
        admin = Admin. query. filter_by(username=username). first()
        if admin and admin. password == password:
            return redirect(url_for('admin_dashboard',username=username))
        else:
            flash('Login unsuccessful. Please check username and password. ', 'danger')

    return render_template('create/login.html', form=form)

@app. route('/login1', methods=['GET', 'POST'])
def login1():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        sponsor = Sponsor.query.filter_by(username1=username). first()

        if sponsor and sponsor.password1 == password:
            flash('Login successful')
            session['user']=username
            session['spon_id']=sponsor.id
            return redirect(url_for('sponsor_dashboard', username=username)) # Redirect to admin dashboard
        else:
            flash('Login unsuccessful. Please check username and password. ', 'danger')
    return render_template('create/login1.html', form=form)
@app. route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username. data
        password = form.password. data
        i = Influencer.query.filter_by(username2=username). first()
        if i and i.password2 == password:
            flash('Login successful')
            session['username'] = username
            session['id']=i.id
            return redirect(url_for('influ_dashboard',username=username)) # redirect to admin dashboard
        else:
            flash('Login unsuccessful. Please check username and password. ', 'danger')
    return render_template('create/login2.html', form=form)

@app. route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = Admin(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
           
        return redirect(url_for('login')) #redirect to the login page
    return render_template('create/register.html', form=form)

@app. route('/register1', methods=['GET', 'POST'])
def register1():
    form = RegistrationForm1()
    if form.validate_on_submit():
        username = form.username.data
        password = form. password. data
        industry = form. industry. data
        budget = form. budget. data
        company = form. company. data
        sponsor = Sponsor(username1=username, password1=password,industry=industry, budget=budget, company=company)
        db. session. add(sponsor)
        db. session. commit()
        
        return redirect(url_for('login1')) #go back to the login page
    return render_template('create/register1. html', form=form)

@app. route('/register2', methods=['GET', 'POST'])
def register2():
    form = RegistrationForm2()
    if form.validate_on_submit():
        username = form. username. data
        password = form. password. data
        category=form. category. data
        niche=form. niche. data
        reach=form. reach. data
        i = Influencer(username2=username, password2=password,category=category,niche=niche,reach=reach)
        db. session. add(i)
        db. session. commit()
       
        return redirect(url_for('login2'))
    return render_template('create/register2.html', form=form)
@app.route('/sponsor_dashboard/<username>', methods=['GET', 'POST'])
def sponsor_dashboard(username):
    form = campaignForm()
    i = Influencer.query.all()
    spon_id=session.get('spon_id')
    s=Sponsor.query.filter_by(id=spon_id).first()
    print(spon_id)
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
    
    
    return render_template('sponsor_dashboard.html',s=s ,form=form,i=i,username=username)


@app.route('/search_influencers/<username>', methods=['GET', 'POST'])
def search_influencers(username):
    query = request.args.get('query')
    spon_id=session.get('spon_id')
    s=Sponsor.query.filter_by(id=spon_id).first()
    influencers = []
    if query:
        search = f"%{query}%"
        influencers = Influencer.query.filter(
            db.or_(
                Influencer.username2.ilike(search),
                Influencer.category.ilike(search),
                Influencer.niche.ilike(search),
                Influencer.reach.ilike(search)
            )
        ).all()
    form = campaignForm()
    return render_template('sponsor_dashboard.html', s=s,username=username,influencers=influencers, form=form)


@app.route('/Request/<int:id>', methods=['GET', 'POST'])
def Request(id):
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


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    form = AdminDashboardForm()

    # Query all campaigns to populate the select field
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.all()]

    ad_requests = []
    campaign_id = None
    
    if form.validate_on_submit():
        campaign_id = form.campaign_id.data
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
       
        flash(f'Searching for campaign ID: {campaign_id}', 'info')
        return redirect(url_for('admin_dashboard', campaign_id=campaign_id,ad_requests=ad_requests))    
    campaign_id = request.args.get('campaign_id')
    if campaign_id:
        ad_requests=AdRequest.query.filter_by(campaign_id=campaign_id).all()
    if ad_requests:
        influencers = [req.influencer.username2 for req in ad_requests]
        payment_amounts = [req.payment_amount for req in ad_requests]
        box = go.Figure()
        box.add_trace(go.Bar(
            x=influencers,
            y=payment_amounts,
            marker_color='blue'
        ))
        box.update_layout(
            title='Ad Requests for Campaign ID: {}'.format(campaign_id),
            xaxis_title='Influencers',
            yaxis_title='Payment Amount',
            barmode='group'
        )
        box_json = json.dumps(box, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        box_json = None
        
    campaigns=Campaign.query.all()
    campaign_names, campaign_budgets = [campaign.name for campaign in campaigns], [campaign.budget for campaign in campaigns]
    pri = Campaign.query.filter_by(visibility = 'private').count()
    pub=Campaign.query.filter_by(visibility = 'public').count()
    labels = ['Private', 'Public']
    values = [pri, pub]
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    pie_chart.update_layout(title='Distribution of Campaigns by Visibility')
    pie_chart_json=json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    # Plotly graph for campaigns
    campaigns_graph = go.Figure()
    campaigns_graph.add_trace(go.Bar(
        x=campaign_names,
        y=campaign_budgets,
        marker_color='blue'
    ))
    campaigns_graph.update_layout(
        title='Campaign Budgets',
        xaxis_title='Campaigns',
        yaxis_title='Budget',
        barmode='group'
    )
    campaigns_graph_json = json.dumps(campaigns_graph, cls=plotly.utils.PlotlyJSONEncoder)
  
    inf=Influencer.query.all()
    sp=Sponsor.query.all()
    return render_template('admin_dashboard.html',inf=inf,sp=sp, form=form,box_json=box_json, campaigns_graph=campaigns_graph_json,pie_chart=pie_chart_json, ad_requests=ad_requests, campaign_id=campaign_id)

@app.route('/influ_dashboard/<username>')
def influ_dashboard(username):
    username = session.get('username')
    id=session.get('id')
    ad_requests=AdRequest.query.filter_by(influencer_id=id).all()
    i=Influencer.query.filter_by(id=id).first()
    return render_template('influ_dashboard.html', i=i,username=username,ad_requests=ad_requests,id=id)
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
@app. route('/accept_ad_request1/<int:id>', methods=['POST'])
def accept_ad_request1(id):
    ad_request1 = AdRequest1. query. get_or_404(id)
    ad_request1.status = 'Accepted'
    db.session.commit()

    return redirect(url_for('campaign_status'))

@app. route('/reject_ad_request1/<int:id>', methods=['POST'])
def reject_ad_request1(id):
    ad_request1 = AdRequest1.query.get_or_404(id)
    ad_request1.status = 'Rejected'
    db.session.commit()
    id1=session.get('id1')
    return redirect(url_for('campaign_status'))
@app. route('/delete_campaign/<int:id>', methods=['POST'])
def delete_campaign(id):
    campaign = Campaign. query. get_or_404(id)
    db. session. delete(campaign)
    db. session. commit()
    return redirect(url_for('campaign_status'))
@app. route('/delete_campaign1/<int:id>', methods=['POST'])
def delete_campaign1(id):
    campaign = AdRequest. query. get_or_404(id)
    db. session. delete(campaign)
    db. session. commit()
    return redirect(url_for('campaign_status'))

@app. route('/campaign/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    campaign = Campaign. query. get_or_404(id) 
    form = campaignForm()

    if form. validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.goals = form.goals.data

        db. session. commit()

        return redirect(url_for('campaign_status'))

    form.name.data = campaign.name
    form.description.data = campaign.description
    form.start_date.data = campaign.start_date
    form.end_date.data = campaign.end_date
    form.budget.data = campaign.budget
    form.visibility.data = campaign.visibility
    form.goals.data = campaign.goals
    return render_template('edit.html', form=form, campaign=campaign)


    return redirect(url_for('campaign_status'))
@app. route('/search_public', methods=['GET', 'POST'])
def search_public():
    query = request. args. get('query')
    c = []
    if query:
        search = f"%{query}%"
        c = Campaign.query.filter(db. or_(
                Campaign.name.ilike(search),
            )
        ). all()

    return render_template('public_cam.html',c=c)
@app. route('/flag_sponsor/<int:s_id>', methods=['POST'])
def flag_sponsor(s_id):
    sponsor = Sponsor. query. get_or_404(s_id)
    sponsor.is_flagged = 'You are flagged'
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
@app. route('/flag_user/<int:id>', methods=['POST'])
def flag_user(id):
    user = Influencer. query. get_or_404(id)
    user. is_flagged = 'You are flagged.'
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
if __name__ == '__main__':
    app. run(debug=True)