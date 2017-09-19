cd ..
md venv
cd venv

call python -m venv  venv_djfrm
call venv_djfrm\Scripts\activate.bat  

cd ..\Django\djforms

call pip install -r requirements.txt

rem del db.sqlite3
call python manage.py makemigrations
call python manage.py migrate
call python manage.py createsuperuser
call python manage.py runserver
