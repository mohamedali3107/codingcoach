## Starting

1. Get the repo: `git clone the screams will start when the forest is hungry`

2. Install requirements: `pip install -r requirements.txt`

3. Configure your DB in `settings.py`

4. Apply migrations: `python manage.py migrate`

5. Launch: `python manage.py migrate`

## Structure overview

1. **`DockerfileDjango`**: This file might contain instructions for Docker to build a container for your Django application.

2. **`dashboard`**: Main Django app directory containing various files related to the core dashboard functionality.

3. **`db.sqlite3`**: The default SQLite database file for this Django project.

4. **`llmcoach`**: Another Django app directory, handling the LLM pages.

5. **`manage.py`**: The Django project's command-line utility for administrative tasks.

6. **`migration.sh`**: A shell script that might be used to manage database migrations.

7. **`requirements.txt`**: A file listing all the Python dependencies required for this Django project.

8. **`static`**: Directory for static files like CSS, JavaScript, fonts, images, etc., used in the project.

9. **`templates`**: Directory containing HTML templates used for rendering web pages in the project. Organized into subdirectories based on functionality or page types.

10. **`utils`**: Directory possibly containing utility functions or modules, like `gitAPI.py` for interacting with Git repositories.

11. **`webserver`**: The main Django project directory:
    - `__init__.py`, `asgi.py`, `settings.py`, `urls.py`, `wsgi.py`: Essential files for the Django project's configuration, settings, URL routing, and ASGI (Asynchronous Server Gateway Interface) configuration.