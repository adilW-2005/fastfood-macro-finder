from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from flask_bcrypt import Bcrypt
import redis
import json

app = Flask(__name__)  # ✅ Define Flask app first

# Ensure this URI is correct for SQLite, PostgreSQL, or MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # ✅ Initialize SQLAlchemy

bcrypt = Bcrypt(app)

# ✅ Allow CORS for all routes and methods

# ✅ Redis Configuration for Sessions
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False  # Sessions expire when the user closes the browser
app.config["SESSION_USE_SIGNER"] = True  # Encrypt session cookies
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_COOKIE_NAME"] = "session_id"  # Set session cookie name
app.config["SESSION_REDIS"] = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=False  # ✅ Ensures UTF-8 encoding
)


app.config["SECRET_KEY"] = "AdilsAPP"  # Generates a random secret key


# ✅ Initialize Flask-Session
Session(app)

# ✅ Enable CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from flask_bcrypt import Bcrypt
import redis
import json

app = Flask(__name__)  # ✅ Define Flask app first

# Ensure this URI is correct for SQLite, PostgreSQL, or MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nutrition.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # ✅ Initialize SQLAlchemy

bcrypt = Bcrypt(app)

# ✅ Allow CORS for all routes and methods

# ✅ Redis Configuration for Sessions
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False  # Sessions expire when the user closes the browser
app.config["SESSION_USE_SIGNER"] = True  # Encrypt session cookies
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_COOKIE_NAME"] = "session_id"  # Set session cookie name
app.config["SESSION_REDIS"] = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=False  # ✅ Ensures UTF-8 encoding
)
app.config["SESSION_COOKIE_HTTPONLY"] = True           # Helps prevent XSS
app.config["SESSION_COOKIE_SAMESITE"] = "None"           # Allows cross-site requests
app.config["SESSION_COOKIE_SECURE"] = True              # Set True if using HTTPS


app.config["SECRET_KEY"] = "AdilsAPP"  # Generates a random secret key


# ✅ Initialize Flask-Session
Session(app)

# ✅ Enable CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])
