#!/usr/bin/env python
"""
Database and recommendations initialization script.
Run: python init_db.py
"""

import sys
import os

# Add project path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.recommendations_utils import RecommendationsManager
from app.models import Recommendation


def main():
    """Main initialization function"""
    print("🚀 Initializing VibeMe database...")

    # Create app
    app = create_app()

    with app.app_context():
        # Create all tables (if not exist)
        db.create_all()
        print("✅ Database tables created")

        # Initialize default recommendations
        RecommendationsManager.initialize_default_recommendations()

        # Show statistics
        total_recs = Recommendation.query.count()

        print(f"📊 Recommendations statistics:")
        print(f"   • Total recommendations in DB: {total_recs}")

        if total_recs > 0:
            # Show recommendations by mood
            print("\n🎭 Recommendations by mood:")
            moods = RecommendationsManager.get_all_moods_with_recommendations()
            for mood in moods:
                count = Recommendation.query.filter_by(mood=mood).count()
                print(f"   • {mood}: {count} recommendations")

        print("\n✅ Database initialized successfully!")
        print("👉 Run the app: python run.py")


if __name__ == '__main__':
    main()