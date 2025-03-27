# app/models/agreement.py

from mongoengine import Document, StringField, ReferenceField, DateTimeField, EnumField
from datetime import datetime
from enum import Enum

# Define an Enum for agreement status
class AgreementStatus(Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"

class Agreement(Document):
    title = StringField(required=True)  # Title of the agreement
    description = StringField()  # Detailed description of the agreement
    client = ReferenceField('Client', required=True)  # Client involved in the agreement
    freelancer = ReferenceField('Freelancer', required=True)  # Freelancer involved in the agreement
    project = ReferenceField('Project', required=True)  # Project associated with the agreement
    status = EnumField(AgreementStatus)  # Use the defined Enum
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the agreement was created
    updated_at = DateTimeField(default=datetime.utcnow)  # Timestamp for when the agreement was updated

    meta = {'collection': 'agreements'}