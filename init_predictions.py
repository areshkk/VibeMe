#!/usr/bin/env python
"""
Predictions initialization script.
Run: python init_predictions.py
"""

import sys
import os

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import Prediction
    from app.predictions_utils import PredictionsManager


    def main():
        """Main initialization function"""
        print("🔮 Initializing predictions system...")

        # Create app
        app = create_app()

        with app.app_context():
            # Create all tables (if not exist)
            db.create_all()
            print("✅ Database tables created")

            # CLEAR existing predictions (if overwrite needed)
            print("🧹 Clearing old predictions...")
            Prediction.query.delete()
            db.session.commit()
            print("✅ Old predictions deleted")

            # Initialize default predictions (ALL 300)
            PredictionsManager.initialize_default_predictions()

            # Show statistics
            total_preds = PredictionsManager.get_predictions_count()

            print(f"📊 Predictions statistics:")
            print(f"   • Total predictions: {total_preds}")

            # Show categories with prediction counts
            categories = PredictionsManager.get_all_categories()
            print(f"   • Categories: {len(categories)}")

            print("\n🎭 Prediction categories with counts:")
            for key, value in categories.items():
                count = db.session.query(Prediction).filter_by(category=key).count()
                print(f"   • {value}: {count} predictions")

            # Verify distribution
            print("\n✅ Distribution check:")
            for key in categories.keys():
                count = db.session.query(Prediction).filter_by(category=key).count()
                if count == 30:
                    print(f"   ✅ {categories[key]}: {count}/30 ✓")
                else:
                    print(f"   ❌ {categories[key]}: {count}/30 (ERROR: should be 30)")

            print(f"\n✅ Predictions system initialized successfully!")
            print(f"   Total loaded: {total_preds} predictions")
            if total_preds == 300:
                print("   ✅ All 300 predictions loaded successfully!")
            else:
                print(f"   ⚠️ Loaded {total_preds} out of 300 predictions")


    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure app/predictions_utils.py exists")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()