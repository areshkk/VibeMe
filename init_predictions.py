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

            # ОЧИСТКА существующих предсказаний (если нужно перезаписать)
            print("🧹 Очистка старых предсказаний...")
            Prediction.query.delete()
            db.session.commit()
            print("✅ Старые предсказания удалены")

            # Инициализируем предсказания по умолчанию (ВСЕ 300)
            PredictionsManager.initialize_default_predictions()

            # Показываем статистику
            total_preds = PredictionsManager.get_predictions_count()

            print(f"📊 Статистика предсказаний:")
            print(f"   • Всего предсказаний: {total_preds}")

            # Показываем категории с количеством предсказаний
            categories = PredictionsManager.get_all_categories()
            print(f"   • Категорий: {len(categories)}")

            print("\n🎭 Категории предсказаний с количеством:")
            for key, value in categories.items():
                # Правильный запрос для подсчета предсказаний по категории
                count = db.session.query(Prediction).filter_by(category=key).count()
                print(f"   • {value}: {count} предсказаний")

            # Проверяем, что все категории имеют по 30 предсказаний
            print("\n✅ Проверка распределения:")
            for key in categories.keys():
                count = db.session.query(Prediction).filter_by(category=key).count()
                if count == 30:
                    print(f"   ✅ {categories[key]}: {count}/30 ✓")
                else:
                    print(f"   ❌ {categories[key]}: {count}/30 (ОШИБКА: должно быть 30)")

            print(f"\n✅ Система предсказаний успешно инициализирована!")
            print(f"   Всего загружено: {total_preds} предсказаний")
            if total_preds == 300:
                print("   ✅ Все 300 предсказаний загружены успешно!")
            else:
                print(f"   ⚠️ Загружено {total_preds} из 300 предсказаний")


    if __name__ == '__main__':
        main()

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что файл app/predictions_utils.py существует")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback

    traceback.print_exc()