from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User

bp = Blueprint("auth", __name__, url_prefix="")

# ===== LOGIN =====
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            flash("Invalid credentials", "error")
            return redirect(url_for("auth.login"))
        login_user(user, remember=True)
        next_url = request.args.get("next") or url_for("index")
        return redirect(next_url)
    # GET
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("login.html")

# ===== REGISTER =====
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Email and password are required", "error")
            return redirect(url_for("auth.register"))
        exists = User.query.filter_by(email=email).first()
        if exists:
            flash("Email already registered", "error")
            return redirect(url_for("auth.register"))
        user = User(email=email, password_hash=User.hash_password(password))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    # GET
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("register.html")

# ===== LOGOUT =====
@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
