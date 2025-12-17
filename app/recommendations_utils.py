from app.models import Recommendation
from app import db
from datetime import datetime


class RecommendationsManager:
    """Manager for handling recommendations"""

    # Default recommendations dictionary (for initial population)
    DEFAULT_RECOMMENDATIONS = {
        'happy': [
            'Share your happiness with others! 🌟',
            'Write down what made you happy today',
            'Do something kind for another person',
            'Enjoy this moment and be grateful for it',
            'Create a "collection of happy moments"'
        ],
        'calm': [
            'Practice deep breathing for 5 minutes',
            'Try meditation to maintain calmness',
            'Enjoy silence and peace',
            'Take a solitary walk in nature',
            'Brew some herbal tea and read a book'
        ],
        'neutral': [
            'Try a new hobby or activity',
            'Set a small goal and achieve it',
            'Listen to uplifting music',
            'Meet up with friends',
            'Do something unusual for variety'
        ],
        'sad': [
            'Listen to your favorite music 🎵',
            'Take a walk in fresh air',
            'Call a loved one',
            'Watch a favorite movie or series',
            'Write about your feelings in a journal'
        ],
        'angry': [
            'Take 10 deep breaths',
            'Engage in physical activity',
            'Express emotions on paper, then tear it up',
            'Distract yourself with another task for 10 minutes',
            'Talk about the problem with someone neutral'
        ],
        'anxious': [
            'Try the 5-4-3-2-1 technique: name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste',
            'Do breathing exercises',
            'Make a list of what you can control',
            'Take a warm shower or bath',
            'Practice mindfulness and grounding'
        ],
        'excited': [
            'Channel your energy into a creative project',
            'Share your excitement with friends',
            'Plan something fun for the future',
            'Dance to your favorite music',
            'Write down your ideas and plans'
        ],
        'tired': [
            'Rest for 20-30 minutes without gadgets',
            'Drink a glass of water and eat something light',
            'Do light stretching',
            'Listen to relaxing music',
            'Go to bed 30 minutes earlier tonight'
        ]
    }

    @staticmethod
    def initialize_default_recommendations():
        """Initialize database with default recommendations"""
        try:
            # Check if recommendations already exist
            if Recommendation.query.first() is not None:
                print("✅ Recommendations already initialized")
                return

            # Add default recommendations
            for mood, advice_list in RecommendationsManager.DEFAULT_RECOMMENDATIONS.items():
                for i, advice in enumerate(advice_list, 1):
                    recommendation = Recommendation(
                        mood=mood,
                        advice=advice,
                        category='default',
                        priority=i
                    )
                    db.session.add(recommendation)

            db.session.commit()
            print(f"✅ Initialized {len(RecommendationsManager.DEFAULT_RECOMMENDATIONS)} moods with recommendations")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error initializing recommendations: {e}")

    @staticmethod
    def get_recommendations_for_mood(mood, limit=3):
        """Get recommendations for a specific mood"""
        try:
            # Get recommendations from database
            recommendations = Recommendation.query.filter_by(
                mood=mood
            ).order_by(Recommendation.priority.asc()).limit(limit).all()

            # If no recommendations in DB, return defaults
            if not recommendations:
                advice_list = RecommendationsManager.DEFAULT_RECOMMENDATIONS.get(mood, [])
                return advice_list[:limit]

            # Convert objects to strings
            return [rec.advice for rec in recommendations]

        except Exception as e:
            print(f"❌ Error getting recommendations: {e}")
            # Return default recommendations on error
            advice_list = RecommendationsManager.DEFAULT_RECOMMENDATIONS.get(mood, [])
            return advice_list[:limit]

    @staticmethod
    def get_all_moods_with_recommendations():
        """Get all moods that have recommendations"""
        try:
            # Get unique moods from database
            moods = db.session.query(Recommendation.mood).distinct().all()
            return [mood[0] for mood in moods]
        except Exception as e:
            print(f"❌ Error getting moods: {e}")
            return list(RecommendationsManager.DEFAULT_RECOMMENDATIONS.keys())

    @staticmethod
    def add_recommendation(mood, advice, category='custom', priority=1):
        """Add a new recommendation"""
        try:
            recommendation = Recommendation(
                mood=mood,
                advice=advice,
                category=category,
                priority=priority
            )
            db.session.add(recommendation)
            db.session.commit()
            return True, "✅ Recommendation added successfully"
        except Exception as e:
            db.session.rollback()
            return False, f"❌ Error adding recommendation: {e}"