from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, MoodForm
from app.models import User, MoodEntry, Recommendation
from app.recommendations_utils import RecommendationsManager
from datetime import datetime
import logging
import csv
from io import StringIO

# Try to import predictions module
try:
    from app.predictions_utils import PredictionsManager
    PREDICTIONS_AVAILABLE = True
except ImportError:
    PREDICTIONS_AVAILABLE = False
    print("⚠️ predictions_utils module not found")
    PredictionsManager = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

# Import predictions manager
try:
    from app.predictions_utils import PredictionsManager
    PREDICTIONS_AVAILABLE = True
except ImportError:
    PREDICTIONS_AVAILABLE = False
    print("⚠️ predictions_utils module not found")

# Import recommendations manager
try:
    from app.recommendations_utils import RecommendationsManager
    RECOMMENDATIONS_AVAILABLE = True
except ImportError:
    RECOMMENDATIONS_AVAILABLE = False
    print("⚠️ recommendations_utils module not found")


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)

            # Save to database
            db.session.add(user)
            db.session.commit()

            logger.info(f'New user registered: {user.username} ({user.email})')
            flash('🎉 Registration successful! You can now log in.', 'success')
            return redirect(url_for('main.login'))

        except ValueError as e:
            db.session.rollback()
            flash(f'❌ Validation error: {str(e)}', 'danger')
            logger.warning(f'Registration validation error: {str(e)}')

        except Exception as e:
            db.session.rollback()
            flash('❌ An error occurred during registration. Please try again.', 'danger')
            logger.error(f'Registration error for {form.email.data}: {str(e)}')

    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Find user by email
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()

            # Check password
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                logger.info(f'User logged in: {user.username}')
                flash(f'🌈 Welcome back, {user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                logger.warning(f'Failed login attempt for email: {form.email.data}')
                flash('❌ Invalid email or password. Please try again.', 'danger')

        except Exception as e:
            flash('❌ An error occurred during login. Please try again.', 'danger')
            logger.error(f'Login error for {form.email.data}: {str(e)}')

    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f'User logged out: {username}')
    flash('👋 You have been logged out. Come back soon!', 'info')
    return redirect(url_for('main.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent mood entries
    recent_moods = MoodEntry.query.filter_by(user_id=current_user.id) \
        .order_by(MoodEntry.timestamp.desc()) \
        .limit(5).all()

    # Get last mood for recommendations
    last_mood = None
    recommendations = []

    if RECOMMENDATIONS_AVAILABLE and recent_moods:
        last_mood = recent_moods[0]
        recommendations = RecommendationsManager.get_recommendations_for_mood(last_mood.mood)

    return render_template('dashboard.html',
                           recent_moods=recent_moods,
                           last_mood=last_mood,
                           recommendations=recommendations)


@bp.route('/mood', methods=['GET', 'POST'])
@login_required
def mood_form():
    form = MoodForm()

    if form.validate_on_submit():
        try:
            # Create new mood entry
            mood_entry = MoodEntry(
                mood=form.mood.data,
                notes=form.notes.data,
                author=current_user
            )

            # Save to database
            db.session.add(mood_entry)
            db.session.commit()

            logger.info(f'Mood entry created by {current_user.username}: {mood_entry.mood}')

            # Get recommendations for saved mood
            recommendations = []
            if RECOMMENDATIONS_AVAILABLE:
                recommendations = RecommendationsManager.get_recommendations_for_mood(form.mood.data)

            # Create readable mood name
            mood_translation = {
                'happy': '😊 Happy',
                'calm': '😌 Calm',
                'neutral': '😐 Neutral',
                'sad': '😔 Sad',
                'angry': '😠 Angry',
                'anxious': '😰 Anxious',
                'excited': '🎉 Excited',
                'tired': '😴 Tired'
            }
            mood_display = mood_translation.get(form.mood.data, form.mood.data)

            flash(f'✅ Mood "{mood_display}" saved successfully!', 'success')

            return render_template('mood_form.html',
                                   form=MoodForm(),
                                   show_recommendations=True,
                                   recommendations=recommendations,
                                   saved_mood=mood_display)

        except Exception as e:
            db.session.rollback()
            flash('❌ An error occurred while saving your mood.', 'danger')
            logger.error(f'Mood entry error for {current_user.username}: {str(e)}')

    return render_template('mood_form.html',
                           form=form,
                           show_recommendations=False)


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@bp.route('/stats')
@login_required
def stats():
    try:
        # Get all mood entries
        mood_entries = MoodEntry.query.filter_by(
            user_id=current_user.id
        ).order_by(MoodEntry.timestamp.asc()).all()

        # Prepare data for chart
        mood_data = {
            'happy': 0,
            'calm': 0,
            'neutral': 0,
            'sad': 0,
            'angry': 0,
            'anxious': 0,
            'excited': 0,
            'tired': 0
        }

        # Count each mood
        for entry in mood_entries:
            if entry.mood in mood_data:
                mood_data[entry.mood] += 1

        # Prepare timeline data
        timeline_data = []
        for entry in mood_entries:
            timeline_data.append({
                'date': entry.timestamp.strftime('%Y-%m-%d'),
                'mood': entry.mood,
                'timestamp': entry.timestamp.isoformat(),
                'notes': entry.notes if entry.notes else ''
            })

        # Prepare data for pie chart
        chart_labels = list(mood_data.keys())
        chart_data = list(mood_data.values())

        # Convert mood keys to readable names
        mood_translation = {
            'happy': '😊 Happy',
            'calm': '😌 Calm',
            'neutral': '😐 Neutral',
            'sad': '😔 Sad',
            'angry': '😠 Angry',
            'anxious': '😰 Anxious',
            'excited': '🎉 Excited',
            'tired': '😴 Tired'
        }

        chart_labels_readable = [mood_translation.get(label, label) for label in chart_labels]

        total_entries = len(mood_entries)

        # Determine most common mood
        most_common_mood = max(mood_data, key=mood_data.get) if total_entries > 0 else None
        most_common_mood_readable = mood_translation.get(most_common_mood,
                                                         most_common_mood) if most_common_mood else None

        logger.info(f'Statistics loaded for user {current_user.username}: {total_entries} entries')

        # Get recommendations for most common mood
        common_mood_recommendations = []
        if RECOMMENDATIONS_AVAILABLE and most_common_mood:
            common_mood_recommendations = RecommendationsManager.get_recommendations_for_mood(most_common_mood, limit=5)

        return render_template(
            'stats.html',
            chart_labels=chart_labels_readable,
            chart_data=chart_data,
            timeline_data=timeline_data,
            total_entries=total_entries,
            most_common_mood=most_common_mood_readable,
            mood_entries=mood_entries[-10:] if mood_entries else [],
            common_mood_recommendations=common_mood_recommendations
        )

    except Exception as e:
        logger.error(f'Error loading stats for {current_user.username}: {str(e)}')
        flash('❌ An error occurred while loading statistics', 'danger')
        return redirect(url_for('main.dashboard'))


# Recommendations routes
if RECOMMENDATIONS_AVAILABLE:
    @bp.route('/recommendations')
    @login_required
    def recommendations_page():
        """Page with all recommendations"""
        all_recommendations = {}
        moods = RecommendationsManager.get_all_moods_with_recommendations()

        for mood in moods:
            all_recommendations[mood] = RecommendationsManager.get_recommendations_for_mood(mood, limit=10)

        return render_template('recommendations.html',
                               all_recommendations=all_recommendations)


    @bp.route('/api/recommendations/<mood>')
    @login_required
    def get_recommendations(mood):
        """API to get recommendations by mood"""
        try:
            recommendations = RecommendationsManager.get_recommendations_for_mood(mood)
            return jsonify({
                'success': True,
                'mood': mood,
                'recommendations': recommendations
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
else:
    @bp.route('/recommendations')
    @login_required
    def recommendations_page():
        flash('Recommendations feature is temporarily unavailable', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/api/recommendations/<mood>')
    @login_required
    def get_recommendations(mood):
        return jsonify({
            'success': False,
            'error': 'Recommendations module unavailable'
        }), 501

# Predictions routes
if PREDICTIONS_AVAILABLE:
    @bp.route('/prediction')
    @login_required
    def prediction():
        """Page to get a prediction"""
        try:
            prediction_obj, category_name = PredictionsManager.get_random_prediction()

            if not prediction_obj:
                try:
                    PredictionsManager.initialize_default_predictions()
                    prediction_obj, category_name = PredictionsManager.get_random_prediction()
                except Exception as e:
                    logger.error(f"Failed to initialize predictions: {str(e)}")
                    flash('❌ Could not load predictions. Please try again later.', 'danger')
                    return redirect(url_for('main.dashboard'))

            all_categories = PredictionsManager.get_all_categories()

            return render_template(
                'prediction.html',
                prediction=prediction_obj,
                category_name=category_name,
                all_categories=all_categories
            )
        except Exception as e:
            logger.error(f'Error in prediction route: {str(e)}')
            flash('❌ An error occurred while loading prediction', 'danger')
            return redirect(url_for('main.dashboard'))


    @bp.route('/prediction/category/<category>')
    @login_required
    def prediction_by_category(category):
        """Get prediction by specific category"""
        try:
            prediction_obj, category_name = PredictionsManager.get_random_prediction(category)

            if not prediction_obj:
                flash('No predictions available for this category yet', 'info')
                return redirect(url_for('main.prediction'))

            return render_template(
                'prediction.html',
                prediction=prediction_obj,
                category_name=category_name,
                all_categories=PredictionsManager.get_all_categories(),
                selected_category=category
            )
        except Exception as e:
            logger.error(f'Error in prediction_by_category route: {str(e)}')
            flash('❌ An error occurred while loading prediction', 'danger')
            return redirect(url_for('main.prediction'))


    @bp.route('/api/prediction/random')
    @login_required
    def api_random_prediction():
        """API to get random prediction"""
        try:
            prediction_obj, category_name = PredictionsManager.get_random_prediction()

            if not prediction_obj:
                return jsonify({
                    'success': False,
                    'message': 'No predictions available'
                })

            return jsonify({
                'success': True,
                'prediction': {
                    'id': prediction_obj.id,
                    'text': prediction_obj.text,
                    'category': prediction_obj.category,
                    'category_name': category_name
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
else:
    @bp.route('/prediction')
    @login_required
    def prediction():
        flash('Predictions feature is temporarily unavailable', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/prediction/category/<category>')
    @login_required
    def prediction_by_category(category):
        flash('Predictions feature is temporarily unavailable', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/api/prediction/random')
    @login_required
    def api_random_prediction():
        return jsonify({
            'success': False,
            'error': 'Predictions module unavailable'
        }), 501