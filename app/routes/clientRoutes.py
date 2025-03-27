from flask import Blueprint, render_template, request, jsonify
from app.models.client import Client
from app.models.project import Project
from app.models.freelancer import Freelancer
from mongoengine import DoesNotExist, Q  # Import Q for querying
from mongoengine import ValidationError

client_bp = Blueprint('client', __name__)

# GET: Show all clients
@client_bp.route("/", methods=["GET"])
def show_clients():
    try:
        clients = Client.objects()
        return render_template("clients/index.html", clients=clients, title="All Clients")
    except Exception as e:
        return render_template("clients/index.html", error="Error fetching clients", title="All Clients")

# GET: Show single client
@client_bp.route("/<client_id>", methods=["GET"])
def show_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        return render_template("clients/show.html", client=client, title=f"{client.first_name} {client.last_name}")
    except DoesNotExist:
        return render_template("clients/show.html", error="Client not found", title="Client Not Found")
    except Exception as e:
        return render_template("clients/show.html", error="Error fetching client details", title="Client Details")

# GET: Client edit form
@client_bp.route("/<client_id>/edit", methods=["GET"])
def edit_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        return render_template("clients/edit.html", client=client, title="Edit Client")
    except DoesNotExist:
        return render_template("clients/edit.html", error="Client not found", title="Edit Client")
    except Exception as e:
        return render_template("clients/edit.html", error="Error loading edit page", title="Edit Client")

# PUT: Update client details
@client_bp.route("/<client_id>", methods=["PUT"])
def update_client(client_id):
    try:
        data = request.form
        updated_client = Client.objects.get(id=client_id)
        updated_client.update(**data)  # Update client details
        return render_template("clients/show.html", client=updated_client, title=f"{updated_client.first_name} {updated_client.last_name}")
    except DoesNotExist:
        return render_template("clients/show.html", error="Client not found", title="Client Not Found")
    except ValidationError:
        return render_template("clients/edit.html", error="Invalid data provided", title="Edit Client")
    except Exception as e:
        return render_template("clients/edit.html", error="Error updating client details", title="Edit Client")

# DELETE: Delete a client
@client_bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        client = Client.objects.get(id=client_id)
        client.delete()
        return render_template("clients/index.html", message="Client deleted successfully", title="All Clients")
    except DoesNotExist:
        return render_template("clients/index.html", error="Client not found", title="All Clients")
    except Exception as e:
        return render_template("clients/index.html", error="Error deleting client", title="All Clients")

# GET: All projects for a specific client
@client_bp.route("/<client_id>/projects", methods=["GET"])
def client_projects(client_id):
    try:
        client = Client.objects.get(id=client_id).populate("projects")
        return render_template("clients/projects.html", client=client, projects=client.projects, title=f"{client.first_name}'s Projects")
    except DoesNotExist:
        return render_template("clients/projects.html", error="Client not found", title="Client Projects")
    except Exception as e:
        return render_template("clients/projects.html", error="Error fetching client projects", title="Client Projects")

# GET: Add new project form for a specific client
@client_bp.route("/<client_id>/projects/add", methods=["GET"])
def add_project_form(client_id):
    return render_template("clients/new-project.html", client_id=client_id)

# POST: Add a new project for a specific client
@client_bp.route("/<client_id>/projects/add", methods=["POST"])
def add_project(client_id):
    try:
        data = request.form
        
        # Validate the data before creating a new project
        if not data.get('projectName'):  # Example validation
            return render_template("clients/new-project.html", error="Project name is required", title="New Project")

        new_project = Project(**data, client=client_id)
        new_project.save()  # Save the new project

        # Update the client's projects list
        Client.objects.get(id =client_id).update(push__projects=new_project.id)

        return render_template("clients/projects.html", message="Project added successfully", title=f"{new_project.client.first_name}'s Projects")
    except ValidationError as ve:
        return render_template("clients/new-project.html", error=f"Validation error: {str(ve)}", title="New Project")
    except DoesNotExist:
        return render_template("clients/new-project.html", error="Client not found", title="New Project")
    except Exception as e:
        return render_template("clients/new-project.html", error="Error creating project: " + str(e), title="New Project")

# GET: Edit project form
@client_bp.route("/<client_id>/projects/<project_id>/edit", methods=["GET"])
def edit_project_form(client_id, project_id):
    try:
        project = Project.objects.get(id=project_id)
        return render_template("clients/edit-project.html", project=project, client_id=client_id)
    except DoesNotExist:
        return render_template("clients/edit-project.html", error="Project not found", title="Edit Project")
    except Exception as e:
        return render_template("clients/edit-project.html", error="Error fetching project for edit", title="Edit Project")

# POST: Update project
@client_bp.route("/<client_id>/projects/<project_id>/edit", methods=["POST"])
def update_project(client_id, project_id):
    try:
        data = request.form
        Project.objects.get(id=project_id).update(**data)
        return render_template("clients/projects.html", message="Project updated successfully", title=f"{Client.objects.get(id=client_id).first_name}'s Projects")
    except DoesNotExist:
        return render_template("clients/projects.html", error="Project not found", title="Client Projects")
    except Exception as e:
        return render_template("clients/projects.html", error="Error updating project", title="Client Projects")

# DELETE: Delete a project
@client_bp.route("/<client_id>/projects/<project_id>", methods=["DELETE"])
def delete_project(client_id, project_id):
    try:
        Project.objects.get(id=project_id).delete()
        return render_template("clients/projects.html", message="Project deleted successfully", title=f"{Client.objects.get(id=client_id).first_name}'s Projects")
    except DoesNotExist:
        return render_template("clients/projects.html", error="Project not found", title="Client Projects")
    except Exception as e:
        return render_template("clients/projects.html", error="Error deleting project", title="Client Projects")

# Route to assign a freelancer to a project
@client_bp.route("/<client_id>/projects/<project_id>/assign-freelancer", methods=["POST"])
def assign_freelancer(client_id, project_id):
    freelancer_id = request.form.get("freelancerId")
    if not ObjectId.is_valid(project_id):
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
        CreditService.earnReferralCreditsForClient(client_id)
        return jsonify({"message": "Referral credits earned successfully."}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

# Route to post a project
@client_bp.route("/<client_id>/post-project", methods=["POST"])
def post_project(client_id):
    project_cost = request.form.get("projectCost")
    try:
        CreditService.postProject(client_id, project_cost)
        return jsonify({"message": "Project posted successfully."}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

