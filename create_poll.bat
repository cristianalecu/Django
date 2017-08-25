md pollsite

cd pollsite

call python -m venv pollenv

cd ..
call pollsite\pollenv\Scripts\activate.bat

git clone git://github.com/django/django.git

call pip install -e django/
