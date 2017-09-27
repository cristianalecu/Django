cd ..
md venv
cd venv

call python -m venv  venv_fin
call venv_fin\Scripts\activate.bat  

cd ..\Django\financiar

call pip install -r requirements.txt

rem del db.sqlite3
call python manage.py makemigrations
call python manage.py migrate
call python manage.py createsuperuser
call python manage.py runserver
