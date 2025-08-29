from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User

bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- LOGIN ---
@bp.get("/login", endpoint="login")
def login_get():
    next_url = request.args.get("next")  # capture the redirect target
    return render_template("login.html", next=next_url)

@bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        flash("Invalid credentials", "error")
        next_url = request.form.get("next") or url_for("index")
        return redirect(url_for("auth.login", next=next_url))

    login_user(user, remember=True)
    # redirect to 'next' if present, otherwise index
    next_url = request.form.get("next") or url_for("index")
    return redirect(next_url)

# --- REGISTER ---
@bp.get("/register", endpoint="register")
def register_get():
    return render_template("register.html")

@bp.post("/register")
def register_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Email and password are required", "error")
        return redirect(url_for("auth.register"))

    if User.query.filter_by(email=email).first():
        flash("Email already registered", "error")
        return redirect(url_for("auth.register"))

    user = User(email=email, password_hash=User.hash_password(password))
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in.", "success")
    return redirect(url_for("auth.login"))

# --- LOGOUT ---
@bp.post("/logout", endpoint="logout")
@login_required
def logout_post():
    logout_user()
    return redirect(url_for("auth.login"))
