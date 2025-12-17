from app import create_app, db
from app.models import User, MoodEntry, Prediction

app = create_app()

with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("✅ Tables created successfully!")

        # Import predictions manager
        try:
            from app.predictions_utils import PredictionsManager

            # Initialize predictions
            PredictionsManager.initialize_default_predictions()
            print("✅ Predictions initialized!")

            # Test random prediction retrieval
            prediction, category_name = PredictionsManager.get_random_prediction()
            if prediction:
                print(f"✅ Random prediction retrieved: '{prediction.text}'")
                print(f"   Category: {category_name}")
            else:
                print("❌ Failed to get prediction")

            # Test category filtering
            prediction_love, love_category = PredictionsManager.get_random_prediction('love')
            if prediction_love:
                print(f"✅ Love category prediction: '{prediction_love.text}'")

            # Check prediction count
            count = PredictionsManager.get_predictions_count()
            print(f"✅ Total predictions in DB: {count}")

        except ImportError:
            print("⚠️ predictions_utils module not found, skipping prediction tests")

        # Test user creation
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('TestPass123')
        db.session.add(test_user)
        db.session.commit()

        # Test mood entry creation
        test_mood = MoodEntry(mood='sad', notes='Test entry', user_id=test_user.id)
        db.session.add(test_mood)
        db.session.commit()

        print("\n✅ All models are working correctly!")

    except Exception as e:
        print(f"❌ Error: {e}")