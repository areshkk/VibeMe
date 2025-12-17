from app import create_app, db
from app.models import User, MoodEntry, Prediction

app = create_app()

with app.app_context():
    try:
        # Создаем все таблицы
        db.create_all()
        print("✅ Таблицы успешно созданы!")

        # Импортируем менеджер предсказаний
        try:
            from app.predictions_utils import PredictionsManager

            # Инициализируем предсказания
            PredictionsManager.initialize_default_predictions()
            print("✅ Предсказания инициализированы!")

            # Проверяем получение случайного предсказания
            prediction, category_name = PredictionsManager.get_random_prediction()
            if prediction:
                print(f"✅ Получено случайное предсказание: '{prediction.text}'")
                print(f"   Категория: {category_name}")
            else:
                print("❌ Не удалось получить предсказание")

            # Проверяем фильтрацию по категории
            prediction_love, love_category = PredictionsManager.get_random_prediction('love')
            if prediction_love:
                print(f"✅ Предсказание по категории 'love': '{prediction_love.text}'")

            # Проверяем количество предсказаний
            count = PredictionsManager.get_predictions_count()
            print(f"✅ Всего предсказаний в базе: {count}")

        except ImportError:
            print("⚠️ Модуль predictions_utils не найден, пропускаем тесты предсказаний")

        # Проверяем создание пользователя
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('TestPass123')
        db.session.add(test_user)
        db.session.commit()

        # Проверяем создание записи настроения
        test_mood = MoodEntry(mood='sad', notes='Тестовая запись', user_id=test_user.id)
        db.session.add(test_mood)
        db.session.commit()

        print("\n✅ Все модели работают корректно!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")