"""
Nexora Suite - Unified WSGI Application

Single integrated Flask application with all modules as integrated features.
All modules share the same database, authentication, and user session.

Architecture:
- Main app: nexora-home (Flask)
- Modules: Integrated as feature sub-routes (/module/<name>/...)
- Database: Shared SQLite (unified schema)
- Auth: Single login, all features accessible
- Deployment: Single WSGI file for PythonAnywhere
"""

import os
import sys

# Add apps/nexora-home to path so we can import from it
app_dir = os.path.join(os.path.dirname(__file__), 'apps', 'nexora-home')
sys.path.insert(0, app_dir)

# Import and get the main Flask application
from app import app

# WSGI application - this is what PythonAnywhere/gunicorn will call
application = app

if __name__ == '__main__':
    # Development server
    port = int(os.getenv('PORT', '5060'))
    print(f"\n{'='*70}")
    print("  Nexora Suite - Enterprise Application")
    print(f"{'='*70}")
    print(f"\n  ✓ Running on http://0.0.0.0:{port}")
    print(f"  ✓ Database: Unified SQLite instance")
    print(f"  ✓ Authentication: Single login for all features")
    print(f"  ✓ Modules: 24 integrated feature modules\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
