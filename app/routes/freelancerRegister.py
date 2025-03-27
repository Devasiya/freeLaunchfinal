# app/routes/freelancerRoutes.py

from flask import Blueprint, render_template, request, redirect, flash, jsonify
from app.models.freelancer import Freelancer
from app.models.projects import Project
from app.models.reviews import Review
from mongoengine import DoesNotExist

freelancer_bp = Blueprint('freelancer', __name__)

# GET: Show all freelancers
@freelancer_bp.route("/", methods=["GET"])
def show_freelancers():
    try:
        freelancers = Freelancer.objects()
        return render_template("freelancers/index.html", freelancers=freelancers, title="All Freelancers")
    except Exception as e:
        flash("Error fetching freelancers", "error")
        return redirect("/")

# GET: Show single freelancer
@freelancer_bp.route("/<freelancer_id>", methods=["GET"])
def show_freelancer(freelancer_id):
    try:
        freelancer = Freelancer.objects.get(id=freelancer_id).populate("projects")
        return render_template("freelancers/show.html", freelancer=freelancer, title=f"{freelancer.first_name} {freelancer.last_name}")
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error fetching freelancer details", "error")
        return redirect("/api/freelancers")

# GET: Freelancer edit form
@freelancer_bp.route("/<freelancer_id>/edit", methods=["GET"])
def edit_freelancer(freelancer_id):
    try:
        freelancer = Freelancer.objects.get(id=freelancer_id)
        return render_template("freelancers/edit.html", freelancer=freelancer, title="Edit Freelancer")
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error loading edit page", "error")
        return redirect("/api/freelancers")

# PUT: Update freelancer details
@freelancer_bp.route("/<freelancer_id>", methods=["PUT"])
def update_freelancer(freelancer_id):
    try:
        data = request.form
        update_data = {
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "username": data.get("username"),
            "email": data.get("email"),
            "profile_photo": data.get("profilePhoto"),
            "experience": data.get("experience"),
            "description": data.get("description"),
            "phone_number": data.get("phoneNumber"),
            "instagram_link": data.get("instagramLink"),
            "linkedIn_link": data.get("linkedInLink"),
            "skills": data.get("skills"),
            "location": {
                "city": data.get("city"),
                "state": data.get("state"),
                "country": data.get("country"),
                "pincode": data.get("pincode")
            }
        }

        # Only update the password if it is provided
        if data.get("password"):
            update_data["password"] = data.get("password")  # Ensure to hash the password if needed

        # Updating the freelancer details
        freelancer = Freelancer.objects.get(id=freelancer_id)
        freelancer.update(**update_data)

        flash("Freelancer updated successfully", "success")
        return redirect(f"/api/freelancers/{freelancer_id}")
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error updating freelancer details", "error")
        return redirect("/api/freelancers")

# DELETE: Delete a freelancer
@freelancer_bp.route("/<freelancer_id>", methods=["DELETE"])
def delete_freelancer(freelancer_id):
    try:
        freelancer = Freelancer.objects.get(id=freelancer_id)
        freelancer.delete()
        flash("Freelancer deleted successfully", "success")
        return redirect("/api/freelancers")
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error deleting freelancer", "error")
        return redirect("/api/freelancers")

# GET: All projects for a specific freelancer
@freelancer_bp.route("/<freelancer_id>/projects", methods=["GET"])
def freelancer_projects(freelancer_id):
    try:
        freelancer = Freelancer.objects.get(id=freelancer_id).populate("projects")
        return render_template("freelancers/projects.html", freelancer=freelancer, projects=freelancer.projects, title=f"{freelancer.first_name}'s Projects")
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error fetching freelancer projects", "error")
        return redirect("/api/freelancers")

# GET: Add new project form for a specific freelancer
@freelancer_bp.route("/<freelancer_id>/projects/add", methods=["GET"])
def add_project_form(freelancer_id):
    return render_template("freelancers/new-project.html", freelancer_id=freelancer_id)

