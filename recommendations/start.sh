# Script to create database and super user

mysql -uroot -e "create database Recservice;"
mysql -uroot -e "create user 'torres'@'localhost' identified by 'torres';"
mysql -uroot -e "grant all privileges on Recservice.* to 'torres'@'localhost' with grant option;"

#parsing script
#python3 parse2csv.py

python3 manage.py makemigrations
python3 manage.py migrate

#add all scripts for fill base
python3 manage.py fill_users
python3 manage.py fill_address_base
python3 manage.py fill_catalog
python3 manage.py fill_answers_questions




