#!/usr/bin/env python
"""
Скрипт для инициализации предсказаний в базе данных.
Запуск: python init_predictions.py
"""

import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import Prediction  # Импортируем модель Prediction
    from app.predictions_utils import PredictionsManager


    def main():
        """Основная функция инициализации"""
        print("🔮 Инициализация системы предсказаний...")

        # Создаем приложение
        app = create_app()

        with app.app_context():
            # Создаем все таблицы (если их нет)
            db.create_all()
            print("✅ Таблицы базы данных созданы")

            # Инициализируем предсказания по умолчанию
            PredictionsManager.initialize_default_predictions()

            # Показываем статистику
            total_preds = PredictionsManager.get_predictions_count()

            print(f"📊 Статистика предсказаний:")
            print(f"   • Всего предсказаний: {total_preds}")

            # Показываем категории
            categories = PredictionsManager.get_all_categories()
            print(f"   • Категорий: {len(categories)}")

            print("\n🎭 Категории предсказаний:")
            for key, value in categories.items():
                # Правильный запрос для подсчета предсказаний по категории
                count = db.session.query(Prediction).filter_by(category=key).count()
                print(f"   • {key} ({value}): {count} предсказаний")

            print("\n✅ Система предсказаний успешно инициализирована!")


    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что файл app/predictions_utils.py существует")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback

    traceback.print_exc()