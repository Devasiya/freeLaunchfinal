# app/models/project.py

from mongoengine import Document, StringField, ListField, ReferenceField, IntField, DateTimeField
from datetime import datetime

class Project(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    budget = IntField(required=True)
    deadline = DateTimeField(required=True)
    status = StringField(choices=["Open", "In Progress", "Completed", "Cancelled"], default="Open")
    categories = ListField(StringField())  # Array of categories
    client = ReferenceField('Client')
    assigned_freelancer = ReferenceField('Freelancer')
    reviews = ListField(ReferenceField('Review'))
    agreement = ReferenceField('Agreement')
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the project was created
    updated_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the project was updated

    meta = {'collection': 'projects'}