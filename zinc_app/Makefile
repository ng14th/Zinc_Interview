run-app:
	python manage.py runserver
migrate:
	python manage.py migrate
makemigrations:
	python manage.py makemigrations

run-migrations:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

run-test:
	uv run python manage.py test tests --keepdb

run-server:
	uv run python manage.py makemigrations
	uv run python manage.py migrate
	uv run gunicorn -c src/configs/gunicorn_config.py src.dj_project.wsgi
	