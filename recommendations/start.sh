# Script to create database and super user

mysql -uroot -e "create database Recservice"
mysql -uroot -e "create user 'torres'@'localhost' identified by 'torres';"
mysql -uroot -e "grant all privileges on Recservice.* to 'torres'@'localhost' with grant option;"

#parsing script
python3 parse2csv.py

#add all scripts for fill base
python3 manage.py fill_base_from_file
python3 manage.py fill_address_base_from_file
python3 manage.py fill_catalog_from_file
python3 manage.py fill_answers_questions


