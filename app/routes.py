from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, MoodForm
from app.models import User, MoodEntry
from datetime import datetime
import logging

# В начале файла, после импортов, добавьте:
try:
    from app.predictions_utils import PredictionsManager
    PREDICTIONS_AVAILABLE = True
except ImportError:
    PREDICTIONS_AVAILABLE = False
    print("⚠️ Модуль predictions_utils не найден")
    PredictionsManager = None  # Для избежания ошибок

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

# Импортируем менеджер предсказаний
try:
    from app.predictions_utils import PredictionsManager

    PREDICTIONS_AVAILABLE = True
except ImportError:
    PREDICTIONS_AVAILABLE = False
    print("⚠️ Модуль predictions_utils не найден")

# Импортируем менеджер рекомендаций (если есть)
try:
    from app.recommendations_utils import RecommendationsManager

    RECOMMENDATIONS_AVAILABLE = True
except ImportError:
    RECOMMENDATIONS_AVAILABLE = False
    print("⚠️ Модуль recommendations_utils не найден")


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
            # Создаем нового пользователя
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)

            # Сохраняем в базу данных
            db.session.add(user)
            db.session.commit()

            logger.info(f'New user registered: {user.username} ({user.email})')
            flash('🎉 Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
            return redirect(url_for('main.login'))

        except ValueError as e:
            db.session.rollback()
            flash(f'❌ Ошибка валидации: {str(e)}', 'danger')
            logger.warning(f'Registration validation error: {str(e)}')

        except Exception as e:
            db.session.rollback()
            flash('❌ Произошла ошибка при регистрации. Попробуйте еще раз.', 'danger')
            logger.error(f'Registration error for {form.email.data}: {str(e)}')

    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Ищем пользователя по email
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()

            # Проверяем пароль
            if user and user.check_password(form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                logger.info(f'User logged in: {user.username}')
                flash(f'🌈 Добро пожаловать, {user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                # Логируем неудачную попытку входа
                logger.warning(f'Failed login attempt for email: {form.email.data}')
                flash('❌ Неверный email или пароль. Попробуйте еще раз.', 'danger')

        except Exception as e:
            flash('❌ Произошла ошибка при входе. Попробуйте еще раз.', 'danger')
            logger.error(f'Login error for {form.email.data}: {str(e)}')

    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f'User logged out: {username}')
    flash('👋 Вы вышли из системы. Возвращайтесь скорее!', 'info')
    return redirect(url_for('main.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    # Получаем последние записи настроения пользователя
    recent_moods = MoodEntry.query.filter_by(user_id=current_user.id) \
        .order_by(MoodEntry.timestamp.desc()) \
        .limit(5).all()

    # Получаем последнее настроение для рекомендаций
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

    # Если форма отправлена и валидна
    if form.validate_on_submit():
        try:
            # Создаем новую запись настроения
            mood_entry = MoodEntry(
                mood=form.mood.data,
                notes=form.notes.data,
                author=current_user
            )

            # Сохраняем в базу данных
            db.session.add(mood_entry)
            db.session.commit()

            logger.info(f'Mood entry created by {current_user.username}: {mood_entry.mood}')

            # Получаем рекомендации для сохраненного настроения
            recommendations = []
            if RECOMMENDATIONS_AVAILABLE:
                recommendations = RecommendationsManager.get_recommendations_for_mood(form.mood.data)

            # Создаем читаемое название настроения
            mood_translation = {
                'happy': '😊 Счастлив',
                'calm': '😌 Спокоен',
                'neutral': '😐 Нейтрален',
                'sad': '😔 Грустен',
                'angry': '😠 Сердит',
                'anxious': '😰 Тревожен',
                'excited': '🎉 В восторге',
                'tired': '😴 Устал'
            }
            mood_display = mood_translation.get(form.mood.data, form.mood.data)

            flash(f'✅ Настроение "{mood_display}" успешно сохранено!', 'success')

            # Рендерим шаблон с рекомендациями
            return render_template('mood_form.html',
                                   form=MoodForm(),  # Новая пустая форма
                                   show_recommendations=True,
                                   recommendations=recommendations,
                                   saved_mood=mood_display)

        except Exception as e:
            db.session.rollback()
            flash('❌ Произошла ошибка при сохранении настроения.', 'danger')
            logger.error(f'Mood entry error for {current_user.username}: {str(e)}')

    # Для GET запроса или если форма не валидна
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
        # Получаем все записи настроения пользователя
        mood_entries = MoodEntry.query.filter_by(
            user_id=current_user.id
        ).order_by(MoodEntry.timestamp.asc()).all()

        # Подготавливаем данные для графика
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

        # Считаем количество каждого настроения
        for entry in mood_entries:
            if entry.mood in mood_data:
                mood_data[entry.mood] += 1

        # Подготавливаем данные для линейного графика по времени
        timeline_data = []
        for entry in mood_entries:
            timeline_data.append({
                'date': entry.timestamp.strftime('%Y-%m-%d'),
                'mood': entry.mood,
                'timestamp': entry.timestamp.isoformat(),
                'notes': entry.notes if entry.notes else ''
            })

        # Подготавливаем данные для круговой диаграммы
        chart_labels = list(mood_data.keys())
        chart_data = list(mood_data.values())

        # Преобразуем ключи настроения в читаемые названия
        mood_translation = {
            'happy': '😊 Счастлив',
            'calm': '😌 Спокоен',
            'neutral': '😐 Нейтрален',
            'sad': '😔 Грустен',
            'angry': '😠 Сердит',
            'anxious': '😰 Тревожен',
            'excited': '🎉 В восторге',
            'tired': '😴 Устал'
        }

        chart_labels_readable = [mood_translation.get(label, label) for label in chart_labels]

        # Подсчитываем общее количество записей
        total_entries = len(mood_entries)

        # Определяем самое частое настроение
        most_common_mood = max(mood_data, key=mood_data.get) if total_entries > 0 else None
        most_common_mood_readable = mood_translation.get(most_common_mood,
                                                         most_common_mood) if most_common_mood else None

        logger.info(f'Statistics loaded for user {current_user.username}: {total_entries} entries')

        # Получаем рекомендации для самого частого настроения
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
            mood_entries=mood_entries[-10:] if mood_entries else [],  # Последние 10 записей для таблицы
            common_mood_recommendations=common_mood_recommendations
        )

    except Exception as e:
        logger.error(f'Error loading stats for {current_user.username}: {str(e)}')
        flash('❌ Произошла ошибка при загрузке статистики', 'danger')
        return redirect(url_for('main.dashboard'))


# Маршрут для рекомендаций (если модуль доступен)
if RECOMMENDATIONS_AVAILABLE:
    @bp.route('/recommendations')
    @login_required
    def recommendations_page():
        """Страница со всеми рекомендациями"""
        # Получаем все настроения с их рекомендациями
        all_recommendations = {}
        moods = RecommendationsManager.get_all_moods_with_recommendations()

        for mood in moods:
            all_recommendations[mood] = RecommendationsManager.get_recommendations_for_mood(mood, limit=10)

        return render_template('recommendations.html',
                               all_recommendations=all_recommendations)


    @bp.route('/api/recommendations/<mood>')
    @login_required
    def get_recommendations(mood):
        """API для получения рекомендаций по настроению"""
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
    # Если модуль рекомендаций недоступен, создаем заглушки
    @bp.route('/recommendations')
    @login_required
    def recommendations_page():
        flash('Функция рекомендаций временно недоступна', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/api/recommendations/<mood>')
    @login_required
    def get_recommendations(mood):
        return jsonify({
            'success': False,
            'error': 'Модуль рекомендаций недоступен'
        }), 501

# Маршруты для предсказаний
if PREDICTIONS_AVAILABLE:
    @bp.route('/prediction')
    @login_required
    def prediction():
        """Страница для получения предсказания"""
        try:
            # Получаем случайное предсказание
            prediction_obj, category_name = PredictionsManager.get_random_prediction()

            # Если предсказаний нет в базе, инициализируем их
            if not prediction_obj:
                PredictionsManager.initialize_default_predictions()
                prediction_obj, category_name = PredictionsManager.get_random_prediction()

            # Получаем все категории для фильтра
            all_categories = PredictionsManager.get_all_categories()

            return render_template(
                'prediction.html',
                prediction=prediction_obj,
                category_name=category_name,
                all_categories=all_categories
            )
        except Exception as e:
            logger.error(f'Error in prediction route: {str(e)}')
            flash('❌ Произошла ошибка при загрузке предсказания', 'danger')
            return redirect(url_for('main.dashboard'))


    @bp.route('/prediction/category/<category>')
    @login_required
    def prediction_by_category(category):
        """Получить предсказание по конкретной категории"""
        try:
            prediction_obj, category_name = PredictionsManager.get_random_prediction(category)

            if not prediction_obj:
                flash('Для этой категории пока нет предсказаний', 'info')
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
            flash('❌ Произошла ошибка при загрузке предсказания', 'danger')
            return redirect(url_for('main.prediction'))


    @bp.route('/api/prediction/random')
    @login_required
    def api_random_prediction():
        """API для получения случайного предсказания"""
        try:
            prediction_obj, category_name = PredictionsManager.get_random_prediction()

            if not prediction_obj:
                return jsonify({
                    'success': False,
                    'message': 'Нет предсказаний'
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
    # Если модуль предсказаний недоступен, создаем заглушки
    @bp.route('/prediction')
    @login_required
    def prediction():
        flash('Функция предсказаний временно недоступна', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/prediction/category/<category>')
    @login_required
    def prediction_by_category(category):
        flash('Функция предсказаний временно недоступна', 'info')
        return redirect(url_for('main.dashboard'))


    @bp.route('/api/prediction/random')
    @login_required
    def api_random_prediction():
        return jsonify({
            'success': False,
            'error': 'Модуль предсказаний недоступен'
        }), 501