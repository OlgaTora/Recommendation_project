# Script to create database and super user
#
#mysql -uroot -e "create database Recservice;"
#mysql -uroot -e "create user 'torres'@'localhost' identified by 'torres';"
#mysql -uroot -e "grant all privileges on Recservice.* to 'torres'@'localhost' with grant option;"

#parsing script
#python3 parse2csv.py

#python3 manage.py makemigrations
python manage.py migrate
#python manage.py collectstatic --no-input

#add all scripts for fill base
python manage.py fill_users
echo Done fill users
python manage.py fill_address_base
echo Done fill address base
python manage.py fill_catalog
echo Done fill catalog
python manage.py fill_answers_questions
echo Done fill QA
python manage.py runserver 0.0.0.0:8000


