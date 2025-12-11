#!/usr/bin/env python
"""
Скрипт для инициализации рекомендаций в базе данных.
Запуск: python init_recommendations.py
"""

import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from recommendations_utils import RecommendationsManager


def main():
    """Основная функция инициализации"""
    print("🚀 Инициализация системы рекомендаций...")

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
        unique_moods = db.session.query(Recommendation.mood).distinct().count()

        print(f"📊 Статистика рекомендаций:")
        print(f"   • Всего рекомендаций: {total_recs}")
        print(f"   • Уникальных настроений: {unique_moods}")

        # Показываем рекомендации по настроениям
        print("\n🎭 Рекомендации по настроениям:")
        moods = RecommendationsManager.get_all_moods_with_recommendations()
        for mood in moods:
            count = Recommendation.query.filter_by(mood=mood).count()
            print(f"   • {mood}: {count} рекомендаций")

        print("\n✅ Система рекомендаций успешно инициализирована!")


if __name__ == '__main__':
    main()