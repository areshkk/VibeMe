from app import create_app, db
from app.models import User, MoodEntry, Recommendation
from recommendations_utils import RecommendationsManager

app = create_app()

with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("✅ Таблицы успешно созданы!")

    # Инициализируем рекомендации
    RecommendationsManager.initialize_default_recommendations()
    print("✅ Рекомендации инициализированы!")

    # Проверяем создание пользователя
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('TestPass123')
    db.session.add(test_user)
    db.session.commit()

    # Проверяем создание записи настроения
    test_mood = MoodEntry(mood='sad', notes='Тестовая запись', user_id=test_user.id)
    db.session.add(test_mood)
    db.session.commit()

    # Проверяем получение рекомендаций
    recommendations = RecommendationsManager.get_recommendations_for_mood('sad')
    print(f"✅ Рекомендации для 'sad': {len(recommendations)} штук")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")

    print("\n✅ Все модели работают корректно!")