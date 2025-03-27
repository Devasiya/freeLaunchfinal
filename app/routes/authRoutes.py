# app/routes/authRoutes.py

from flask import Blueprint, request, jsonify, render_template, redirect, flash, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from app.models.client import Client
from app.models.freelancer import Freelancer
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

# Set up upload folder
UPLOAD_FOLDER = 'public/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# GET: Client Registration Page
@auth_bp.route('/register/client', methods=['GET'])
def register_client_page():
    return render_template("clientRegister.html", title="Client Registration", messages={"success": flash.get_flashed_messages(with_categories=True)})

# POST: Register Client
@auth_bp.route('/register/client', methods=['POST'])
def register_client():
    if 'profilePhoto' not in request.files:
        return redirect('/auth/register/client')

    file = request.files['profilePhoto']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        profile_photo_url = f"/uploads/{filename}"
    else:
        profile_photo_url = ""

    data = request.form
    email = data.get('email')
    password = data.get('password')

    existing_client = Client.objects(email=email).first()
    if existing_client:
        flash("Email is already registered!", "error")
        return redirect("/auth/register/client")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    client = Client(
        email=email,
        password=hashed_password,
        profile_photo=profile_photo_url,
        **data
    )
    client.save()

    flash("Client registered successfully!", "success")
    return redirect("/auth/login")

# GET: Freelancer Registration Page
@auth_bp.route('/register/freelancer', methods=['GET'])
def register_freelancer_page():
    return render_template("freelancerRegister.html", title="Freelancer Registration", messages={"success": flash.get_flashed_messages(with_categories=True)})

# POST: Register Freelancer
@auth_bp.route('/register/freelancer', methods=['POST'])
def register_freelancer():
    if 'profilePhoto' not in request.files:
        return redirect('/auth/register/freelancer')

    file = request.files['profilePhoto']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        profile_photo_url = f"/uploads/{filename}"
    else:
        profile_photo_url = ""

    data = request.form
    email = data.get('email')
    password = data.get('password')

    existing_freelancer = Freelancer.objects(email=email).first()
    if existing_freelancer:
        flash("Email is already registered!", "error")
        return redirect("/auth/register/freelancer")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    freelancer = Freelancer(
        email=email,
        password=hashed_password,
        profile_photo=profile_photo_url,
        **data
    )
    freelancer.save()

    flash("Freelancer registered successfully!", "success")
    return redirect("/auth/login")

# GET: Login Page
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html", title="Login", messages={"success": flash.get_flashed_messages(with_categories=True)})

# POST: Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    client = Client.objects(email=email).first()
    freelancer = Freelancer.objects(email=email).first()

    user = client if client else freelancer

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'email': user.email, 'user_type': 'client' if client else 'freelancer'})
        session['user_id'] = str(user .id)
        session['role'] = 'client' if client else 'freelancer'
        flash("Login successful!", "success")
        return redirect("/")

    flash("Invalid email or password!", "error")
    return redirect("/auth/login")

# GET: Logout User
@auth_bp.route('/logout', methods=['GET'])
def logout():
    flash("Logged out successfully!", "success")
    session.clear()
    return redirect("/auth/login")