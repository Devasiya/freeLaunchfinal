# app/models/freelancer.py

from mongoengine import Document, StringField, ListField, ReferenceField, IntField, EmbeddedDocumentField
from app.models.client import Location  # Ensure you import Location if it's defined in client.py

class Freelancer(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    profile_photo = StringField()  # Image URL
    location = EmbeddedDocumentField(Location)  # Ensure Location is defined and imported
    experience = StringField()  # Years of experience
    reviews = ListField(ReferenceField('Review'))
    description = StringField()
    credits = IntField(default=0)  # Platform credits
    projects = ListField(ReferenceField('Project'))
    phone_number = StringField()
    instagram_link = StringField()
    linkedin_link = StringField()
    skills = ListField(StringField())  # List of skills
    applied_projects = ListField(ReferenceField('Project'))
    earnings = IntField(default=0)
    transaction_history = ListField(ReferenceField('Transaction'))

    meta = {'collection': 'freelancers'}