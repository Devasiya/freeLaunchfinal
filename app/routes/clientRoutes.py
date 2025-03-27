# app/routes/clientRoutes.py

from flask import Blueprint, render_template, request, redirect, flash, jsonify
from app.models.client import Client
from app.models.projects import Project
from app.models.freelancer import Freelancer
from mongoengine import DoesNotExist
import mongoose  # Ensure you have the necessary imports

client_bp = Blueprint('client', __name__)

# GET: Show all clients
@client_bp.route("/", methods=["GET"])
def show_clients():
    try:
        clients = Client.objects()
        return render_template("clients/index.html", clients=clients, title="All Clients")
    except Exception as e:
        flash("Error fetching clients", "error")
        return redirect("/")

# GET: Show single client
@client_bp.route("/<client_id>", methods=["GET"])
def show_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        return render_template("clients/show.html", client=client, title=f"{client.first_name} {client.last_name}")
    except DoesNotExist:
        flash("Client not found", "error")
        return redirect("/api/clients")
    except Exception as e:
        flash("Error fetching client details", "error")
        return redirect("/api/clients")

# GET: Client edit form
@client_bp.route("/<client_id>/edit", methods=["GET"])
def edit_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        return render_template("clients/edit.html", client=client, title="Edit Client")
    except DoesNotExist:
        flash("Client not found", "error")
        return redirect("/api/clients")
    except Exception as e:
        flash("Error loading edit page", "error")
        return redirect("/api/clients")

# PUT: Update client details
@client_bp.route("/<client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        data = request.form
        updated_client = Client.objects.get(id=client_id)
        updated_client.update(**data)  # Update client details
        flash("Client updated successfully", "success")
        return redirect(f"/api/clients/{client_id}")
    except DoesNotExist:
        flash("Client not found", "error")
        return redirect("/api/clients")
    except Exception as e:
        flash("Error updating client details", "error")
        return redirect("/api/clients")

# DELETE: Delete a client
@client_bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        client.delete()
        flash("Client deleted successfully", "success")
        return redirect("/api/clients")
    except DoesNotExist:
        flash("Client not found", "error")
        return redirect("/api/clients")
    except Exception as e:
        flash("Error deleting client", "error")
        return redirect("/api/clients")

# GET: All projects for a specific client
@client_bp.route("/<client_id>/projects", methods=["GET"])
def client_projects(client_id):
    try:
        client = Client.objects.get(id=client_id).populate("projects")
        return render_template("clients/projects.html", client=client, projects=client.projects, title=f"{client.first_name}'s Projects")
    except DoesNotExist:
        flash("Client not found", "error")
        return redirect("/api/clients")
    except Exception as e:
        flash("Error fetching client projects", "error")
        return redirect("/api/clients")

# GET: Add new project form for a specific client
@client_bp.route("/<client_id>/projects/add", methods=["GET"])
def add_project_form(client_id):
    return render_template("clients/new-project.html", client_id=client_id)

# POST: Add a new project for a specific client
@client_bp.route("/<client_id>/projects/add", methods=["POST"])
def add_project(client_id):
    try:
        data = request.form
        new_project = Project(**data, client=client_id)
        new_project.save()
        Client.objects.get(id=client_id).update(push__projects=new_project.id)
        return redirect(f"/api/clients/{client_id}/projects")
    except Exception as e:
        flash("Error creating project", "error")
        return redirect(f"/api/clients/{client_id}/projects/add")

# GET: Edit project form
@client_bp.route("/<client_id>/projects/<project_id>/edit", methods=["GET"])
def edit_project_form(client_id, project_id):
    try:
        project = Project.objects.get(id=project_id)
        return render_template("clients/edit-project.html", project=project, client_id=client_id)
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/clients/{client_id}/projects")
    except Exception as e:
        flash("Error fetching project for edit", "error")
        return redirect(f"/api/clients/{client_id}/projects")

# POST: Update project
@client_bp.route("/<client_id>/projects/<project_id>/edit", methods=["POST"])
def update_project(client_id, project_id):
    try:
        data = request.form
        Project.objects.get(id=project_id).update(**data)
        return redirect(f"/api/clients/{client_id}/projects")
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/clients/{client_id}/projects/{project_id}/edit")
    except Exception as e:
        flash("Error updating project", "error")
        return redirect(f"/api/clients/{client_id}/projects/{project_id}/edit")

# DELETE: Delete a project
@client_bp.route("/<client_id>/projects/<project_id>", methods=["DELETE"])
def delete_project(client_id, project_id):
    try:
        Project.objects.get(id=project_id).delete()
        return redirect(f"/api/clients/{client_id}/projects")
    except DoesNotExist:
        flash("Project not found", "error")
        return redirect(f"/api/clients/{client_id}/projects")
    except Exception as e:
        flash("Error deleting project", "error")
        return redirect(f"/api/clients/{client_id}/projects")

# Route to assign a freelancer to a project
@client_bp.route("/<client_id>/projects/<project_id>/assign-freelancer", methods=["POST"])
def assign_freelancer(client_id, project_id):
    freelancer_id = request.form.get("freelancerId")
    if not mongoose.Types.ObjectId.is_valid(project_id):
        return jsonify({"error": "Invalid Project ID"}), 400

    try:
        project = Project.objects.get(id=project_id)
        project.update(assignedFreelancer=freelancer_id)
        return jsonify({"message": "Freelancer assigned successfully", "project": project}), 200
    except DoesNotExist:
        return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": "Error assigning freelancer"}), 500

# Route to search freelancers
@client_bp.route("/freelancers/search", methods=["GET"])
def search_freelancers():
    query = request.args.get("q")
    try:
        freelancers = Freelancer.objects(
            Q(firstName__icontains=query) | Q(lastName__icontains=query)
        ).only("id", "firstName", "lastName")
        return jsonify(freelancers), 200
    except Exception as e:
        return jsonify({"error": "Error fetching freelancers"}), 500

# Route to earn referral credits
@client_bp.route("/<client_id>/earn-referral-credits", methods=["POST"])
def earn_referral_credits(client_id):
    try:
        # Assuming you have a CreditService to handle this logic
        CreditService .earnReferralCreditsForClient(client_id)
        return jsonify({"message": "Referral credits earned successfully."}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

# Route to post a project
@client_bp.route("/<client_id>/post-project", methods=["POST"])
def post_project(client_id):
    project_cost = request.form.get("projectCost")
    try:
        # Assuming you have a CreditService to handle this logic
        CreditService.postProject(client_id, project_cost)
        return jsonify({"message": "Project posted successfully."}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

# Register the blueprint in your main application file
# In your app/__init__.py, add the following line:
# from app.routes.clientRoutes import client_bp
# app.register_blueprint(client_bp, url_prefix='/api/clients')
