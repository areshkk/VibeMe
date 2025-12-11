# run.py
from app import create_app, db
import os
import sys

app = create_app()

# Создаем таблицы при запуске приложения
with app.app_context():
    try:
        print("🔧 Проверяю базу данных...")

        # Получаем путь к файлу БД
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']

        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            print(f"📁 Файл БД: {db_path}")

            # Создаем папку для БД, если нужно
            if os.path.dirname(db_path):
                os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Создаем все таблицы, если их нет
        db.create_all()
        print("✅ База данных проверена/создана")

        # Проверяем, какие таблицы созданы
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Таблицы в БД: {tables}")

        # Создаем тестового пользователя, если таблица user пуста
        from app.models import User

        if User.query.count() == 0:
            print("👤 Создаю тестового пользователя...")
            try:
                test_user = User(username='demo', email='demo@example.com')
                test_user.set_password('Demo123')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Тестовый пользователь создан")
                print("   Email: demo@example.com")
                print("   Password: Demo123")
            except Exception as e:
                print(f"⚠️ Не удалось создать тестового пользователя: {e}")
                db.session.rollback()

    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        import traceback

        traceback.print_exc()

# ⚠️ ВАЖНО: Двойные подчеркивания с обеих сторон!
if __name__ == '__main__':
    print(f"🚀 Запуск VibeMe...")
    print(f"📂 Текущая папка: {os.getcwd()}")
    print(f"🌐 Откройте в браузере: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
