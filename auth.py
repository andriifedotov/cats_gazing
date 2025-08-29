from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import db, User

bp = Blueprint("auth", __name__, url_prefix="")

@bp.get("/login")
def login_get():
    return render_template("login.html")

@bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        flash("Invalid credentials", "error")
        return redirect(url_for("auth.login_get"))
    login_user(user, remember=True)
    next_url = request.args.get("next") or url_for("protected")
    return redirect(next_url)

@bp.get("/register")
def register_get():
    return render_template("register.html")

@bp.post("/register")
def register_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not email or not password:
        flash("Email and password are required", "error")
        return redirect(url_for("auth.register_get"))
    exists = User.query.filter_by(email=email).first()
    if exists:
        flash("Email already registered", "error")
        return redirect(url_for("auth.register_get"))
    user = User(email=email, password_hash=User.hash_password(password))
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in.", "success")
    return redirect(url_for("auth.login_get"))

@bp.post("/logout")
@login_required
def logout_post():
    logout_user()
    return redirect(url_for("index"))
