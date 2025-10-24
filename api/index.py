import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.debug = False

# Set secret key and config
app.secret_key = os.getenv('APP_KEY', 'default-secret-key-change-this')
# Use POSTGRES_URL from Neon, fallback to DATABASE_URL, then SQLite
database_url = os.getenv('POSTGRES_URL') or os.getenv('DATABASE_URL', 'sqlite:///db/algo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Initialize CORS
CORS(app, 
     origins=["*"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization"])

# Initialize extensions
try:
    from extensions import socketio
    socketio.init_app(app, cors_allowed_origins="*")
except Exception as e:
    print(f"SocketIO initialization skipped: {e}")

try:
    from database.db import db
    db.init_app(app)
    
    # Initialize database tables on first request
    @app.before_first_request
    def init_database():
        try:
            from database.auth_db import init_db as ensure_auth_tables_exists
            from database.master_contract_db import init_db as ensure_master_contract_tables_exists
            from database.apilog_db import init_db as ensure_api_log_tables_exists
            
            with app.app_context():
                ensure_auth_tables_exists()
                ensure_master_contract_tables_exists()
                ensure_api_log_tables_exists()
        except Exception as e:
            print(f"Database initialization error: {e}")
except Exception as e:
    print(f"Database setup error: {e}")

# Register blueprints
try:
    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.orders import orders_bp
    from blueprints.search import search_bp
    from blueprints.api_v1 import api_v1_bp
    from blueprints.apikey import api_key_bp
    from blueprints.log import log_bp
    from blueprints.tv_json import tv_json_bp
    from blueprints.core import core_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(api_v1_bp)
    app.register_blueprint(api_key_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(tv_json_bp)
    app.register_blueprint(core_bp)
except Exception as e:
    print(f"Blueprint registration error: {e}")

@app.route('/')
def home():
    return "App is running!"

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_cors():
    return jsonify({"status": "success", "message": "CORS is working!"})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# Export for Vercel
app = app
