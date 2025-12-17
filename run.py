# run.py
from app import create_app, db
import os
import sys

app = create_app()

# Create tables on app startup
with app.app_context():
    try:
        print("🔧 Checking database...")

        # Get DB file path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']

        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"📁 DB file: {db_path}")

            # Create DB folder if needed
            if os.path.dirname(db_path):
                os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Create all tables if they don't exist
        db.create_all()
        print("✅ Database checked/created")

        # Check which tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Tables in DB: {tables}")

        # Create test user if user table is empty
        from app.models import User
        if User.query.count() == 0:
            print("👤 Creating test user...")
            try:
                test_user = User(username='demo', email='demo@example.com')
                test_user.set_password('Demo123')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created")
                print("   Email: demo@example.com")
                print("   Password: Demo123")
            except Exception as e:
                print(f"⚠️ Could not create test user: {e}")
                db.session.rollback()

    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print(f"🚀 Starting VibeMe...")
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"🌐 Open in browser: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)