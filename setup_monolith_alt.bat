cd ..
md venv
cd venv

call python -m venv  venv_mnl2
call venv_mnl2\Scripts\activate.bat  

cd ..\cloud_orders\monolith_alt

call pip install -r requirements.txt

rem del db.sqlite3
call python manage.py makemigrations
call python manage.py migrate
call python manage.py createsuperuser
call python manage.py runserver
