# app/models/client.py

from mongoengine import Document, StringField, ListField, ReferenceField, IntField, EmbeddedDocumentField, EmbeddedDocument

class Location(EmbeddedDocument):
    city = StringField()
    state = StringField()
    country = StringField()
    pincode = StringField()

class Client(Document):
    first_name = StringField(required=False)
    last_name = StringField(required=False)
    username = StringField(required=True, unique=True)
    company_name = StringField()
    profile_photo = StringField()  # Image URL
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    location = EmbeddedDocumentField(Location)
    category = StringField()  # Industry category
    description = StringField()
    credits = IntField(default=0)  # Platform credits
    projects = ListField(ReferenceField('Project'))
    reviews = ListField(ReferenceField('Review'))
    phone_number = StringField()
    instagram_link = StringField()
    linkedin_link = StringField()
    transaction_history = ListField(ReferenceField('Transaction'))
    agreements = ListField(ReferenceField('Agreement'))

    meta = {'collection': 'clients'}