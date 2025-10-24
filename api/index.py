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

# Try multiple environment variable names for database URL (with and without db_ prefix)
database_url = (
    os.environ.get('POSTGRES_URL') or 
    os.environ.get('db_POSTGRES_URL') or 
    os.environ.get('POSTGRES_PRISMA_URL') or 
    os.environ.get('db_POSTGRES_PRISMA_URL') or 
    os.environ.get('db_DATABASE_URL') or 
    os.environ.get('DATABASE_URL') or 
    'sqlite:///tmp/algo.db'  # Use /tmp for serverless
)

# Debug: Print which database is being used (remove in production)
print(f"Using database: {database_url[:30]}...")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

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
    
    # Initialize database tables immediately (not on first request for serverless)
    print("🔄 Initializing database tables...")
    try:
        from database.auth_db import init_db as ensure_auth_tables_exists
        from database.master_contract_db import init_db as ensure_master_contract_tables_exists
        from database.apilog_db import init_db as ensure_api_log_tables_exists
        
        with app.app_context():
            print("📊 Creating auth tables...")
            ensure_auth_tables_exists()
            print("📊 Creating master contract tables...")
            ensure_master_contract_tables_exists()
            print("📊 Creating API log tables...")
            ensure_api_log_tables_exists()
            print("✅ All database tables initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        import traceback
        traceback.print_exc()
except Exception as e:
    print(f"❌ Database setup error: {e}")
    import traceback
    traceback.print_exc()

# Register blueprints
blueprints_registered = []
try:
    from blueprints.core import core_bp
    app.register_blueprint(core_bp)
    blueprints_registered.append('core_bp')
    print("✅ Core blueprint registered")
except Exception as e:
    print(f"❌ Core blueprint error: {e}")

try:
    from blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    blueprints_registered.append('auth_bp')
    print("✅ Auth blueprint registered")
except Exception as e:
    print(f"❌ Auth blueprint error: {e}")

try:
    from blueprints.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    blueprints_registered.append('dashboard_bp')
    print("✅ Dashboard blueprint registered")
except Exception as e:
    print(f"❌ Dashboard blueprint error: {e}")

try:
    from blueprints.orders import orders_bp
    app.register_blueprint(orders_bp)
    blueprints_registered.append('orders_bp')
    print("✅ Orders blueprint registered")
except Exception as e:
    print(f"❌ Orders blueprint error: {e}")

try:
    from blueprints.search import search_bp
    app.register_blueprint(search_bp)
    blueprints_registered.append('search_bp')
    print("✅ Search blueprint registered")
except Exception as e:
    print(f"❌ Search blueprint error: {e}")

try:
    from blueprints.api_v1 import api_v1_bp
    app.register_blueprint(api_v1_bp)
    blueprints_registered.append('api_v1_bp')
    print("✅ API v1 blueprint registered")
except Exception as e:
    print(f"❌ API v1 blueprint error: {e}")

try:
    from blueprints.apikey import api_key_bp
    app.register_blueprint(api_key_bp)
    blueprints_registered.append('api_key_bp')
    print("✅ API Key blueprint registered")
except Exception as e:
    print(f"❌ API Key blueprint error: {e}")

try:
    from blueprints.log import log_bp
    app.register_blueprint(log_bp)
    blueprints_registered.append('log_bp')
    print("✅ Log blueprint registered")
except Exception as e:
    print(f"❌ Log blueprint error: {e}")

try:
    from blueprints.tv_json import tv_json_bp
    app.register_blueprint(tv_json_bp)
    blueprints_registered.append('tv_json_bp')
    print("✅ TV JSON blueprint registered")
except Exception as e:
    print(f"❌ TV JSON blueprint error: {e}")

print(f"Total blueprints registered: {len(blueprints_registered)}")

# Home route is handled by core_bp blueprint

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_cors():
    return jsonify({"status": "success", "message": "CORS is working!"})

@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check environment variables"""
    return jsonify({
        "has_postgres_url": bool(os.environ.get('POSTGRES_URL')),
        "has_db_postgres_url": bool(os.environ.get('db_POSTGRES_URL')),
        "has_database_url": bool(os.environ.get('DATABASE_URL')),
        "has_db_database_url": bool(os.environ.get('db_DATABASE_URL')),
        "database_type": "postgresql" if "postgresql" in app.config['SQLALCHEMY_DATABASE_URI'] else "sqlite",
        "database_url_preview": app.config['SQLALCHEMY_DATABASE_URI'][:50] + "...",
        "app_key_set": bool(os.environ.get('APP_KEY')),
        "all_env_vars": [key for key in os.environ.keys() if 'POSTGRES' in key or 'DATABASE' in key]
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# Export for Vercel
app = app
