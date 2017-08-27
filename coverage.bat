
rem pip install coverage

cd pollsite

del .coverage
rmdir /s /q htmlcov

coverage run --source='..' manage.py test polls

coverage html

start htmlcov/index.html

cd ..

