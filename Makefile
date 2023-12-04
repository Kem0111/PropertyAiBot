migrations:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate


start: 
	uvicorn package.asgi:application --host 0.0.0.0 --port 8000 --proxy-headers
