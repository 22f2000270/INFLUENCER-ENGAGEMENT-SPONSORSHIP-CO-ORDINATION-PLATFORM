# Example usage in a controller function

from application.models import Admin, Influencer, Sponsor
from application.database import db

def create_admin(username, password):
    admin = Admin(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
    return admin

def create_influencer(username, password):
    influencer = Influencer(username2=username, password2=password)
    db.session.add(influencer)
    db.session.commit()
    return influencer

def create_sponsor(username, password):
    sponsor = Sponsor(username1=username, password1=password)
    db.session.add(sponsor)
    db.session.commit()
    return sponsor

# Implement other CRUD operations as needed
