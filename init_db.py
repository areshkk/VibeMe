#!/usr/bin/env python
"""
Скрипт для инициализации базы данных и рекомендаций.
Запуск: python init_db.py
"""

import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.recommendations_utils import RecommendationsManager
from app.models import Recommendation


def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация базы данных VibeMe...")

    # Создаем приложение
    app = create_app()

    with app.app_context():
        # Создаем все таблицы (если их нет)
        db.create_all()
        print("✅ Таблицы базы данных созданы")

        # Инициализируем рекомендации по умолчанию
        RecommendationsManager.initialize_default_recommendations()

        # Показываем статистику
        total_recs = Recommendation.query.count()

        print(f"📊 Статистика рекомендаций:")
        print(f"   • Всего рекомендаций в базе: {total_recs}")

        if total_recs > 0:
            # Показываем рекомендации по настроениям
            print("\n🎭 Рекомендации по настроениям:")
            moods = RecommendationsManager.get_all_moods_with_recommendations()
            for mood in moods:
                count = Recommendation.query.filter_by(mood=mood).count()
                print(f"   • {mood}: {count} рекомендаций")

        print("\n✅ База данных успешно инициализирована!")
        print("👉 Запустите приложение: python run.py")


if __name__ == '__main__':
    main()