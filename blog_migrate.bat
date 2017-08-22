call orderenv\Scripts\activate.bat
call python manage.py makemigrations blog
call python manage.py migrate blog