# POST: Add a new project for a specific freelancer
@freelancer_bp.route("/<freelancer_id>/projects/add", methods=["POST"])
def add_project(freelancer_id):
    try:
        data = request.form
        new_project = Project(
            title=data.get("title"),
            description=data.get("description"),
            budget=data.get("budget"),
            deadline=data.get("deadline"),  # Ensure this is a valid date
            status=data.get("status"),
            freelancer=freelancer_id
        )
        new_project.save()

        # Update the freelancer's projects array
        Freelancer.objects.get(id=freelancer_id).update(push__projects=new_project.id)

        return redirect(f"/api/freelancers/{freelancer_id}/projects")
    except Exception as e:
        flash("Error creating project", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects/add")

# GET: Edit project form
@freelancer_bp.route("/<freelancer_id>/projects/<project_id>/edit", methods=["GET"])
def edit_project_form(freelancer_id, project_id):
    try:
        project = Project.objects.get(id=project_id)
        return render_template("freelancers/edit-project.html", project=project, freelancer_id=freelancer_id)
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects")
    except Exception as e:
        flash("Error fetching project for edit", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects")

# POST: Update project
@freelancer_bp.route("/<freelancer_id>/projects/<project_id>/edit", methods=["POST"])
def update_project(freelancer_id, project_id):
    try:
        data = request.form
        Project.objects.get(id=project_id).update(
            title=data.get("title"),
            description=data.get("description"),
            budget=data.get("budget"),
            deadline=data.get("deadline"),
            status=data.get("status")
        )
        return redirect(f"/api/freelancers/{freelancer_id}/projects")
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects/{project_id}/edit")
    except Exception as e:
        flash("Error updating project", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects/{project_id}/edit")

# DELETE: Delete a project
@freelancer_bp.route("/<freelancer_id>/projects/<project_id>", methods=["DELETE"])
def delete_project(freelancer_id, project_id):
    try:
        Project.objects.get(id=project_id).delete()
        return redirect(f"/api/freelancers/{freelancer_id}/projects")
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects")
    except Exception as e:
        flash("Error deleting project", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/projects")

# GET: Reviews for a specific freelancer
@freelancer_bp.route("/<freelancer_id>/reviews", methods=["GET"])
def freelancer_reviews(freelancer_id):
    try:
        freelancer = Freelancer.objects.get(id=freelancer_id).populate({
            'path': 'reviews',
            'populate': {
                'path': 'reviewer',
                'model': 'Client'
            }
        })
        return render_template("freelancers/reviews.html", freelancer=freelancer, reviews=freelancer.reviews)
    except DoesNotExist:
        flash("Freelancer not found", "error")
        return redirect("/api/freelancers")
    except Exception as e:
        flash("Error fetching reviews", "error")
        return redirect("/api/freelancers")

# POST: Create a new review for a freelancer
@freelancer_bp.route("/<freelancer_id>/reviews", methods=["POST"])
def create_review(freelancer_id):
    try:
        data = request.form
        new_review = Review(
            rating=data.get("rating"),
            comment=data.get("comment"),
            reviewer=request.user.id,  # Assuming user is logged in
            freelancer=freelancer_id
        )
        new_review.save()

        # Update the freelancer's reviews array
        Freelancer.objects.get(id=freelancer_id).update(push__reviews=new_review.id)

        flash("Review submitted successfully", "success")
        return redirect(f"/api/freelancers/{freelancer_id}")
    except Exception as e:
        flash("Error creating review", "error")
        return redirect(f"/api/freelancers/{freelancer_id}")

# GET: Edit review form
@freelancer_bp.route("/<freelancer_id>/reviews/<review_id>/edit", methods=["GET"])
def edit_review_form(freelancer_id, review_id):
    try:
        review = Review.objects.get(id=review_id)
        return render_template("freelancers/edit-review.html", review=review, freelancer_id=freelancer_id)
    except DoesNotExist:
        flash("Review not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")
    except Exception as e:
        flash("Error fetching review for edit", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")

# POST: Update review
@freelancer_bp.route("/<freelancer_id>/reviews/<review_id>/edit", methods=["POST"])
def update_review(freelancer_id, review_id):
    try:
        data = request.form
        Review.objects.get(id=review_id).update(
            rating=data.get("rating"),
            comment=data.get("comment")
        )
        flash("Review updated successfully", "success")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")
    except DoesNotExist:
        flash("Review not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews/{review_id}/edit")
    except Exception as e:
        flash("Error updating review", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews/{review_id}/edit")

# DELETE: Delete a review
@freelancer_bp.route("/<freelancer_id>/reviews/<review_id>", methods=["DELETE"])
def delete_review(freelancer_id, review_id):
    try:
        Review.objects.get(id=review_id).delete()
        Freelancer.objects.get(id=freelancer_id).update(pull__reviews=review_id)
        flash("Review deleted successfully", "success")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")
    except DoesNotExist:
        flash("Review not found", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")
    except Exception as e:
        flash("Error deleting review", "error")
        return redirect(f"/api/freelancers/{freelancer_id}/reviews")

# Register the blueprint in your main application file
# In your app/__init__.py, add the following line:
# from app.routes.freelancerRoutes import freelancer_bp
# app.register_blueprint(freelancer_bp, url_prefix='/api/freelancers')