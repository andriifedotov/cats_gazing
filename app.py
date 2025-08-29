import os
import random
import requests
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, User
from auth import bp as auth_bp
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")  # should be set securely in prod

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://user:password@postgres:5432/mydb"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB + Login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # redirect if not logged in
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprint with auth routes (login, logout, register)
app.register_blueprint(auth_bp)

CAT_API_URL = os.getenv("CAT_API_URL", "https://api.thecatapi.com/v1/images/search")
CAT_API_KEY = os.getenv("CAT_API_KEY")  # optional, improves rate limits

FALLBACK_CATS = [
    "https://placekitten.com/640/360",
    "https://placekitten.com/600/400",
    "https://placekitten.com/500/500",
    "https://placekitten.com/720/480",
    "https://placekitten.com/800/533",
]

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    return redirect(url_for("auth.login"))

@app.route("/api/cat")
@login_required
def api_cat():
    headers = {}
    if CAT_API_KEY:
        headers["x-api-key"] = CAT_API_KEY

    try:
        r = requests.get(
            CAT_API_URL,
            params={"limit": 1, "mime_types": "jpg,png"},
            headers=headers,
            timeout=5,
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return jsonify({"url": data[0].get("url")})
    except Exception:
        pass

    return jsonify({"url": random.choice(FALLBACK_CATS)})

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # auto-create tables if not exist
    app.run(host="0.0.0.0", port=5000)
