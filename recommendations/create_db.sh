# Script to create database

#parsing script
#python parse2csv.py

python manage.py makemigrations
python manage.py migrate
echo Make make migrations

#scripts for fill base
python manage.py fill_users
echo Done fill users
python manage.py fill_address_base
echo Done fill address base
python manage.py fill_catalog
echo Done fill catalog
python manage.py fill_answers_questions
echo Done fill QA
python manage.py runserver 0.0.0.0:8000
