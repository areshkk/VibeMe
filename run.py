from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    print(f"Current working directory: {os.getcwd()}")
    print(f"Templates folder: {app.template_folder}")
    print(f"Templates exists: {os.path.exists(app.template_folder)}")
    app.run(debug=True)