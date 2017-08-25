call pip install --upgrade pip
call pip install Django==1.11.4
call python -m venv orderenv
call orderenv\Scripts\activate.bat
call django-admin.py startproject ordersite .
call python manage.py migrate
call python manage.py createsuperuser
code .
