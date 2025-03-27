# app/models/review.py

from mongoengine import Document, IntField, StringField, ReferenceField, DateTimeField, EnumField
from datetime import datetime
from enum import Enum

# Define an Enum for reviewer types
class ReviewerModel(Enum):
    CLIENT = "Client"
    FREELANCER = "Freelancer"

class Review(Document):
    rating = IntField(min_value=1, max_value=5, required=True)  # Star rating (1 to 5)
    comment = StringField()  # Optional feedback text
    reviewer = ReferenceField('Client', reverse_delete_rule=4)  # Who gave the review
    reviewer_model = EnumField(ReviewerModel)  # Use the defined Enum
    freelancer = ReferenceField('Freelancer', required=True)  # The freelancer receiving the review
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the review was created
    updated_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the review was updated

    meta = {'collection': 'reviews'}