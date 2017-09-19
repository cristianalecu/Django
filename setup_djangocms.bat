cd ..
md venv
cd venv

call python -m venv  venv_djcms
call venv_djcms\Scripts\activate.bat  

cd ..\Django\

rem md django_cms
cd django_cms
rem pip install djangocms-installer
rem djangocms -p . django_cms

rem call pip install -r requirements.txt

rem del db.sqlite3
rem call python manage.py makemigrations
rem call python manage.py migrate
rem call python manage.py createsuperuser
call python manage.py runserver
