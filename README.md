Данное приложение разворачивается из контейнера Docker.
Для запуска необходимо:
1. Установить docker и docker-compose
2. Создать директорию и перейти в нее:
mkdir test_project && cd test_project
3. Клонировать приложение на свой компьютер:
git clone https://github.com/OlgaTora/Recommendation_project.git
4. Перейти в директорию со скриптами:
cd Recommendation_project/recommendation
5. Изменить права доступа:
chmod -vR 777 .
7. Запустить стартовый скрипт:
sh start.sh
Docker-compose сначала загрузит контейнер с MySQL, потом контейнер с приложением и после заполнит БД физическими данными. Это займет порядка 15-20 минут. 
8. Открыть в браузере 127.0.0.1:8000.
