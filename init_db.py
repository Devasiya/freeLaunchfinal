# init_db.py

from app import app, db
from app.models.client import Client
from app.models.freelancer import Freelancer
from app.models.project import Project
from app.models.review import Review
from app.models.agreement import Agreement

# Initialize the Flask application
with app.app_context():
    # Drop existing collections (optional)
    db.get_db().drop_collection('clients')
    db.get_db().drop_collection('freelancers')
    db.get_db().drop_collection('projects')
    db.get_db().drop_collection('reviews')
    db.get_db().drop_collection('agreements')

    # Create sample clients
    client1 = Client(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        company_name="Doe Enterprises",
        email="john@example.com",
        password="password123",
        location={"city": "New York", "state": "NY", "country": "USA", "pincode": "10001"},
        category="Technology",
        description="A tech company specializing in software development.",
        credits=100
    )
    client1.save()

    client2 = Client(
        first_name="Jane",
        last_name="Smith",
        username="janesmith",
        company_name="Smith Solutions",
        email="jane@example.com",
        password="password123",
        location={"city": "Los Angeles", "state": "CA", "country": "USA", "pincode": "90001"},
        category="Marketing",
        description="A marketing agency focused on digital marketing.",
        credits=200
    )
    client2.save()

    # Create sample freelancers
    freelancer1 = Freelancer(
        first_name="Alice",
        last_name="Johnson",
        username="alicejohnson",
        email="alice@example.com",
        password="password123",
        location={"city": "San Francisco", "state": "CA", "country": "USA", "pincode": "94101"},
        experience="5 years",
        description="Freelance web developer.",
        credits=50,
        skills=["HTML", "CSS", "JavaScript"]
    )
    freelancer1.save()

    # Create sample projects
    project1 = Project(
        title="Website Development",
        description="Develop a responsive website for a client.",
        budget=5000,
        deadline="2023-12-31",
        status="Open",
        categories=["Web Development", "Design"],
        client=client1,
        assigned_freelancer=freelancer1
    )
    project1.save()

    # Create sample reviews
    review1 = Review(
        rating=5,
        comment="Excellent work!",
        reviewer=client1,
        reviewer_model="Client",
        freelancer=freelancer1
    )
    review1.save()

    # Create sample agreements
    agreement1 = Agreement(
        title="Web Development Agreement",
        description="Agreement for the development of a website.",
        client=client1,
        freelancer=freelancer1,
        project=project1,
        status="Active"
    )
    agreement1.save()

    print("Database initialized with sample data.")